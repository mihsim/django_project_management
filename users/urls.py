from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('create/', views.account_create, name='create'),
    path('', views.view_myself, name="view_myself"),
    path('account/change/', views.change_username_email, name="change"),
    path('account/change/password/', views.change_password, name="change_password"),
    path('login/', views.account_login, name="login"),
    path('logout/', views.account_logout, name="logout"),
    path('delete/', views.account_delete, name="delete"),
]
