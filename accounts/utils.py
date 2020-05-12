from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


class SendEmail:
    def __init__(self, user):
        self.user = user

    def account_activation(self, link):
        html_message = render_to_string(
            "email/account_activation.html", {"name": self.user.name, "link": link,}
        )
        plain_message = strip_tags(html_message)

        send_mail(
            subject="Account Activation",
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email,],
            html_message=html_message,
            fail_silently=False,
        )
