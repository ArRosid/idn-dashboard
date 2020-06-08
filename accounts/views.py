from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from accounts.forms import SignUpForm
from accounts.tokens import token_generator
from accounts.utils import SendEmail
from accounts.models import User, LinkToken


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            token = token_generator.make_token(user)
            LinkToken.objects.create(user=user, key=token, used_for=0)
            path = reverse(
                "accounts:activate_account", kwargs={"token": token}
            )
            link = request.build_absolute_uri(path)
            SendEmail(user=user).account_activation(link=link)
            return HttpResponse("<h1>Check your email</h1>")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


def activate_account(request, **kwargs):
    try:
        key = kwargs["token"]
        token = LinkToken.objects.get(key=key)
    except:
        token = None

    if token is not None and token.is_valid:
        token.user.is_active = True
        token.user.save()
        token.is_valid = False
        token.save()
        return redirect("home:home")
    else:
        return HttpResponse("<h1>Activation link not valid!</h1>")

