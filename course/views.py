from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from course.forms import RegistrationFormAdd
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


# class TrainingAutoComplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         qs = super(TrainingAutoComplete, self).get_queryset()
#         category = self.forwarded.get("training_category", None)
#
#         if category:
#             qs = qs.filter(category=category)
#
#         return qs
