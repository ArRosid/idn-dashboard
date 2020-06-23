from django import forms
from course.models import Registration
from course.choices import TrainingType
from course.models import (
    TrainingCategory,
    MonthYearScheddule,
    PaymentConfirm,
    Training,
    Scheddule,
    Discount,
    JadwalFile,
    MaxPeserta,
)


class RegistrationFormAdd(forms.ModelForm):
    training_category = forms.ModelChoiceField(
        queryset=TrainingCategory.objects.all(), label="Kategori Training"
    )
    training_type = forms.CharField(
        widget=forms.Select(choices=TrainingType.choices), label="Tipe Training"
    )
    month_year = forms.ModelChoiceField(
        queryset=MonthYearScheddule.objects.all(), label="Bulan"
    )

    class Meta:
        model = Registration
        fields = (
            "training_category",
            "training",
            "training_type",
            "month_year",
            "scheddule",
            "diskon_kode",
            "affiliate_kode",
        )
        labels = {
            "training": "Training",
            "scheddule": "Jadwal",
            "diskon_kode": "Kode Diskon",
            "affiliate_kode": "Kode Affiliate",
        }


class RegistrationFormUpdate(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ("training", "scheddule")


class PaymentConfirmForm(forms.ModelForm):
    class Meta:
        model = PaymentConfirm
        fields = ("amount", "proof_of_payment")
        labels = {"amount": "Jumlah Transfer", "proof_of_payment": "Bukti Pembayaran"}


class SchedduleForm(forms.ModelForm):
    class Meta:
        model = Scheddule
        fields = ("training", "training_type", "month_year", "day")


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ("category", "name", "duration", "price")


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ("kode", "persen", "end_date", "training_type")
        widgets = {"end_date": forms.TextInput(attrs={"placeholder": "YYYY-MM-DD"})}


class JadwalFileForm(forms.ModelForm):
    class Meta:
        model = JadwalFile
        fields = ("file",)


class MaxPesertaForm(forms.ModelForm):
    class Meta:
        model = MaxPeserta
        fields = ("max_peserta",)
