from django.db import models
from django.db.models import Q
from core.models import BaseModel
from accounts.models import User
from course.choices import TrainingType, RegistrationPaymentStatus, Month
from course.utils import upload_bukti_pembayaran


class TrainingCategory(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Training Category"
        verbose_name_plural = "Training Categories"


class Training(BaseModel):
    category = models.ForeignKey(TrainingCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    duration = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField()

    class Meta:
        unique_together = ("category", "name", "duration", "price")

    def __str__(self):
        return self.name


class MonthYearScheddule(BaseModel):
    month = models.PositiveSmallIntegerField(choices=Month.choices)
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{Month.choices[self.month-1][1]} {self.year}"

    class Meta:
        verbose_name = "Mont Year Scheddule"


class DayScheddule(BaseModel):
    month_year = models.ForeignKey(MonthYearScheddule, on_delete=models.CASCADE)
    day = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Day Scheddule"

    def __str__(self):
        return f"{self.day}, {self.month_year}"


class Scheddule(BaseModel):
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    training_type = models.PositiveSmallIntegerField(choices=TrainingType.choices)
    month_year = models.ForeignKey(MonthYearScheddule, on_delete=models.CASCADE)
    day = models.ForeignKey(DayScheddule, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("training", "training_type", "month_year", "day")

    def __str__(self):
        return f"{self.day}"

    def get_training_type(self):
        return TrainingType.choices[self.training_type][1]

    def get_jml_peserta(self):
        all_reg = Registration.objects.filter(scheddule=self)
        paid_reg = all_reg.filter(Q(status=2) | Q(status=3))
        return len(paid_reg)


class Registration(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    training_category = models.ForeignKey(TrainingCategory, on_delete=models.CASCADE)
    training_type = models.PositiveSmallIntegerField(choices=TrainingType.choices)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    month_year = models.ForeignKey(MonthYearScheddule, on_delete=models.CASCADE)
    scheddule = models.ForeignKey(Scheddule, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        choices=RegistrationPaymentStatus.choices,
        default=RegistrationPaymentStatus.not_paid,
    )
    is_retraining = models.BooleanField(default=False)
    diskon_kode = models.CharField(max_length=100, null=True, blank=True)
    affiliate_kode = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.training}"

    class Meta:
        unique_together = ("user", "training", "training_type")

    def get_status(self):
        return RegistrationPaymentStatus.choices[self.status][1]

    def get_training_type(self):
        return TrainingType.choices[self.scheddule.training_type][1]


class PaymentConfirm(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    amount = models.IntegerField()
    proof_of_payment = models.ImageField(upload_to=upload_bukti_pembayaran)
    status = models.PositiveSmallIntegerField(choices=RegistrationPaymentStatus.choices)

    class Meta:
        verbose_name = "Payment Confirm"

    def get_status(self):
        return RegistrationPaymentStatus.choices[self.status][1]

    def __str__(self):
        return f"{self.user} - {self.registration.training}"


class Discount(BaseModel):
    persen = models.PositiveIntegerField()
    kode = models.CharField(max_length=100, unique=True)
    end_date = models.DateField()
    training_type = models.PositiveSmallIntegerField(choices=TrainingType.choices)

    def __str__(self):
        return self.kode

    def get_training_type(self):
        return TrainingType.choices[self.training_type][1]


class JadwalFile(BaseModel):
    file = models.FileField(upload_to="jadwal_file")


class MaxPeserta(BaseModel):
    max_peserta = models.PositiveIntegerField()
