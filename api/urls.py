from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('auth/', obtain_auth_token), # authentication view to get a token
    
    path('product/<str:type_name>', views.Type_list_view), # product list view api
    path('product/', views.Type_list_view), # product list view api


    ## user general profile api
    path('user/<int:id>/', views.User_Retrieve_View),
    path('user/username/<str:username>', views.User_Retrieve_View2),
    path('user/<int:id>/reservations/', views.User_Reservations_Retrieve_View),
    path('user/botpress/<str:botpress>', views.User_Botpress_Retrieve_View),
    path('user/telegram/<str:telegram>', views.User_Telegram_View),

    ## user profiles retrieve/update APIs
    path('user/<int:user>/profile/', views.Use_Profile_View), 
    path('user/<int:user>/company/', views.User_CompanyProfile_View), 
    path('user/<int:user>/finanical/', views.User_FinanicalResponse_View), 
    path('user/<int:user>/technical/', views.User_TechResponse_View),

    ## product reservation api
    path('product/resdomain/<str:id>/', views.ResDomain_Retrieve_Update_API), # retreive/update
    path('product/resdomain/', views.ResDomain_Retrieve_Update_API), # create
    
    path('product/hostdomain/<int:id>/', views.HostDomain_Retrieve_Update_API), # retreive/update
    path('product/hostdomain/',views.HostDomain_Retrieve_Update_API), # create

    path('product/shared/<int:id>/', views.Shared_Retrieve_Update_API),  # retreive/update
    path('product/shared/', views.Shared_Retrieve_Update_API),  # create

    path('product/vps/<int:id>/', views.VPS_Retrieve_Update_API),  # retreive/update
    path('product/vps/', views.VPS_Retrieve_Update_API), # create


    ## QA update question score
    path('qa/update/', views.HostDomain_Retrieve_Update_API),
]



'''
explainations of api URLs

1- view for read only all types with related products grouped at one # done

2- view for read only logined user with all related profile objects and signed products

3- update user profiles objects 'company, tech response, fin response, profile'.

4- update/post resdomain

5- update/post hostdomain

6- update/post shared hosting

7- update/post vps hosting
'''