from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login
from django.views.generic import FormView


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
        return redirect('/')
    return render(request, 'accounts/signup.html')


# @method_decorator(logout_message_required, name='dispatch')
class LoginPage(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = '/'

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
