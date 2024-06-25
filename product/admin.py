from typing import Any
from django.contrib import admin
from .models import Product, Type, HostDomain, ResDomain, SharedHosting, VPS
from .forms import SharedHostingForm
from django.contrib.auth.models import User

# customize admin panel

class ProductAdmin(admin.ModelAdmin):
    list_display= ("product_name", "product_type","pub_date","updated")
    list_filter = ["product_name", "product_type"]
    search_fields = ["product_name", "product_type"]
    
    class Meta:
        model=Product

class ResDomainAdmin(admin.ModelAdmin):
    list_display= ("domain_name", "hosting_company","reg_date","updated")
    list_filter = ["domain_name", "hosting_company"]
    search_fields = ["domain_name", "hosting_company"]

    class Meta:
        model=ResDomain
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "my_product":
            # print(db_field.clean)
            kwargs["queryset"] = Product.objects.filter(product_type=2)
        return super(ResDomainAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class HostDomainAdmin(admin.ModelAdmin):
    list_display= ("domain_name", "ip_address","reg_date","updated")
    list_filter = ["domain_name", "ip_address"]
    search_fields = ["domain_name", "ip_address"]

    class Meta:
        model=HostDomain

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "my_product":
            # print(db_field.clean)
            kwargs["queryset"] = Product.objects.filter(product_type=1)
        return super(HostDomainAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class SharedAdmin(admin.ModelAdmin):
    list_display= ("website_name", "operation","reg_date","updated")
    list_filter = ["website_name", "operation"]
    search_fields = ["website_name", "operation"]

    class Meta:
        model=SharedHosting
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "my_product":
            # print(db_field.clean)
            kwargs["queryset"] = Product.objects.filter(product_type=3)
        return super(SharedAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class VPSAdmin(admin.ModelAdmin):
    list_display= ("website_name", "operation_system","reg_date","updated")
    list_filter = ["website_name", "operation_system"]
    search_fields = ["website_name", "operation_system"]

    class Meta:
        model=VPS
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "my_product":
            # print(db_field.clean)
            kwargs["queryset"] = Product.objects.filter(product_type=4)
        return super(VPSAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(Type)
admin.site.register(Product, ProductAdmin)
admin.site.register(HostDomain, HostDomainAdmin)
admin.site.register(ResDomain, ResDomainAdmin)
admin.site.register(SharedHosting, SharedAdmin)
admin.site.register(VPS, VPSAdmin)
# Register your models here.

