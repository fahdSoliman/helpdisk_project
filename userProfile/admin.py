from django.contrib import admin
from .models import Profile, CompanyProfile, TechnicalResponse, FinanicalResponse


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'facebook', 'telegram', 'botpress']
    list_filter = ['user', 'facebook', 'telegram']
    search_fields = ['user', 'facebook', 'telegram']
    class Meta:
        model = Profile

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['user', 'customer_type', 'country', 'email']
    class Meta:
        model = CompanyProfile

class TechAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'email']
    class Meta:
        model = TechnicalResponse

class FinAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone','email']
    class Meta:
        model = FinanicalResponse

admin.site.register(Profile, ProfileAdmin)
admin.site.register(CompanyProfile, CompanyAdmin)
admin.site.register(TechnicalResponse, TechAdmin)
admin.site.register(FinanicalResponse, FinAdmin)