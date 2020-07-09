from django import forms
from marketing.models import Interaksi


class InteraksiForm(forms.ModelForm):
    class Meta:
        model = Interaksi
        fields = (
            "nama_client",
            "training_terkait",
            "sumber",
            "no_hp",
            "email",
            "fb",
            "ig",
            "topik",
        )
