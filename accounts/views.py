from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from accounts.forms import SignUpForm
from accounts.tokens import token_generator
from accounts.utils import SendEmail
from accounts.models import User


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            path = reverse(
                "accounts:activate_account", kwargs={"uid": uid, "token": token}
            )
            link = request.build_absolute_uri(path)
            SendEmail(user=user).account_activation(link=link)
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


def activate_account(request, **kwargs):
    try:
        uid = force_text(urlsafe_base64_decode(kwargs["uid"]))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and token_generator.check_token(user, kwargs["token"]):
        user.is_active = True
        user.save()
        return redirect("home")
    else:
        return "<h1>activation invalid</h1>"
