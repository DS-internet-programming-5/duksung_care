from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User

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