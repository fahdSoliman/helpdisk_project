from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import Profile, CompanyProfile, FinanicalResponse, TechnicalResponse
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
        fields = ['image','fbName','telegram','gender']


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