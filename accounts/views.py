from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.views.generic import FormView


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


# @method_decorator(logout_message_required, name='dispatch')
class LoginPage(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = '/main_page1'

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            self.request.session['email'] = email
            login(self.request, user)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '이메일 또는 비밀번호가 일치하지 않습니다.')
        return super().form_invalid(form)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/main_page1')
    return render(request, 'accounts/login.html')
