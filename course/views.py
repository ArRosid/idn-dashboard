from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from course.forms import RegistrationFormAdd, PaymentConfirmForm
from course.models import Registration, Training


@login_required
def daftar_training(request):
    if request.method == "POST":
        form = RegistrationFormAdd(request.POST)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.user = request.user
            reg.save()
            messages.success(
                request, "Pendaftaran berhasil, silahkan check email Anda!"
            )
            return redirect("home:home")
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
