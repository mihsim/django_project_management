from django.shortcuts import render, redirect
from django.views import View

from project.models import User, Project, ProjectParticipants, ProjectParticipantsInvites


# Create your views here.
class Projects(View):
    """
    Projects page. (All projects)
    - Displays list of all projects user is administrator to.
    - Displays list of all projects user is contributor to.
    - Has button "Create new project" which leads to next page.
    """
    def get(self, request):
        user = User.objects.get(id=request.user.pk)
        projects_user_is_administrator_to = Project.objects.filter(administrator=user)
        projects_user_is_participant_to = ProjectParticipants.objects.filter(user=user)
        projects_user_is_invited_to = ProjectParticipantsInvites.objects.filter(to_user=user)
        return render(request, "projects/overview.html", {'administrator_to_projects': projects_user_is_administrator_to,
                                                     'participations_to_projects': projects_user_is_participant_to,
                                                     'invitations_to_projects': projects_user_is_invited_to})


class Create(View):
    def get(self, request):
        return render(request, "projects/create.html")

    def post(self, request):
        project = Project.objects.create(name=request.POST["project_name"],
                                         description=request.POST["project_description"],
                                         administrator=User.objects.get(id=request.user.pk)
                                         )
        project.save()
        return redirect('projects:overview')