from django.urls import path
from . import views

app_name = 'project'
urlpatterns = [
    path("", views.project_home, name="home"),
    path("create/", views.project_create, name="create"),
    path("<int:project_id>/", views.project_view, name="project"),
    path("<int:project_id>/modify/", views.project_modify, name="modify"),
    path("<int:project_id>/modify/invite_contributors/", views.invite_contributors, name="invite_contributors"),
    path("<int:project_id>/<int:contributor_id>/", views.add_contributor , name="add_contributor"),
]