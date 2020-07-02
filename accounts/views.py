from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from accounts.forms import SignUpForm, ProfileForm
from accounts.tokens import token_generator
from accounts.utils import SendEmail
from accounts.models import LinkToken, Profile
from course.models import Registration, PointHistory


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
            return redirect("home:home")
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "accounts/update_profile.html", {"form": form})


@login_required
def affiliate_view(request):
    affiliate_id = request.user.profile.affiliate_id
    affiliate_point = request.user.profile.affiliate_point
    my_affiliate = Registration.objects.filter(affiliate_kode=affiliate_id)

    my_affiliate_code = request.user.profile.affiliate_id
    my_downlink = Registration.objects.filter(affiliate_kode=my_affiliate_code)
    my_downlink_fix = my_downlink.filter(Q(status=2) | Q(status=3))
    my_point_history = PointHistory.objects.filter(user=request.user)
    print(my_point_history)
    return render(
        request,
        "accounts/affiliate_list.html",
        {
            "affiliate_id": affiliate_id,
            "affiliate_point": affiliate_point,
            "my_affiliate": my_affiliate,
            "my_downlink": my_downlink_fix,
            "my_point_history": my_point_history,
        },
    )
