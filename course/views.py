from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.utils import IntegrityError
from django.views import generic
from course.forms import (
    RegistrationFormAdd,
    PaymentConfirmForm,
    TrainingForm,
    SchedduleForm,
)
from course.models import (
    Registration,
    Training,
    Scheddule,
    MonthYearScheddule,
    DayScheddule,
)
from course.choices import TrainingType
import csv
import io


@login_required
def daftar_training(request):
    if request.method == "POST":
        form = RegistrationFormAdd(request.POST)
        try:
            if form.is_valid():
                reg = form.save(commit=False)
                reg.user = request.user
                reg.save()
                messages.success(
                    request, "Pendaftaran berhasil, silahkan check email Anda!"
                )
                return redirect("home:home")
        except IntegrityError:
            messages.error(request, "Anda sudah mendaftar training ini!")
    else:
        form = RegistrationFormAdd()

    if not request.user.profile.is_valid():
        messages.error(request, "Lengkapi profile anda sebelum mendaftar!")
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
    messages.error(request, "Pendaftaran berhasil di hapus")
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
            payment.save()
            reg.status = 1
            reg.save()
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
def jadwal_upload(request):
    error_list = []
    if request.method == "POST":
        csv_file = request.FILES["file"].file
        csv_file = io.TextIOWrapper(csv_file)  # python 3 only
        dialect = csv.Sniffer().sniff(csv_file.read(), delimiters=";,")
        csv_file.seek(0)

        content = list(csv.reader(csv_file, dialect))
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
