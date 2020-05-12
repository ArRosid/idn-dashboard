from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text="Required.")

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
