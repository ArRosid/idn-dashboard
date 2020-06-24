from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from core.models import BaseModel
from accounts.managers import UserManager
from accounts.choices import LinkModelUsedFor, MengetahuiIDN


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class LinkToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    used_for = models.CharField(max_length=10, choices=LinkModelUsedFor.choices)
    is_valid = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Link Token"
        verbose_name_plural = "Link Token"

    def __str__(self):
        return self.key


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    ttl = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    jabatan = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    mengetahui_idn_dari = models.CharField(
        max_length=100, null=True, blank=True, choices=MengetahuiIDN.choices
    )
    affiliate_id = models.CharField(max_length=20, null=True, blank=True)
    affiliate_point = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user}"

    def is_valid(self):
        for field_name in self._meta.get_fields():
            if (
                field_name.name == "affiliate_id"
                or field_name.name == "affiliate_point"
            ):
                continue

            value = getattr(self, field_name.name, None)
            if value is None:
                return False
        return True

    def get_wa_link(self):
        if self.phone_number.startswith("0"):
            return "https://wa.me/62" + self.phone_number[1:].replace(" ", "").replace(
                "-", ""
            )
        if self.phone_number.startswith("+"):
            return "https://wa.me/" + self.phone_number[1:].replace(" ", "").replace(
                "-", ""
            )
        if self.phone_number.startswith("6"):
            return "https://wa.me/" + self.phone_number.replace(" ", "").replace(
                "-", ""
            )

    def get_wa_send_link(self):
        if self.phone_number.startswith("0"):
            return "https://api.whatsapp.com/send?phone=62" + self.phone_number[
                1:
            ].replace(" ", "").replace("-", "")
        if self.phone_number.startswith("+"):
            return "https://api.whatsapp.com/send?phone=" + self.phone_number[
                1:
            ].replace(" ", "").replace("-", "")
        if self.phone_number.startswith("6"):
            return "https://api.whatsapp.com/send?phone=" + self.phone_number.replace(
                " ", ""
            ).replace("-", "")
