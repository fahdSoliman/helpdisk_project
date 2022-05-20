from django.contrib import admin
from .models import Product, Type, HostDomain, ResDomain, SharedHosting, VPS


# customize admin panel

class ProductAdmin(admin.ModelAdmin):
    list_display= ("product_name", "product_type","pub_date","updated")
    list_filter = ["product_name", "product_type"]
    search_fields = ["product_name", "product_type"]
    
    class Meta:
        model=Product



admin.site.register(Type)
admin.site.register(Product, ProductAdmin)
admin.site.register(HostDomain)
admin.site.register(ResDomain)
admin.site.register(SharedHosting)
admin.site.register(VPS)
# Register your models here.

