from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

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
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                self.add_error('email', '이메일이 존재하지 않습니다.')
                return

            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')
