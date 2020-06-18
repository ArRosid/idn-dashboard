from django.db import models
from core.models import BaseModel


class HiIDN(BaseModel):
    nama = models.CharField(max_length=100)
    no_hp = models.CharField(max_length=100)
    email = models.EmailField()
    pertanyaan = models.TextField(max_length=255)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "HI IDN"
        verbose_name_plural = "HI IDN"
