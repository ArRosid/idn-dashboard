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
        fields = ("name", "company", "address", "phone_number", "facebook")
