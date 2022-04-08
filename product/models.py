from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date
from django.utils.timezone import now
from djmoney.models.fields import MoneyField


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
    product_description = models.TextField()
    product_file = models.FileField(upload_to='product_files/', null=True)
    year_fees = MoneyField(max_digits=14, decimal_places=2, default_currency='SYP')

    def __str__(self):
        return str(self.product_name)


class HostDomain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    my_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    domain_name = models.URLField()
    ip_address = models.GenericIPAddressField()
    reg_date = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    is_valid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField(null=True)
    expire_date = models.DateField(null=True)
    note = models.TextField(null=True)
    bill_file = models.ImageField(upload_to='bill_files_hostdomain/' , null=True)

    def __str__(self):
        return str(self.user.username + " / " + self.domain_name)

class ResDomain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    my_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    domain_name = models.URLField()
    activate = models.BooleanField()
    primary_name_server = models.CharField(max_length=255)
    secondary_name_server = models.CharField(max_length=255)
    reg_date = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    is_valid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True)
    expire_date = models.DateField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    bill_file = models.ImageField(upload_to='bill_files_resdomain/', null=True)

    def __str__(self):
        return str(self.user.username + " / " + self.domain_name)

class SharedHosting(models.Model):
    operation_windows = 0
    operation_linux = 1
    operation_choice = [(operation_windows, 'windows'), (operation_linux, 'linux')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    my_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    website_name = models.CharField(max_length=255)
    operation = models.IntegerField(choices=operation_choice, null=True)
    transfer_website = models.BooleanField()
    backup_website = models.BooleanField()
    reg_date = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    is_valid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField(null=True)
    expire_date = models.DateField(null=True)
    note = models.TextField(null=True)
    bill_file = models.ImageField(upload_to='bill_files_sharedhosting/', null=True)

    def __str__(self):
        return str(self.user.username + " / " + self.website_name)


class VPS(models.Model):


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    my_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    website_name = models.CharField(max_length=255)
    operation_system = models.CharField(max_length=255)
    ip_address = models.BooleanField()
    ip_count = models.IntegerField()
    port_numbers = models.CharField(max_length=255)
    data_transfer = models.BooleanField()
    data_backup = models.BooleanField()

    reg_date = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    is_valid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField(null=True)
    expire_date = models.DateField(null=True)
    note = models.TextField(null=True)
    bill_file = models.ImageField(upload_to='bill_files_VBShosting/', null=True)

    def __str__(self):
        return str(self.user.username + " / " + self.my_product.product_name)
    