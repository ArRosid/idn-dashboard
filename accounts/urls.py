from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LogoutView,
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from accounts.views import signup, activate_account, profile, affiliate_view

app_name = "accounts"

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signup/<str:token>/", activate_account, name="activate_account"),
    path(
        "login/", LoginView.as_view(template_name="accounts/login.html"), name="login"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "settings/password/",
        PasswordChangeView.as_view(
            template_name="accounts/password_change.html",
            success_url=reverse_lazy("accounts:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "settings/password/done/",
        PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "reset/",
        PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            html_email_template_name="accounts/password_reset_email.html",
            email_template_name="accounts/password_reset_email.html",
            subject_template_name="accounts/password_reset_subject.txt",
            success_url=reverse_lazy("accounts:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "reset/done/",
        PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<str:uidb64>/<str:token>/",
        PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("profile/", profile, name="profile"),
    path("affiliate/", affiliate_view, name="affiliate"),
]
