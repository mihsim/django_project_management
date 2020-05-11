from django.urls import path

from . import views


app_name = 'sprints'
urlpatterns = [
    path("", views.all_sprints, name="all"),
    path("create/", views.create, name="create"),
    path("<int:sprint_pk>/", views.sprint_view, name="sprint"),
    path("<int:sprint_pk>/<int:task_pk>/increase/", views.increase_task_progress, name="increase_task_progress"),
    path("<int:sprint_pk>/<int:task_pk>/decrease/", views.decrease_task_progress, name="decrease_task_progress"),
]
