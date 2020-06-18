from django import forms

from home.models import HiIDN


class HiIDNForms(forms.ModelForm):
    class Meta:
        model = HiIDN
        fields = ("nama", "no_hp", "email", "pertanyaan")


class HiIDNFormsAuthenticated(forms.ModelForm):
    class Meta:
        model = HiIDN
        fields = ("pertanyaan",)
