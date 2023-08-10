from email.policy import default
from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date
from django.utils.timezone import now
from djmoney.models.fields import MoneyField
from ckeditor.fields import RichTextField
from django.utils.html import strip_tags

class Type(models.Model):
    type_name = models.CharField(max_length=255)
    des_file = models.FileField(upload_to='type_files/', null=True)

    def __str__(self):
        return str(self.type_name)


class Product(models.Model):
    product_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_img = models.ImageField(default='default.png' ,upload_to='product_img/')
    pub_date = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    product_description = RichTextField(null=True)
    product_specification = RichTextField(null=True)
    product_file = models.FileField(upload_to='product_files/', null=True)
    year_fees = MoneyField(max_digits=14, decimal_places=2, default_currency='SYP')

    def __str__(self):
        return str(self.product_name)


    def pretty_pub_date(self):
        return self.pub_date.strftime('%b %Y')
        
    def get_description_clean(self):
        return strip_tags(str(self.product_description))
    
    def get_specification_clean(self):
        return strip_tags(str(self.product_specification))

## product related to user classes

class HostDomain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    my_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    domain_name = models.URLField(unique=True)
    ip_address = models.GenericIPAddressField(null=True)

    reg_date = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    is_valid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField(default=date.today())
    expire_date = models.DateField(default=(date.today() + relativedelta(years=1)))
    note = RichTextField(null=True, default="")
    bill_file = models.ImageField(upload_to='bill_files_hostdomain/' , null=True)

    def __str__(self):
        return str(self.domain_name)

    def pretty_reg_date(self):
        return self.reg_date.strftime('%Y/%m/%d - %H:%M')

    def pretty_updated(self):
        return self.updated.strftime('%Y/%m/%d - %H:%M')

    def pretty_start_date(self):
        return self.start_date.strftime('%Y/%m/%d')

    def pretty_expire_date(self):
        return self.expire_date.strftime('%Y/%m/%d')


class ResDomain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    my_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    domain_name = models.URLField(unique=True)
    activate = models.BooleanField(default=True)
    primary_name_server = models.CharField(max_length=255, null=True)
    secondary_name_server = models.CharField(max_length=255,null=True)
    hosting_company = models.CharField(max_length=255,null=True)

    reg_date = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    is_valid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField(default=date.today())
    expire_date = models.DateField(default=(date.today() + relativedelta(years=1)))
    note = RichTextField(null=True, default="")
    bill_file = models.ImageField(upload_to='bill_files_resdomain/', null=True)

    def __str__(self):
        return str(self.domain_name)

    def pretty_reg_date(self):
        return self.reg_date.strftime('%Y/%m/%d - %H:%M')

    def pretty_updated(self):
        return self.updated.strftime('%Y/%m/%d - %H:%M')

    def pretty_start_date(self):
        return self.start_date.strftime('%Y/%m/%d')

    def pretty_expire_date(self):
        return self.expire_date.strftime('%Y/%m/%d')
    
    def get_note_clean(self):
        return strip_tags(self.note)


class SharedHosting(models.Model):
    operation_windows = 0
    operation_linux = 1
    operation_choice = [(operation_windows, 'windows'), (operation_linux, 'linux')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    my_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    website_name = models.CharField(unique=True,max_length=255)
    operation = models.IntegerField(choices=operation_choice, null=True)
    transfer_website = models.BooleanField(default=False)
    backup_website = models.BooleanField(default=False)
    
    reg_date = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    is_valid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField(default=date.today())
    expire_date = models.DateField(default=(date.today() + relativedelta(years=1)))
    note = RichTextField(null=True, default="")
    bill_file = models.ImageField(upload_to='bill_files_sharedhosting/', null=True)

    def __str__(self):
        return str(self.website_name)
    
    def pretty_reg_date(self):
        return self.reg_date.strftime('%Y/%m/%d - %H:%M')

    def pretty_updated(self):
        return self.updated.strftime('%Y/%m/%d - %H:%M')

    def pretty_start_date(self):
        return self.start_date.strftime('%Y/%m/%d')

    def pretty_expire_date(self):
        return self.expire_date.strftime('%Y/%m/%d')

    
    def get_operation(self):
        t = self.operation_choice[self.operation] # type: ignore
        return str(t[1])


class VPS(models.Model):
    operation_windows = 0
    operation_linux = 1
    operation_choice = [(operation_windows, 'windows'), (operation_linux, 'linux')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    my_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    website_name = models.CharField(unique=True,max_length=255)
    operation_system = models.IntegerField(choices=operation_choice, null=True)
    ip_address = models.GenericIPAddressField(null=True)
    ip_count = models.IntegerField(null=True)
    port_numbers = models.CharField(max_length=255)
    data_transfer = models.BooleanField(default=False)
    data_backup = models.BooleanField(default=False)

    reg_date = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    is_valid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField(default=date.today())
    expire_date = models.DateField(default=(date.today() + relativedelta(years=1)))
    note = RichTextField(null=True, default="")
    bill_file = models.ImageField(upload_to='bill_files_VBShosting/', null=True)

    def __str__(self):
        return str(self.website_name)
    
    def pretty_reg_date(self):
        return self.reg_date.strftime('%Y/%m/%d - %H:%M')

    def pretty_updated(self):
        return self.updated.strftime('%Y/%m/%d - %H:%M')

    def pretty_start_date(self):
        return self.start_date.strftime('%Y/%m/%d')

    def pretty_expire_date(self):
        return self.expire_date.strftime('%Y/%m/%d')

    
    def get_operation(self):
        t = self.operation_choice[self.operation_system]
        return str(t[1])
    