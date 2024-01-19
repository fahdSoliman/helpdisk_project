from django.contrib import admin
from .models import  DataURL, Passage
# Register your models here.

# class KnowledgeAdmin(admin.ModelAdmin):
#     list_display=("data", "pub_date","updated")
#     class Meta:
#         model = KnowledgeBase

class DataAdmin(admin.ModelAdmin):
    list_display=("title" ,"data_type","url", "pub_date","updated")
    class Meta:
        model = DataURL

class PassagesAdmin(admin.ModelAdmin):
    list_display=("knowledge", "translated", "pub_date", "updated")
    class Meta:
        model = Passage

# admin.site.register(KnowledgeBase, KnowledgeAdmin)
admin.site.register(DataURL, DataAdmin)
admin.site.register(Passage,PassagesAdmin)
