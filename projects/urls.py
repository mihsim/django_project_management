from django.urls import path

from . import views

app_name = 'projects'

urlpatterns =[
    path("", views.Projects.as_view(), name="overview"),
    path("create/", views.Create.as_view(), name="create"),
]