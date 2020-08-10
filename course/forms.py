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
from course.utils import max_file_size_2m


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
            "affiliate_point_used",
        )
        labels = {
            "training": "Training",
            "scheddule": "Jadwal",
            "diskon_kode": "Kode Diskon",
            "affiliate_kode": "Kode Affiliate",
            "affiliate_point_used": "Gunakan Affiliate Point",
        }
        widgets = {
            "affiliate_point_used": forms.TextInput(
                attrs={"placeholder": "Contoh: 200"}
            )
        }


class RegistrationFormUpdate(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ("training", "scheddule")


class PaymentConfirmForm(forms.ModelForm):
    proof_of_payment = forms.FileField(
        validators=[max_file_size_2m], label="Bukti Pembayaran (Max 1M)"
    )

    class Meta:
        model = PaymentConfirm
        fields = ("amount", "proof_of_payment")
        labels = {"amount": "Jumlah Transfer", "proof_of_payment": "Bukti Pembayaran"}


class SchedduleForm(forms.ModelForm):
    day_ = forms.CharField(required=False)

    class Meta:
        model = Scheddule
        fields = ("training", "training_type", "month_year", "day_")


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ("category", "name", "duration", "price", "exclude_diskon")


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ("kode", "persen", "end_date", "training_type", "diskon_pelajar")
        widgets = {"end_date": forms.TextInput(attrs={"placeholder": "YYYY-MM-DD"})}


class JadwalFileForm(forms.ModelForm):
    class Meta:
        model = JadwalFile
        fields = ("file",)


class MaxPesertaForm(forms.ModelForm):
    class Meta:
        model = MaxPeserta
        fields = ("max_peserta",)
