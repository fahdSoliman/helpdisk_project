from django import forms
from django.contrib.auth.models import User
from .models import Type, Product, SharedHosting, ResDomain, VPS, HostDomain




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

class ResDomainForm(forms.ModelForm):

    class Meta:
        model = ResDomain
        fields = [
            'my_product',
            'user',
            'domain_name',
            'activate',
            'primary_name_server',
            'secondary_name_server',
            'bill_file'
        ]

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