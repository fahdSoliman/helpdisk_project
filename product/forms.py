from urllib import request
from django import forms
from django.contrib.auth.models import User
from .models import Type, Product, SharedHosting, ResDomain, VPS, HostDomain
from django.contrib import messages



class HostDomainForm(forms.ModelForm):

    class Meta:
        model = HostDomain
        fields = [
            'my_product',
            'user',
            'domain_name',
            'ip_address',
            'bill_file'
        ]
    def clean_domain_name(self,*args, **kwargs):
        webname = self.cleaned_data.get("domain_name")
        vps = HostDomain.objects.filter(domain_name=webname).count()
        print(vps)
        if vps>0:
            raise forms.ValidationError(f"النطاق {webname} الذي أدخلته محجوز مسبقاً، يرجى استخدام نطاق آخر.")
        return webname

class ResDomainForm(forms.ModelForm):
    # bill_file = forms.CharField()
    class Meta:
        model = ResDomain
        fields = [
            'my_product',
            'user',
            'domain_name',
            'activate',
            'primary_name_server',
            'secondary_name_server',
            'hosting_company',
            'bill_file'
        ]
    def clean_domain_name(self,*args, **kwargs):
        webname = self.cleaned_data.get("domain_name")
        vps = ResDomain.objects.filter(domain_name=webname).count()
        print(vps)
        if vps>0:
            raise forms.ValidationError(f"النطاق {webname} الذي أدخلته محجوز مسبقاً، يرجى استخدام نطاق آخر.")
        return webname

class SharedHostingForm(forms.ModelForm):

    class Meta:
        model = SharedHosting
        fields = [
            'my_product',
            'user',
            'website_name', 
            'operation', 
            'transfer_website', 
            'backup_website', 
            'bill_file'
        ]
    def clean_website_name(self,*args, **kwargs):
        webname = self.cleaned_data.get("website_name")
        vps = SharedHosting.objects.filter(website_name=webname).count()
        print(vps)
        if vps>0:
            raise forms.ValidationError(f"اسم الموقع {webname} الذي أدخلته محجوز مسبقاً، يرجى استخدام اسم آخر.")
        return webname

class VPSForm(forms.ModelForm):

    class Meta:
        model = VPS
        fields = [
            'my_product',
            'user',
            'website_name',
            'operation_system',
            'ip_address',
            'ip_count',
            'port_numbers',
            'data_transfer',
            'data_backup',
            'bill_file'
        ]
    def clean_website_name(self,*args, **kwargs):
        webname = self.cleaned_data.get("website_name")
        vps = VPS.objects.filter(website_name=webname).count()
        print(vps)
        if vps>0:
            raise forms.ValidationError(f"اسم الموقع {webname} الذي أدخلته محجوز مسبقاً، يرجى استخدام اسم آخر")
        return webname

