from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('create/', views.user_create, name='create'),
    path('', views.view_myself, name="view_myself"),
    path('account/change/', views.change, name="change"),
    # path('account/change/password/', views.change_password, name="change_password"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('delete/', views.account_delete, name="delete"),
]
