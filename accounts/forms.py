from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User=get_user_model()

class SignupForm(UserCreationForm):
    email=forms.EmailField(label="이메일")

    class Meta(UserCreationForm):
        model=User
        fields=['email','nickname','date_of_birth','phone','username']

