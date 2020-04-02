from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('create/', views.account_create, name='create'),
    path('account/modify/', views.account_modify, name="modify"),
    path('account/modify/password/', views.change_password, name="change_password"),
    path('login/', views.account_login, name="login"),
    path('logout/', views.account_logout, name="logout"),
]
