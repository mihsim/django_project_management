from django.urls import path
from . import views

app_name = 'project'
urlpatterns = [
    path("", views.Projects.as_view(), name="home"),
    path("create/", views.ProjectsCreate.as_view(), name="create"),
    path("<int:project_id>/", views.ProjectView.as_view(), name="project"),
    path("<int:project_id>/change/", views.ProjectChangeView.as_view(), name="change"),
    path("<int:project_id>/search_participants/", views.ProjectInviteView.as_view(), name="search_participants"),
    path("<int:project_id>/<int:participant_id>/send", views.ProjectInviteView.as_view(), name="send_invite"),
    path("<int:project_id>/<int:participant_id>/delete", views.ProjectInviteView.as_view(), name="invite_delete"),

]