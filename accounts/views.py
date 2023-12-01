from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from accounts.models import User
from hospitals.models import Review
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import auth


@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    reviews = Review.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'accounts/user_detail.html', {'user': user, 'reviews': reviews})


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

@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user)  # 현재 로그인한 사용자가 작성한 후기 가져오기
    return render(request, 'accounts/user_reviews.html', {'reviews': reviews})


def SignupPage(request):
    if request.method == 'POST':
        form_class = SignupForm(request.POST)
        email=request.POST.get('email') + '@duksung.ac.kr'
        date_of_birth=request.POST.get('date_of_birth')
        if date_of_birth == '':
            date_of_birth = None

        user = User.objects.create_user(
            email=email,
            password=request.POST.get('password'),
            nickname=request.POST.get('nickname'),
            username=request.POST.get('username'),
            date_of_birth=date_of_birth,
            phone=request.POST.get('phone'),
            profileImg=request.FILES.get('profileImg'),
        )
        login(request, user)

        return redirect('/main_page1/')
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
            return HttpResponseRedirect('/accounts/login')

    return render(request, 'accounts/login.html',{'form': form})

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/main_page1')
    return render(request, 'accounts/login.html')
