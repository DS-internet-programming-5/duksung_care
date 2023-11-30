from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError, ObjectDoesNotExist

User=get_user_model()

class SignupForm(UserCreationForm):
    email=forms.EmailField(label="이메일")
    class Meta(UserCreationForm):
        model=User
        fields=('email','nickname','date_of_birth','phone','username','profileImg')
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@duksung.ac.kr'):
            email += '@duksung.ac.kr'

        if email and User.objects.filter(email=email).exists():
            raise ValidationError('이미 등록된 이메일 주소입니다.')

        return email

class LoginForm(forms.Form):
    email=forms.CharField()
    password = forms.CharField(
       widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "패스워드"})
    )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@duksung.ac.kr'):
            email += '@duksung.ac.kr'

        return email

    def clean(self):
        user = self.authenticate_via_email()
        if not user:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        else:
            self.user = user
        return self.cleaned_data

    def authenticate_user(self):
        return authenticate(
            username=self.user.username,
            password=self.cleaned_data['password'])

    def authenticate_via_email(self):
        email = self.cleaned_data['email']
        if email:
            try:
                user = User.objects.get(email__iexact=email)
                if user.check_password(self.cleaned_data['password']):
                    return user
            except ObjectDoesNotExist:
                pass
        return None
