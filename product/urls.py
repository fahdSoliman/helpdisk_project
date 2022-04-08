from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_home, name='product'),
    path('<int:product_id>/', views.product_details, name='detail'),
    path('add/<int:id>/', views.add_product, name='add_product'),
]