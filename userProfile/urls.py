from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', user_views.profile, name= 'account'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='profile/login.html'), name='login' ),
    path('logout/', auth_views.LogoutView.as_view(template_name='profile/logout.html'), name='logout'),
    path('settings/', user_views.settings, name= 'settings'),
    path('profile/', user_views.profile, name='profile'),
    path('myproducts/', user_views.myproduct, name='myproducts'),
    path('update/resdomain/<int:id>', user_views.resdomain_update, name='resdomain_update'),
    path('update/hostdomain/<int:id>', user_views.hostdomain_update, name='hostdomain_update'),
    path('update/shared/<int:id>', user_views.shared_update, name='shared_update'),
    path('update/vps/<int:id>', user_views.vps_update, name='vps_update'),

]
