from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.view_new_request , name='view_new_request'),
    path('old-request/', views.view_old_request ,name='view_old_request'),
    path('resdomain/<int:id>/', views.agent_process_resdomain, name='agent_process_resdomain'),
    path('hostdomain/<int:id>/', views.agent_process_hostdomain, name='agent_process_hostdomain'),
    path('shared/<int:id>/', views.agent_process_shared, name='agent_process_shared'),
    path('vps/<int:id>/', views.agent_process_vps, name='agent_process_vps'),
    path('botpress/HITL/', views.agent_botpress_hitl, name='botpress_hitl'),
    path('botpress/', views.admin_botpress, name='agent_botpress'),
    path('botpress/init/', views.admin_botpress_init, name='agent_botpress_init'),
    path('botpress/add/', views.admin_botpress_create_user, name='agent_botpress_add'),
    path('botpress/del/<str:email>/', views.admin_botpress_del_user, name="agent_botpress_del")
]