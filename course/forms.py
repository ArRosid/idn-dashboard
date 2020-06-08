from django import forms
from course.models import Registration
from course.choices import TrainingType
from course.models import TrainingCategory, MonthYearScheddule, Training


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
