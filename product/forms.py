from django import forms
from .models import  SharedHosting, ResDomain, VPS, HostDomain



class HostDomainForm(forms.ModelForm):
    bill_file = forms.FileField(required=False)

    class Meta:
        model = HostDomain
        fields = [
            'my_product',
            'user',
            'domain_name',
            'ip_address',
            'bill_file',
            'note'
        ]
    def clean_domain_name(self,*args, **kwargs):
        webname = self.cleaned_data.get("domain_name")
        vps = HostDomain.objects.filter(domain_name=webname).count()
        if vps>0:
            raise forms.ValidationError(f"النطاق {webname} الذي أدخلته محجوز مسبقاً، يرجى استخدام نطاق آخر.")
        return webname

class ResDomainForm(forms.ModelForm):
    bill_file = forms.FileField(required=False)
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
            'bill_file',
            'note'
        ]
    def clean_domain_name(self,*args, **kwargs):
        webname = self.cleaned_data.get("domain_name")
        vps = ResDomain.objects.filter(domain_name=webname).count()
        if vps>0:
            raise forms.ValidationError(f"النطاق {webname} الذي أدخلته محجوز مسبقاً، يرجى استخدام نطاق آخر.")
        return webname

    def clean_bill_file(self):
        return self.cleaned_data['bill_file'] or None

class SharedHostingForm(forms.ModelForm):
    bill_file = forms.FileField(required=False)

    class Meta:
        model = SharedHosting
        fields = [
            'my_product',
            'user',
            'website_name', 
            'operation', 
            'transfer_website', 
            'backup_website', 
            'bill_file',
            'note'
        ]
    
    
    def clean_website_name(self,*args, **kwargs):
        webname = self.cleaned_data.get("website_name")
        vps = SharedHosting.objects.filter(website_name=webname).count()
        if vps>0:
            raise forms.ValidationError(f"اسم الموقع {webname} الذي أدخلته محجوز مسبقاً، يرجى استخدام اسم آخر.")
        return webname
    def clean_bill_file(self):
        return self.cleaned_data['bill_file'] or None

class VPSForm(forms.ModelForm):
    bill_file = forms.FileField(required=False)

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
            'bill_file',
            'note'
        ]
    def clean_website_name(self,*args, **kwargs):
        webname = self.cleaned_data.get("website_name")
        vps = VPS.objects.filter(website_name=webname).count()
        if vps>0:
            raise forms.ValidationError(f"اسم الموقع {webname} الذي أدخلته محجوز مسبقاً، يرجى استخدام اسم آخر")
        return webname
    def clean_bill_file(self):
        return self.cleaned_data['bill_file'] or None
