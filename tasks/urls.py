from django.urls import path

from . import views


app_name = "tasks"
urlpatterns = [
    path("", views.tasks_all, name="all"),
    path("create/", views.create_view, name="create"),
    path("change/<int:task_pk>/", views.change_view, name="change"),
]
