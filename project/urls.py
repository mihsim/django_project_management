from django.urls import path
from . import views

app_name = 'project'
urlpatterns = [
    path("", views.project_home, name="home"),
    path("create/", views.project_create, name="create"),
    path("<int:project_id>/", views.project_view, name="project"),
    path("<int:project_id>/modify/", views.project_modify, name="modify"),
    path("<int:project_id>/modify/search_participants/", views.search_participants, name="search_participants"),
    path("<int:project_id>/<int:participant_id>/", views.invite_participant, name="invite_participant"),
]