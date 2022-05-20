from django.shortcuts import render, redirect
from .forms import (UserRegisterForm, 
                    UserUpdateForm, 
                    ProfileUpdateForm, 
                    CompanyUpdateForm, 
                    TechUpdateForm, 
                    FinUpdateForm)
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from product.models import HostDomain,ResDomain,SharedHosting,VPS


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


@login_required(login_url='login')
def profile(request):
    user = request.user.id
    prof = User.objects.get(id=user)
    try:
        hostdomain_products = HostDomain.objects.filter(user=user)
    except(HostDomain.DoesNotExist) as e:
        print(e)
    try:
        resdomain_products = ResDomain.objects.filter(user=user)
    except(ResDomain.DoesNotExist) as e:
        print(e)
    try:
        shared_products = SharedHosting.objects.filter(user=user)
    except(SharedHosting.DoesNotExist) as e:
        print(e)
    try:
        vps_products = VPS.objects.filter(user=user)
    except(VPS.DoesNotExist) as e:
        print(e)
    context = {
        'profile': prof,
        'host_products': hostdomain_products,
        'resdomain_products': resdomain_products,
        'shared_products': shared_products,
        'vps_products': vps_products
    }

    return render(request, 'profile/account.html', context)

@login_required(login_url='login')
def settings(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        company_form = CompanyUpdateForm(request.POST, instance=request.user.companyprofile)
        fin_form = FinUpdateForm(request.POST, instance=request.user.finanicalresponse)
        tech_form = TechUpdateForm(request.POST, instance=request.user.technicalresponse)
        if user_form.is_valid() and profile_form.is_valid() and company_form.is_valid() and fin_form.is_valid() and tech_form.is_valid():
            user_form.save()
            profile_form.save()
            company_form.save()
            fin_form.save()
            tech_form.save()
            messages.success(request, f'تم تعديل بيانات الحساب بنجاح')
            return redirect('settings')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        company_form = CompanyUpdateForm(instance=request.user.companyprofile)
        fin_form = FinUpdateForm(instance=request.user.finanicalresponse)
        tech_form = TechUpdateForm(instance=request.user.technicalresponse)

    context = {
        'u_form': user_form,
        'p_form': profile_form,
        'company_form': company_form,
        'fin_form': fin_form,
        'tech_form': tech_form,
    }
    return render(request, 'profile/settings.html', context)


@login_required(login_url='login')
def myproduct(request):
    user = request.user.id
    prof = User.objects.get(id=user)
    try:
        hostdomain_products = HostDomain.objects.filter(user=user)
    except(HostDomain.DoesNotExist) as e:
        print(e)
    try:
        resdomain_products = ResDomain.objects.filter(user=user)
    except(ResDomain.DoesNotExist) as e:
        print(e)
    try:
        shared_products = SharedHosting.objects.filter(user=user)
    except(SharedHosting.DoesNotExist) as e:
        print(e)
    try:
        vps_products = VPS.objects.filter(user=user)
    except(VPS.DoesNotExist) as e:
        print(e)
    context = {
        'profile': prof,
        'host_products': hostdomain_products,
        'resdomain_products': resdomain_products,
        'shared_products': shared_products,
        'vps_products': vps_products
    }
    return render(request, 'profile/my_products.html', context)