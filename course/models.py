from django.db import models
from accounts.models import User


class Training(models.Model):
    name = models.CharField(max_length=100)
    duration = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    training_type = models.PositiveSmallIntegerField()
    scheddule = models.DateField()
    status = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("user", "training")
