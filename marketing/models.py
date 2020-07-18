from django.db import models

from core.models import BaseModel
from accounts.models import User
from course.models import Training
from marketing.choices import MarketingSourceChoices


class Interaksi(BaseModel):
    tim_marketing = models.ForeignKey(User, on_delete=models.CASCADE)
    nama_client = models.CharField(max_length=255)
    training_terkait = models.ForeignKey(
        Training, on_delete=models.CASCADE, null=True, blank=True
    )
    sumber = models.CharField(max_length=200, choices=MarketingSourceChoices.choices)
    no_hp = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    fb = models.CharField(max_length=100, blank=True, null=True)
    ig = models.CharField(max_length=100, blank=True, null=True)
    topik = models.TextField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.tim_marketing} - {self.nama_client}"

    class Meta:
        verbose_name = "Interaksi"
        verbose_name_plural = "Interaksi"
        # constraints = [
        #     models.UniqueConstraint(fields=["no_hp", "date_created"], name="no_hp unik"),
        #     models.UniqueConstraint(fields=["email", "date_created"], name="email unik"),
        #     models.UniqueConstraint(fields=["fb", "date_created"], name="fb unik"),
        #     models.UniqueConstraint(fields=["ig", "date_created"], name="ig unik"),
        # ]
        unique_together = (
            ("no_hp", "date_created"),
            ("email", "date_created"),
            ("fb", "date_created"),
            ("ig", "date_created"),
        )
