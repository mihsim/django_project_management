from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('create/', views.account_create, name='create'),
    path('login/', views.account_login, name="login"),
    path('logout/', views.account_logout, name="logout"),
]
