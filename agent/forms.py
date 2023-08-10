from pyexpat import model
from django import forms
from product.models import ResDomain, HostDomain, SharedHosting, VPS
from .models import Botpress



class Resdomain_Form(forms.ModelForm):
    class Meta:
        model = ResDomain
        fields = [
            'is_valid',
            'is_active',
            'start_date',
            'expire_date',
            'note',
        ]
        exclude = [
            'user',
            'my_product',
            'domain_name',
            'activate',
            'primary_name_server',
            'secondary_name_server',
            'hosting_company',
            'bill_file',
        ]

class Hostdomain_Form(forms.ModelForm):
    class Meta:
        model = HostDomain
        fields = [
            'is_valid',
            'is_active',
            'start_date',
            'expire_date',
            'note',
        ]
        exclude = [
            'user',
            'my_product',
            'domain_name',
            'ip_address',
            'bill_file',
        ]


class Shared_Form(forms.ModelForm):
    class Meta:
        model = SharedHosting
        fields = [
            'is_valid',
            'is_active',
            'start_date',
            'expire_date',
            'note',
        ]
        exclode = [
            'user',
            'my_product',
            'website_name',
            'operation',
            'transfer_website',
            'backup_website',
            'bill_file'
        ]

class Vps_Form(forms.ModelForm):
    class Meta:
        model = SharedHosting
        fields = [
            'is_valid',
            'is_active',
            'start_date',
            'expire_date',
            'note',
        ]
        exclode = [
            'user',
            'my_product',
            'website_name',
            'operation_system',
            'ip_address',
            'ip_count',
            'port_numbers',
            'data_transfer',
            'data_backup',
            'bill_file'
        ]



class Botpress_form(forms.ModelForm):
    class Meta:
        model = Botpress
        fields = [
            'botpress_base_url',
            'db_url',
            'db_type',
            'db_name',
            'db_username',
            'db_password'
        ]


class Botpress_user(forms.Form):
    email = forms.EmailField()
    role = forms.CharField()