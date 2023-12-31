from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from accounts.models import User
from hospitals.models import Review
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
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
                user.profileImg.delete()
            user.profileImg = None
        else:
            user.profileImg = request.FILES.get('profile_image', user.profileImg)

        new_nickname = request.POST.get('nickname')
        existing_user = User.objects.filter(nickname=new_nickname).exclude(pk=user.pk).first()
        if existing_user:
            messages.error(request, '이미 존재하는 닉네임입니다.')
            return render(request, 'accounts/modify.html')

        user.nickname = new_nickname
        user.date_of_birth = request.POST.get('date_of_birth')
        user.phone = request.POST.get('phone')

        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        if password and new_password:
            if user.check_password(password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user) # 로그인 유지
            else:
                messages.error(request, '기존 비밀번호와 일치하지 않습니다.')
                return render(request, 'accounts/modify.html')

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
    form_class = SignupForm(request.POST)
    if request.method == 'POST':
        # email=request.POST.get('email') + '@duksung.ac.kr'
        date_of_birth=request.POST.get('date_of_birth')
        if date_of_birth == '':
            date_of_birth = None
        if form_class.is_valid():
            user = User.objects.create_user(
                email=request.POST.get('email'),
                password=request.POST.get('password'),
                nickname=request.POST.get('nickname'),
                username=request.POST.get('username'),
                date_of_birth=date_of_birth,
                phone=request.POST.get('phone'),
                profileImg=request.FILES.get('profileImg'),
            )
            login(request, user)

            return redirect('/main_page1/')
    else:
        form_class = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form_class})

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
