from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import Profile, CompanyProfile, FinanicalResponse, TechnicalResponse
from product.models import ResDomain, HostDomain, SharedHosting, VPS



# User Profile Forms

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','facebook','telegram','gender','is_complete']


class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['customer_name', 'customer_type', 'country', 'phone', 'email']


class FinUpdateForm(forms.ModelForm):
    class Meta:
        model = FinanicalResponse
        fields = ['financial_name', 'phone', 'email']


class TechUpdateForm(forms.ModelForm):
    class Meta:
        model = TechnicalResponse
        fields = ['technical_name', 'phone', 'email']

# User Services Update Forms 

class ResDomainForm(forms.ModelForm):
    class Meta:
        model = ResDomain
        Fields = [
            'domain_name',
            'activate',
            'primary_name_server',
            'secondary_name_server',
            'hosting_company',
            'bill_file',
        ]
        exclude = [
            'user',
            'my_product',
            'is_valid',
            'is_active',
            'start_date',
            'expire_date',
            'note',

        ]

class HostDomainForm(forms.ModelForm):
    class Meta:
        model = HostDomain
        fields = [
            'domain_name',
            'ip_address',
            'bill_file',
        ]
        exclude = [
            'user',
            'my_product',
            'is_valid',
            'is_active',
            'start_date',
            'expire_date',
            'note',
        ]

class SharedHostingForm(forms.ModelForm):
    class Meta:
        model = SharedHosting
        Fields = [
            'website_name',
            'operation',
            'transfer_website',
            'backup_website',
            'bill_file'
        ]
        exclude = [
            'user',
            'my_product',
            'is_valid',
            'is_active',
            'start_date',
            'expire_date',
            'note',
        ]

class VPSForm(forms.ModelForm):
    class Meta:
        model = VPS
        fields = [
            'website_name',
            'operation_system',
            'ip_address',
            'ip_count',
            'port_numbers',
            'data_transfer',
            'data_backup',
            'bill_file'
        ]
        exclude = [
            'user',
            'my_product',
            'is_valid',
            'is_active',
            'start_date',
            'expire_date',
            'note',
        ]