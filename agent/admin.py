from django.contrib import admin
from .models import Botpress
# Register your models here.
class BotpressAdmin(admin.ModelAdmin):

    class Meta:
        model = Botpress


admin.site.register(Botpress)