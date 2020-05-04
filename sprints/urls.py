from django.urls import path

from . import views


app_name = 'sprints'
urlpatterns = [
    path("", views.all_sprints, name="all"),
    path("create/", views.create, name="create"),
]