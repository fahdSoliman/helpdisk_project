from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.view_request , name='view_request'),
    path('admin/settings/', views.admin_settings, name='admin_settings'),
    path('admin/botpress/', views.admin_botpress_accounts, name='admin_botpress'),
]