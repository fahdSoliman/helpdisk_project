from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.view_request , name='view_request'),
    path('resdomain/<int:id>/', views.agent_process_resdomain, name='agent_process_resdomain'),
    path('hostdomain/<int:id>/', views.agent_process_hostdomain, name='agent_process_hostdomain'),
    path('shared/<int:id>/', views.agent_process_shared, name='agent_process_shared'),
    path('vps/<int:id>/', views.agent_process_vps, name='agent_process_vps'),
    path('settings/', views.agent_settings, name='agent_settings'),
    path('botpress/', views.agent_botpress_accounts, name='agent_botpress'),
]