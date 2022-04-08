from django.contrib import admin
from .models import Profile, CompanyProfile, TechnicalResponse, FinanicalResponse


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['fbName', 'telegram']
    list_filter = ['fbName', 'telegram']
    search_fields = ['fbName', 'telegram']
    class Meta:
        model = Profile


admin.site.register(Profile, ProfileAdmin)
admin.site.register(CompanyProfile)
admin.site.register(TechnicalResponse)
admin.site.register(FinanicalResponse)