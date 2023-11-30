from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from accounts.models import User
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import auth


@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'accounts/user_detail.html', {'user': user})


@login_required
def modify(request):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.user.pk)
        default_profile_image = request.POST.get('default_profile_image')
        if default_profile_image == 'default':
            if user.profileImg:
                user.profileImg.delete()  # 이 부분 추가
            user.profileImg = None
        else:
            user.profileImg = request.FILES.get('profile_image', user.profileImg)
        user.nickname = request.POST.get('nickname')
        user.date_of_birth = request.POST.get('date_of_birth')
        user.phone = request.POST.get('phone')
        user.save()
        return redirect('accounts-user', pk=user.pk)
    else:
        return render(request, 'accounts/modify.html')

@login_required
def user_delete(request):
    user = get_object_or_404(User, pk=request.user.pk)
    user.delete()
    messages.success(request, '회원 탈퇴가 완료되었습니다.')
    return redirect('/main_page1/')

def SignupPage(request):
    if request.method == 'POST':
        form_class = SignupForm(request.POST)
        user = User.objects.create_user(
            email=request.POST.get('email'),
            password=request.POST.get('password'),
            nickname=request.POST.get('nickname'),
            username=request.POST.get('username'),
            date_of_birth=request.POST.get('date_of_birth'),
            phone=request.POST.get('phone'),
            profileImg=request.FILES.get('profileImg'),
        )
        login(request, user)
        return redirect('/main_page1')
    return render(request, 'accounts/signup.html')

def LoginPage(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/main_page1')
        else:
            messages.error(request, '이메일이 존재하지 않거나 비밀번호가 틀렸습니다.')

    return render(request, 'accounts/login.html',{'form': form})

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/main_page1')
    return render(request, 'accounts/login.html')
