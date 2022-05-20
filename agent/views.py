from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
import sqlite3
from product.models import HostDomain,ResDomain,SharedHosting,VPS
from .forms import Resdomain_Form, Hostdomain_Form,Shared_Form, Vps_Form
# Create your views here.


###################
##  stuff views  ##
###################


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='stuff').exists(), login_url='login')
def view_request(request):
    hostdomain_products = HostDomain.objects.filter(is_active = 0).order_by('-updated')
    resdomain_products = ResDomain.objects.filter(is_active = 0).order_by('-updated')
    shared_products = SharedHosting.objects.filter(is_active = 0).order_by('-updated')
    vps_products = VPS.objects.filter(is_active = 0).order_by('-updated')  
    context = {
        'host_products': hostdomain_products,
        'resdomain_products': resdomain_products,
        'shared_products': shared_products,
        'vps_products': vps_products
    }
    return render(request, 'agent/view_request.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='stuff').exists(), login_url='login')
def agent_process_resdomain(request, id):

    detail = get_object_or_404(ResDomain, id = id)
    print(detail.user)
    customer = User.objects.get(username = detail.user)
    if request.method == 'POST':
        resdomain = Resdomain_Form(request.POST, request.FILES, instance=detail)
        if resdomain.is_valid():
            resdomain.save()
            messages.success(request, f'تم تعديل بيانات الطلب بنجاح')
            return redirect('view_request')
    else:
        resdomain = Resdomain_Form(instance=detail)

    context = {

        'customer': customer,
        'resdomain_form':resdomain,
    }
    return render(request, 'agent/process_resdomain.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='stuff').exists(), login_url='login')
def agent_process_hostdomain(request, id):

    detail = get_object_or_404(HostDomain, id = id)
    print(detail.user)
    customer = User.objects.get(username = detail.user)
    if request.method == 'POST':
        hostdomain = Hostdomain_Form(request.POST, request.FILES, instance=detail)
        if hostdomain.is_valid():
            hostdomain.save()
            messages.success(request, f'تم تعديل بيانات الطلب بنجاح')
            return redirect('view_request')
    else:
        hostdomain = Hostdomain_Form(instance=detail)

    context = {

        'customer': customer,
        'hostdomain_form':hostdomain,
    }
    return render(request, 'agent/process_hostdomain.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='stuff').exists(), login_url='login')
def agent_process_shared(request, id):

    detail = get_object_or_404(SharedHosting, id = id)
    print(detail.user)
    customer = User.objects.get(username = detail.user)
    if request.method == 'POST':
        shared_form = Shared_Form(request.POST, request.FILES, instance=detail)
        if shared_form.is_valid():
            shared_form.save()
            messages.success(request, f'تم تعديل بيانات الطلب بنجاح')
            return redirect('view_request')
    else:
        shared_form = Shared_Form(instance=detail)

    context = {

        'customer': customer,
        'shared_form':shared_form,
    }
    return render(request, 'agent/process_shared.html', context)



@login_required()
@user_passes_test(lambda u: u.groups.filter(name='stuff').exists(), login_url='login')
def agent_process_vps(request, id):

    detail = get_object_or_404(VPS, id = id)
    print(detail.user)
    customer = User.objects.get(username = detail.user)
    if request.method == 'POST':
        vps_form = Vps_Form(request.POST, request.FILES, instance=detail)
        if vps_form.is_valid():
            vps_form.save()
            messages.success(request, f'تم تعديل بيانات الطلب بنجاح')
            return redirect('view_request')
    else:
        vps_form = Shared_Form(instance=detail)

    context = {

        'customer': customer,
        'vps_form':vps_form,
    }
    return render(request, 'agent/process_vps.html', context)




def agent_settings(request):
    # code here

    return render(request, 'agent/agent_settings.html')

# end of Agent Views


######################
##   Admin Views    ##
######################

def agent_botpress_accounts(request):
    con = sqlite3.connect("C:\\botpress\\data\\storage\\core.sqlite")
    cur = con.cursor()
    res = (())
    cur.execute('select * from strategy_default')
    rows = cur.fetchall()
    print(rows)
    
    context = {
        'res': rows,
    }
    return render(request, 'agent/agent_botpress_accounts.html', context)