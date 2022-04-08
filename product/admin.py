from django.contrib import admin
from .models import Product, Type, HostDomain, ResDomain, SharedHosting, VPS


admin.site.register(Type)
admin.site.register(Product)
admin.site.register(HostDomain)
admin.site.register(ResDomain)
admin.site.register(SharedHosting)
admin.site.register(VPS)
# Register your models here.
