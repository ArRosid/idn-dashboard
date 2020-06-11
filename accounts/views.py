from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from accounts.forms import SignUpForm, ProfileForm
from accounts.tokens import token_generator
from accounts.utils import SendEmail
from accounts.models import LinkToken


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            token = token_generator.make_token(user)
            LinkToken.objects.create(user=user, key=token, used_for=0)
            path = reverse("accounts:activate_account", kwargs={"token": token})
            link = request.build_absolute_uri(path)
            SendEmail(user=user).account_activation(link=link)
            messages.success(
                request,
                "Akun Anda berhasil dibuat, silahkan check email untuk melakukan konfirmasi",
            )
            return redirect("accounts:login")

    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


def activate_account(request, **kwargs):
    try:
        key = kwargs["token"]
        token = LinkToken.objects.get(key=key)
    except:
        token = None
    print(token)
    if token is not None and token.is_valid:
        token.user.is_active = True
        token.user.save()
        token.is_valid = False
        token.save()
        login(request, user=token.user)
        messages.success(request, "Akun Anda sudah aktif!")
        return redirect("home:home")
    else:
        messages.error(
            request, "Link activation sudah tidak valid, silahkan register ulang"
        )
        return redirect("accounts:signup")


@login_required()
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Akun Anda berhasil di update!")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "accounts/update_profile.html", {"form": form})
