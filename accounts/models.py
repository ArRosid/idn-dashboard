from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from core.models import BaseModel
from accounts.managers import UserManager
from accounts.choices import LinkModelUsedFor

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


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
    company = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    facebook = models.CharField(max_length=100)

