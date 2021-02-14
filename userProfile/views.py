from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from .models import profile



def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'أهلاً بك يا {username} تم انشاء حسابك بنجاح!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'profile/register.html',{'form' : form})

def account(request):
    if request.user.is_authenticated:
        prof = profile.objects.get(id=request.user.id)
    return render(request, 'profile/account.html',{'profile': prof})