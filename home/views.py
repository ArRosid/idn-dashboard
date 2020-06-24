from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from course.models import Registration
from home.forms import HiIDNForms, HiIDNFormsAuthenticated


@login_required
def home(request):
    registrations = Registration.objects.filter(user=request.user).order_by(
        "-created_at"
    )
    context = {"registrations": registrations}
    return render(request, "home/index.html", context)


def hi_idn(request):
    if request.user.is_authenticated and not request.user.profile.is_valid():
        messages.error(
            request,
            "Anda harus melengkap profile Anda sebelum menghubungi admin, <a href='accounts/profile/'>disini</a>",
        )
        return redirect("home:home")

    if request.method == "POST":
        if request.user.is_authenticated:
            form = HiIDNFormsAuthenticated(request.POST)
            if form.is_valid():
                hi = form.save(commit=False)
                hi.nama = request.user.profile.name
                hi.email = request.user.email
                hi.no_hp = request.user.profile.phone_number
                hi.save()

                salam = settings.WA_HI.format(hi.nama).replace(" ", "%20")
                pertanyaan = hi.pertanyaan.replace(" ", "%20")
                url = (
                    settings.WA_URL + settings.WA_ADMIN + "&text=" + salam + pertanyaan
                )
                return redirect(url)

            return render(request, "home/hi_idn_authenticated.html", {"form": form})

        else:
            form = HiIDNForms(request.POST)
            if form.is_valid():
                hi = form.save()

                salam = settings.WA_HI.format(hi.nama).replace(" ", "%20")
                pertanyaan = hi.pertanyaan.replace(" ", "%20")
                url = (
                    settings.WA_URL + settings.WA_ADMIN + "&text=" + salam + pertanyaan
                )
                return redirect(url)

            return render(request, "home/hi_idn.html", {"form": form})

    else:
        if request.user.is_authenticated:
            form = HiIDNFormsAuthenticated()
            return render(request, "home/hi_idn_authenticated.html", {"form": form})
        else:
            form = HiIDNForms()
            return render(request, "home/hi_idn.html", {"form": form})
