from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
    path('user/', user, name='user'),
    path('settings/', accounts_settings, name='settings'),
    path('products/', products, name='products'),
    path('customer/<str:pk>/', customer, name='customer'),
    path('delete_customer/<str:pk>/', delete_customer, name='delete_customer'),
    path('create_order/<str:pk>/', createOrder, name='create_order'),
    path('update_order/<str:pk>/', updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', deleteOrder, name='delete_order'),
]