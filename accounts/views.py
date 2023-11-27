from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.contrib import auth

@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'accounts/user_detail.html', {'user': user})

@login_required
def modify(request):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.user.pk)
        user.email = request.POST.get('email')
        user.nickname = request.POST.get('nickname')
        user.username = request.POST.get('username')
        user.date_of_birth = request.POST.get('date_of_birth')
        user.phone = request.POST.get('phone')
        user.save()
        return redirect('accounts-user', pk=user.pk)
    else:
        return render(request, 'accounts/modify.html')

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
