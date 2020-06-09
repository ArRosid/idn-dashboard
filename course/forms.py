from django import forms
from course.models import Registration
from course.choices import TrainingType
from course.models import (
    TrainingCategory,
    MonthYearScheddule,
    PaymentConfirm,
    Training,
    Scheddule,
)


class RegistrationFormAdd(forms.ModelForm):
    training_category = forms.ModelChoiceField(queryset=TrainingCategory.objects.all())
    training_type = forms.CharField(widget=forms.Select(choices=TrainingType.choices))
    month_year = forms.ModelChoiceField(queryset=MonthYearScheddule.objects.all())

    class Meta:
        model = Registration
        fields = (
            "training_category",
            "training",
            "training_type",
            "month_year",
            "scheddule",
        )


class RegistrationFormUpdate(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ("training", "scheddule")


class PaymentConfirmForm(forms.ModelForm):
    class Meta:
        model = PaymentConfirm
        fields = ("amount", "proof_of_payment")


class SchedduleForm(forms.ModelForm):
    class Meta:
        model = Scheddule
        fields = ("training", "training_type", "month_year", "day")


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ("category", "name", "duration")
