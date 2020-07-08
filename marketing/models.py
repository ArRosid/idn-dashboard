from django.db import models

from core.models import BaseModel
from accounts.models import User
from marketing.choices import MarketingSourceChoices


class Interaksi(BaseModel):
    tim_marketing = models.ForeignKey(User, on_delete=models.CASCADE)
    nama_client = models.CharField(max_length=255)
    sumber = models.CharField(max_length=200, choices=MarketingSourceChoices.choices)
    no_hp = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    fb = models.CharField(max_length=100, blank=True, null=True)
    ig = models.CharField(max_length=100, blank=True, null=True)
    topik = models.TextField()

    def __str__(self):
        return f"{self.tim_marketing} - {self.nama_client}"

    class Meta:
        verbose_name = "Interaksi"
        verbose_name_plural = "Interaksi"
