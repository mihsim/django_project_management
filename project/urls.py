from django.urls import path
from . import views

app_name = 'project'
urlpatterns = [
    path("", views.project_home, name="home"),
    path("create/", views.project_create, name="create"),
]