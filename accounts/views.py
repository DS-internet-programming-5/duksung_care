from django.shortcuts import render, redirect
from accounts.models import User
from django.contrib import auth

def SignupPage(request):
    form_class=SignupPage
    if request.method == 'POST':
        user = User.objects.create_user(
            email=request.POST.get('email'),
            password=request.POST.get('password'),
            nickname=request.POST.get('nickname'),
            username=request.POST.get('username'),
            date_of_birth=request.POST.get('date_of_birth'),
            phone=request.POST.get('phone'),
            profileImg=request.FILES.get('profileImg'),
        )
        auth.login(request, user)
        return redirect('/')
    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': '이메일 또는 비밀번호가 틀렸습니다.'})
    else:
        return render(request, 'login.html')