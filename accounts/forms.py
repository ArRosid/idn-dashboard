from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User, Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text="Required.")

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "name",
            "ttl",
            "company",
            "jabatan",
            "address",
            "phone_number",
            "mengetahui_idn_dari",
        )
        labels = {
            "name": "Nama",
            "ttl": "Tempat Tanggal Lahir",
            "company": "Perusahaan",
            "jabatan": "Jabatan",
            "address": "Alamat",
            "phone_number": "No HP (WA)",
            "mengetahui_idn_dari": "Mengetahui IDN dari Mana?",
        }
