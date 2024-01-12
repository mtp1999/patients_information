# from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


# class CostumeUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ("email", "password1", "password2")


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "password")
