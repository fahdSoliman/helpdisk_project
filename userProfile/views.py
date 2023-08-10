from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .forms import (UserRegisterForm, 
                    UserUpdateForm, 
                    ProfileUpdateForm, 
                    CompanyUpdateForm, 
                    TechUpdateForm, 
                    FinUpdateForm)
from django.contrib import messages
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from product.models import HostDomain,ResDomain,SharedHosting,VPS
from .forms import ResDomainForm, HostDomainForm, SharedHostingForm, VPSForm

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'أهلاً بك يا {username} تم انشاء حسابك بنجاح!')
            id = request.POST.get('botpressID')
            botpressIdUpdate(id, username)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'profile/register.html',{'form' : form})

def botpressIdUpdate(id, username):
    ## some new code tomorrow
    user = User.objects.get(username=username)
    print(user.id)
    prof = Profile.objects.filter(user=user.id).update(botpress=id)
    return


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
            profile_form.instance.is_complete = True
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

## update subsecriptions 

@login_required(login_url='login')
def resdomain_update(request, id):
    user = request.user.username
    service = get_object_or_404(ResDomain, id = id)
    print(user, service.user.username)
    if user == service.user.username:
        if request.method == "POST":
            resdomain_form = ResDomainForm(request.POST, request.FILES, instance=service)
            if resdomain_form.is_valid():
                service.is_valid = False
                date = datetime.now().strftime('%Y/%m/%d - %H:%M')
                note = service.note
                print(note)
                service.note = str(f"<p> تم تعديل الطلب من قبل الزبون بتاريخ {date} </p>") + note
                resdomain_form.save()
                messages.success(request, f'تم تعديل الخدمة')
                return redirect('myproducts')
        else:
            resdomain_form = ResDomainForm(instance=service)
        context = {
            'detail': service,
            'resdomain_form': resdomain_form,
        }
        return render(request, 'profile/resdomain_update.html', context)
    else:
        messages.error(request, f'الصفحة المطلوبة غير موجودة')
        return redirect('myproducts')
     

@login_required(login_url='login')
def hostdomain_update(request, id):
    user = request.user.username
    service = get_object_or_404(HostDomain, id = id)
    if user == service.user.username:
        if request.method == "POST":
            hostdomain_form = HostDomainForm(request.POST, request.FILES, instance=service)
            if hostdomain_form.is_valid():
                service.is_valid = False
                date = datetime.now().strftime('%Y/%m/%d - %H:%M')
                note = service.note
                service.note = str(f"<p> تم تعديل الطلب من قبل الزبون بتاريخ {date} </p>") + note
                hostdomain_form.save()
                messages.success(request, f'تم تعديل الخدمة بنجاح')
                return redirect('myproducts')
        else:
            hostdomain_form = HostDomainForm(instance=service)
        context = {
            'detail': service,
            'hostdomain_form': hostdomain_form,
        }
        return render(request, 'profile/hostdomain_update.html', context)
    else:
        messages.error(request, f'الصفحة المطلوبة غير موجودة')
        return redirect('myproducts')



@login_required(login_url='login')
def shared_update(request, id):
    user = request.user.username
    service = get_object_or_404(SharedHosting, id = id)
    if user == service.user.username:
        if request.method == "POST":
            shared_form = SharedHostingForm(request.POST, request.FILES, instance=service)
            if shared_form.is_valid():
                shared_form.save()
                messages.success(request, f'تم تعديل الخدمة بنجاح')
                return redirect('myproducts')
        else:
            shared_form = SharedHostingForm(instance=service)
        context = {
            'detail': service,
            'shared_form': shared_form,
        }
        return render(request, 'profile/shared_update.html', context)
    else:
        messages.error(request, f'الصفحة المطلوبة غير موجودة')
        return redirect('myproducts')


@login_required(login_url='login')
def vps_update(request, id):
    user = request.user.username
    service = get_object_or_404(VPS, id = id)
    if user == service.user.username:
        if request.method == "POST":
            vps_form = VPSForm(request.POST, request.FILES, instance=service)
            if vps_form.is_valid():
                vps_form.save()
                messages.success(request, f'تم تعديل الخدمة بنجاح')
                return redirect('myproducts')
        else:
            vps_form = VPSForm(instance=service)
        context = {
            'detail': service,
            'vps_form': vps_form,
        }
        return render(request, 'profile/vps_update.html', context)
    else:
        messages.error(request, f'الصفحة المطلوبة غير موجودة')
        return redirect('myproducts')