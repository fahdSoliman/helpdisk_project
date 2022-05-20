from django.shortcuts import render, get_object_or_404, redirect
from .models import Type, Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from product.models import Product, HostDomain, ResDomain, SharedHosting, VPS
from django.contrib import messages
from .forms import HostDomainForm, ResDomainForm, SharedHostingForm, VPSForm

def product_home(request):
    
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    detail = get_object_or_404(Product, pk=product_id)
    context ={
        'detail': detail,
    }
    return render(request, 'products/details_product.html', context)



@login_required(login_url='login')
def add_product(request,id):

    prod = get_object_or_404(Product, pk=id)
    print(prod.product_type.type_name)
    type_name = prod.product_type.type_name
    if type_name == "حجز نطاق":
        return add_RegDomain(request, prod)
    elif type_name == "استضافة مشتركة":
        return add_SharedHosting(request, prod)
    elif type_name == "استضافة نطاق":
        return add_HostDomain(request, prod)
    elif type_name == "استضافة مستقلة افتراضية":
        return add_VPS(request, prod)




def add_RegDomain(request, prod):
    product = prod.product_type.type_name + " / " + prod.product_name
    if request.method == "POST":
        print("POST")
        updated_request = request.POST.copy()
        updated_request.update({'user': request.user.id, 'my_product': prod.id})
        resdomain_form = ResDomainForm(updated_request, request.FILES)
        if resdomain_form.is_valid():
            print("sucsses")
            resdomain_form.save()
            messages.success(request, f'تم التسجيل في الخدمة {product} بنجاح')
            return redirect('home')
    else:
        print("GET")
        resdomain_form = ResDomainForm()

    context = {
        'resdomain_form': resdomain_form,
        'product': product
    }
    return render(request, 'products/resdomain.html', context)


def add_HostDomain(request, prod):
    product = prod.product_type.type_name + " / " + prod.product_name
    if request.method == "POST":
        updated_request = request.POST.copy()
        updated_request.update({'user': request.user.id, 'my_product':prod.id})
        hostdomain_form = HostDomainForm(updated_request, request.FILES)
        if hostdomain_form.is_valid():
            hostdomain_form.save()
            messages.success(request, f'تم التسجيل  في الخدمة بنجاح')
            return redirect('home')
    else:
        hostdomain_form = HostDomainForm()
    
    context = {
        'hostdomain_form': hostdomain_form,
        'product': product
    }
    return render(request, 'products/hostdomain.html', context)


def add_SharedHosting(request, prod):
    product = prod.product_type.type_name + " / " + prod.product_name
    if request.method == "POST":
        updated_request = request.POST.copy()
        updated_request.update({'user': request.user.id, 'my_product':prod.id})
        sharedhosting_form = SharedHostingForm(updated_request, request.FILES)
        if sharedhosting_form.is_valid():
            sharedhosting_form.save()
            messages.success(request, f'تم التسجيل  في الخدمة بنجاح')
            return redirect('home')
    else:
        sharedhosting_form = SharedHostingForm()
    
    context = {
        'sharedhosting_form': sharedhosting_form,
        'product': product
    }
    return render(request, 'products/sharedhosting.html', context)


def add_VPS(request, prod):
    product = prod.product_type.type_name + " / " + prod.product_name
    if request.method == "POST":
        updated_request = request.POST.copy()
        updated_request.update({'user': request.user.id, 'my_product':prod.id})
        vps_form = VPSForm(updated_request, request.FILES)
        if vps_form.is_valid():
            vps_form.save()
            messages.success(request, f'تم التسجيل  في الخدمة بنجاح')
            return redirect('home')
    else:
        vps_form = VPSForm()
    
    context = {
        'vps_form': vps_form,
        'product': product
    }
    return render(request, 'products/vps.html', context)

