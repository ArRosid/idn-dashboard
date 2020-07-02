from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from accounts.models import Profile
import random
import string


def randomStringAffiliateID(stringLength=8):
    letters = "".join(
        random.choice(string.ascii_lowercase) for i in range(stringLength)
    )
    while True:
        try:
            Profile.objects.get(affiliate_id=letters)
        except:
            break
    return letters


class SendEmail:
    def __init__(self, user):
        self.user = user

    def account_activation(self, link):
        html_message = render_to_string(
            "email/account_activation.html", {"name": self.user.email, "link": link,}
        )
        plain_message = strip_tags(html_message)

        send_mail(
            subject="Aktifasi Akun IDN.ID",
            message=plain_message,
            from_email=settings.EMAIL_FORM,
            recipient_list=[self.user.email,],
            html_message=html_message,
            fail_silently=False,
        )

    def panduan_pembayaran(self, data):
        html_message = render_to_string("email/panduan_pembayaran.html", data)
        plain_message = strip_tags(html_message)

        send_mail(
            subject="Panduan Pembayaran Training IDN.ID",
            message=plain_message,
            from_email=settings.EMAIL_FORM,
            recipient_list=[self.user.email,],
            html_message=html_message,
            fail_silently=False,
        )

    def konfirmasi_pembayaran_dp(self, data):
        html_message = render_to_string("email/konfirmasi_pembayaran_dp.html", data)
        plain_message = strip_tags(html_message)

        send_mail(
            subject="Konfirmasi Pembayaran Training IDN.ID",
            message=plain_message,
            from_email=settings.EMAIL_FORM,
            recipient_list=[self.user.email,],
            html_message=html_message,
            fail_silently=False,
        )

    def konfirmasi_pembayaran_lunas(self, data):
        html_message = render_to_string("email/konfirmasi_pembayaran_lunas.html", data)
        plain_message = strip_tags(html_message)

        send_mail(
            subject="Konfirmasi Pembayaran Training IDN.ID",
            message=plain_message,
            from_email=settings.EMAIL_FORM,
            recipient_list=[self.user.email,],
            html_message=html_message,
            fail_silently=False,
        )

    def konfirmasi_pembayaran_tolak(self, data):
        html_message = render_to_string("email/konfirmasi_pembayaran_tolak.html", data)
        plain_message = strip_tags(html_message)

        send_mail(
            subject="Konfirmasi Pembayaran Training IDN.ID",
            message=plain_message,
            from_email=settings.EMAIL_FORM,
            recipient_list=[self.user.email,],
            html_message=html_message,
            fail_silently=False,
        )
