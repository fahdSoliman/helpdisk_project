from pyexpat import model
from django import forms
from product.models import ResDomain, HostDomain, SharedHosting, VPS

class Resdomain_Form(forms.ModelForm):
    class Meta:
        model = ResDomain
        fields = [
            'domain_name',
            'activate',
            'primary_name_server',
            'secondary_name_server',
            'hosting_company',
            'is_valid',
            'is_active',
            'start_date',
            'expire_date',
            'note',
            'bill_file'
        ]
        exclude = [
            'user',
            'my_product'
        ]

class Hostdomain_Form(forms.ModelForm):
    class Meta:
        model = HostDomain
        fields = [
            'domain_name',
            'ip_address',
            'is_valid',
            'is_active',
            'start_date',
            'expire_date',
            'note',
            'bill_file'
        ]
        exclude = [
            'user',
            'my_product'
        ]


class Shared_Form(forms.ModelForm):
    class Meta:
        model = SharedHosting
        fields = [
            'website_name',
            'operation',
            'transfer_website',
            'backup_website',
            'is_valid',
            'is_active',
            'start_date',
            'expire_date',
            'note',
            'bill_file'
        ]


class Vps_Form(forms.ModelForm):
    class Meta:
        model = SharedHosting
        fields = [
            'website_name',
            'operation',
            'transfer_website',
            'backup_website',
            'is_valid',
            'is_active',
            'start_date',
            'expire_date',
            'note',
            'bill_file'
        ]

