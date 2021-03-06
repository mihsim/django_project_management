from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path("<int:project_id>/", views.ProjectView.as_view(), name="project"),
    path("<int:project_id>/delete/", views.ProjectView.delete, name="delete"),
    path("<int:project_id>/participants/", views.ProjectView.participants, name="participants"),

    path("<int:project_id>/change/", views.ProjectChangeView.as_view(), name="change"),

    path("<int:project_id>/search/participants/", views.CreateInviteToProject.as_view(), name="search_participants"),
    path("<int:project_id>/<int:participant_id>/invite/", views.CreateInviteToProject.as_view(), name="send_invite"),

    path("<int:invitation_id>/invitation/<str:action>", views.ManageInvite.as_view(), name="invitation"),

    path("<int:participation_id>/<int:user_id>/<str:action>/", views.ManageParticipation.as_view(), name="manage_participation")
]