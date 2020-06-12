from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.utils import IntegrityError
from django.views import generic
from django.conf import settings
from django.utils import timezone
from course.forms import (
    RegistrationFormAdd,
    PaymentConfirmForm,
    TrainingForm,
    SchedduleForm,
    DiscountForm,
    JadwalFileForm,
    MaxPesertaForm,
)
from course.models import (
    Registration,
    Training,
    Scheddule,
    MonthYearScheddule,
    DayScheddule,
    PaymentConfirm,
    Discount,
    MaxPeserta,
)
from accounts.utils import SendEmail
from course.choices import TrainingType
import csv
import os


@login_required
def daftar_training(request):
    if request.method == "POST":
        form = RegistrationFormAdd(request.POST)
        try:
            if form.is_valid():
                reg = form.save(commit=False)
                reg.user = request.user
                harga_diskon = reg.training.price
                try:
                    max_peserta = MaxPeserta.objects.get(id=1)
                except:
                    max_peserta = None

                if (
                    max_peserta
                    and reg.scheddule.get_jml_peserta() >= max_peserta.max_peserta
                ):
                    raise Exception(
                        "Mohon maaf, Jadwal ini sudah Full, silahkan pilih jadwal lain"
                    )

                if reg.diskon_kode:
                    diskon = Discount.objects.get(kode=reg.diskon_kode)
                    if (
                        timezone.now().date() <= diskon.end_date
                        and reg.training_type == diskon.training_type
                    ):
                        harga_diskon = reg.training.price - (
                            reg.training.price * diskon.persen / 100
                        )
                    else:
                        raise Exception(
                            "Diskon tidak berlaku untuk tipe training ini atau sudah berahir"
                        )

                reg.save()
                data = {
                    "name": reg.user.email,
                    "training": reg.training.name,
                    "training_type": reg.get_training_type(),
                    "jadwal": f"{reg.scheddule.day.day}, {reg.month_year}",
                    "harga_asli": "{:,}".format(reg.training.price),
                    "harga_diskon": "{:,}".format(harga_diskon),
                }
                SendEmail(user=reg.user).panduan_pembayaran(data)
                messages.success(
                    request,
                    "Pendaftaran berhasil, silahkan check email Anda untuk melihat Panduan Pembayaran",
                )
                return redirect("home:home")
        except IntegrityError:
            messages.error(request, "Anda sudah mendaftar training ini!")
        except Discount.DoesNotExist:
            messages.error(request, "Kode diskon tidak valid")
        except Exception as e:
            messages.error(request, e)

    else:
        form = RegistrationFormAdd()

    if not request.user.profile.is_valid():
        messages.error(
            request,
            "Anda harus melengkap profile Anda sebelum mendaftar, <a href='accounts/profile/'>disini</a>",
        )
        return redirect("home:home")

    context = {"form": form, "button": "Daftar Training"}
    return render(request, "course/daftar_training.html", context)


@login_required
def edit_pendaftaran(request, pk):
    reg = get_object_or_404(Registration, pk=pk)
    if request.method == "POST":
        form = RegistrationFormAdd(request.POST, instance=reg)
        if form.is_valid():
            form.save()
            messages.success(request, "Pendaftaran berhasil di edit!")
            return redirect("home:home")
    else:
        form = RegistrationFormAdd(instance=reg)

    context = {"form": form, "button": "Update Training"}
    return render(request, "course/daftar_training.html", context)


@login_required
def delete_registration(request, pk):
    reg = get_object_or_404(Registration, pk=pk)
    reg.delete()
    messages.success(request, "Pendaftaran berhasil di hapus")
    return redirect("home:home")


@login_required
def payment_confirm(request, registration_id):
    reg = get_object_or_404(Registration, pk=registration_id)
    if request.method == "POST":
        form = PaymentConfirmForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.registration = reg
            payment.user = request.user
            payment.status = 1
            payment.save()
            reg.status = 1
            reg.save()
            messages.success(
                request,
                "Terimakasih telah melakukan konfirmasi pembayaran. Admin kami akan segera menghubungi Anda via email maksimal 1x24 jam",
            )
            return redirect("home:home")
    else:
        form = PaymentConfirmForm()
    return render(request, "course/payment_confirm.html", {"form": form})


@staff_member_required(login_url="accounts:login")
def list_jadwal(request):
    scheds = Scheddule.objects.all().order_by("-created_at")
    context = {"scheds": scheds}
    return render(request, "course/list_jadwal.html", context)


@staff_member_required(login_url="accounts:login")
def download_contoh_jadwal(request):
    file = os.path.join(settings.BASE_DIR, "templates/master/master_import_jadwal.csv")
    if os.path.exists(file):
        with open(file, "rb") as fh:
            response = HttpResponse(fh.read(), content_type="text/csv")
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                file
            )
            return response


class AddJadwal(generic.CreateView):
    model = Scheddule
    template_name = "course/add_jadwal.html"
    form_class = SchedduleForm

    def get_success_url(self):
        return reverse("course:list_jadwal")


class UpdateJadwal(generic.UpdateView):
    model = Scheddule
    form_class = SchedduleForm
    template_name = "course/edit_jadwal.html"

    def get_success_url(self):
        return reverse("course:list_jadwal")


@staff_member_required(login_url="acounts:login")
def delete_jadwal(request, pk):
    jadwal = get_object_or_404(Scheddule, pk=pk)
    jadwal.delete()
    messages.error(request, "Jadwal berhasil di hapus")
    return redirect("course:list_jadwal")


@staff_member_required(login_url="accounts:login")
def list_training(request):
    list_training = Training.objects.all().order_by("created_at")
    context = {"list_training": list_training}
    return render(request, "course/list_training.html", context)


@staff_member_required(login_url="accounts:login")
def add_training(request):
    if request.method == "POST":
        form = TrainingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Training berhasil ditambahkan")
            return redirect("course:list_training")
    else:
        form = TrainingForm()

    return render(request, "course/add_training.html", {"form": form})


class UpdateTraining(generic.UpdateView):
    model = Training
    form_class = TrainingForm
    template_name = "course/edit_training.html"

    def get_success_url(self):
        return reverse("course:list_training")


@staff_member_required(login_url="acounts:login")
def delete_training(request, pk):
    training = get_object_or_404(Training, pk=pk)
    training.delete()
    messages.error(request, "Training berhasil di hapus")
    return redirect("course:list_training")


@staff_member_required(login_url="accounts:login")
def list_pembayaran(request):
    list_pembayaran = PaymentConfirm.objects.filter(status=1)
    return render(
        request, "course/list_pembayaran.html", {"list_pembayaran": list_pembayaran}
    )


@staff_member_required(login_url="accounts:login")
def list_pembayaran_dp_lunas(request):
    list_pembayaran = PaymentConfirm.objects.filter(Q(status=2) | Q(status=3))
    return render(
        request,
        "course/list_pembayaran_dp_lunas.html",
        {"list_pembayaran": list_pembayaran, "title": "List Pembayaran DP / Lunas"},
    )


@staff_member_required(login_url="accounts:login")
def list_pembayaran_ditolak(request):
    list_pembayaran = PaymentConfirm.objects.filter(Q(status=4))
    return render(
        request,
        "course/list_pembayaran_dp_lunas.html",
        {"list_pembayaran": list_pembayaran, "title": "List Pembayaran Ditolak"},
    )


@staff_member_required(login_url="accounts:login")
def konfirmasi_pembayaran_dp(request, pk):
    pembayaran = get_object_or_404(PaymentConfirm, pk=pk)
    pembayaran.registration.status = 2
    pembayaran.registration.save()
    pembayaran.status = 2
    pembayaran.save()
    data = {
        "name": pembayaran.user.email,
        "training": pembayaran.registration.training.name,
        "training_type": pembayaran.registration.get_training_type(),
        "jadwal": f"{pembayaran.registration.scheddule.day.day}, {pembayaran.registration.month_year}",
    }
    SendEmail(user=pembayaran.user).konfirmasi_pembayaran_dp(data)
    return redirect("course:list_pembayaran")


@staff_member_required(login_url="accounts:login")
def konfirmasi_pembayaran_lunas(request, pk):
    pembayaran = get_object_or_404(PaymentConfirm, pk=pk)
    pembayaran.registration.status = 3
    pembayaran.registration.save()
    pembayaran.status = 3
    pembayaran.save()
    data = {
        "name": pembayaran.user.email,
        "training": pembayaran.registration.training.name,
        "training_type": pembayaran.registration.get_training_type(),
        "jadwal": f"{pembayaran.registration.scheddule.day.day}, {pembayaran.registration.month_year}",
    }
    SendEmail(user=pembayaran.user).konfirmasi_pembayaran_lunas(data)
    return redirect("course:list_pembayaran_dp_lunas")


@staff_member_required(login_url="accounts:login")
def hapus_konfirmasi(request, pk):
    pembayaran = get_object_or_404(PaymentConfirm, pk=pk)
    pembayaran.registration.status = 1
    pembayaran.registration.save()
    pembayaran.status = 1
    pembayaran.save()
    return redirect("course:list_pembayaran_dp_lunas")


@staff_member_required(login_url="accounts:login")
def tolak_pembayaran(request, pk):
    pembayaran = get_object_or_404(PaymentConfirm, pk=pk)
    pembayaran.registration.status = 4
    pembayaran.registration.save()
    pembayaran.status = 4
    pembayaran.save()
    data = {
        "name": pembayaran.user.email,
        "training": pembayaran.registration.training.name,
        "training_type": pembayaran.registration.get_training_type(),
        "jadwal": f"{pembayaran.registration.scheddule.day.day}, {pembayaran.registration.month_year}",
    }
    SendEmail(user=pembayaran.user).konfirmasi_pembayaran_tolak(data)
    return redirect("course:list_pembayaran_dp_lunas")


@staff_member_required(login_url="accounts:login")
def list_pendaftar_belum_bayar(request):
    list_pendaftar = Registration.objects.filter(status=0)
    return render(
        request, "course/list_pendaftar.html", {"list_pendaftar": list_pendaftar}
    )


@staff_member_required(login_url="accounts:login")
def export_pendaftar_belum_bayar(request):
    if "last" in request.GET:
        date = timezone.now() - timezone.timedelta(days=int(request.GET.get("last")))
        list_pendaftar = Registration.objects.filter(
            Q(status=0) & Q(created_at__gte=date)
        ).order_by("-created_at")
    else:
        list_pendaftar = Registration.objects.filter(status=0).order_by("-created_at")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="pendaftar_belum_bayar.csv"'

    writer = csv.writer(response, delimiter=";")

    writer.writerow(
        ["User", "Training", "Training Type", "Jadwal", "No HP", "Email", "Created At"]
    )

    rows = []
    for pendaftar in list_pendaftar:
        col = []
        col.append(pendaftar.user.profile.name)
        col.append(pendaftar.training.name)
        col.append(pendaftar.get_training_type())
        col.append(
            f"{pendaftar.scheddule.day}, {pendaftar.scheddule.month_year.month} {pendaftar.scheddule.month_year.year}"
        )
        col.append(pendaftar.user.profile.phone_number)
        col.append(pendaftar.user.email)
        col.append(pendaftar.created_at)
        rows.append(col)

    for row in rows:
        writer.writerow(row)

    return response


@staff_member_required(login_url="accounts:login")
def list_peserta(request, pk):
    jadwal = Scheddule.objects.get(pk=pk)
    all_peserta = Registration.objects.filter(Q(scheddule=jadwal))
    peserta_bayar = all_peserta.filter(Q(status=2) | Q(status=3))
    return render(request, "course/list_peserta.html", {"peserta_bayar": peserta_bayar})


@staff_member_required(login_url="accounts:login")
def list_diskon(request):
    diskon = Discount.objects.all().order_by("-created_at")
    return render(request, "course/list_diskon.html", {"diskon": diskon})


@staff_member_required(login_url="accounts:login")
def add_diskon(request):
    if request.method == "POST":
        form = DiscountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Diskon berhasil ditambahkan")
            return redirect("course:list_diskon")
    else:
        form = DiscountForm()

    return render(request, "course/add_diskon.html", {"form": form})


class UpdateDiskon(generic.UpdateView):
    model = Discount
    form_class = DiscountForm
    template_name = "course/edit_diskon.html"

    def get_success_url(self):
        return reverse("course:list_diskon")


@staff_member_required(login_url="acounts:login")
def delete_diskon(request, pk):
    diskon = get_object_or_404(Discount, pk=pk)
    diskon.delete()
    messages.error(request, "Diskon berhasil di hapus")
    return redirect("course:list_diskon")


@staff_member_required(login_url="accounts:login")
def upload_jadwal(request):
    error_list = []

    if request.method == "POST":
        form = JadwalFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            csv_file = open(file.file.url.strip("/"), "r")
            content = list(csv.reader(csv_file, delimiter=";"))
            csv_file.close()

            # hapus file & model instance
            os.remove(file.file.url.strip("/"))
            file.delete()

            master_header = ["ï»¿training", "training_type", "month", "year", "day"]
            header = content.pop(0)
            if header != master_header:
                messages.error(
                    request, "Format file tidak sesuai, silahkan download contohnya"
                )
                return redirect("course:upload_jadwal")

            for row in content:
                try:
                    training = Training.objects.get(name=row[0])
                    training_type = TrainingType.dict_choices[row[1]]
                    month_year = MonthYearScheddule.objects.get(
                        month=int(row[2]), year=int(row[3])
                    )
                    day, created = DayScheddule.objects.get_or_create(
                        month_year=month_year, day=row[4]
                    )
                    Scheddule.objects.create(
                        training=training,
                        training_type=training_type,
                        month_year=month_year,
                        day=day,
                    )
                except IntegrityError:
                    row.append("jadwal tersebut sudah ada")
                    error_list.append(row)
                except Exception as e:
                    row.append(e)
                    error_list.append(row)
            messages.success(request, "Jadwal berhasil di upload")

    return render(request, "course/jadwal_upload.html", {"error_list": error_list})


@staff_member_required(login_url="accounts:login")
def set_max_peserta(request):
    try:
        max_peserta = MaxPeserta.objects.get(id=1)
    except:
        max_peserta = MaxPeserta.objects.create(max_peserta=5)

    if request.method == "POST":
        form = MaxPesertaForm(request.POST, instance=max_peserta)
        if form.is_valid():
            form.save()
            messages.success(request, "Max Peserta berhasil diupdate")
            return redirect("course:set_max_peserta")
    else:
        form = MaxPesertaForm(instance=max_peserta)

    return render(request, "course/set_max_peserta.html", {"form": form})
