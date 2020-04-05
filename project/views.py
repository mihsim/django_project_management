from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from typing import List, Dict

from .models import Project, ProjectParticipants, ProjectParticipantsInvites


class Projects(View):
    """
    Projects page. (All projects)
    - Displays list of all projects user is administrator to.
    - Displays list of all projects user is contributor to.
    - Has button "Create new project" which leads to next page.
    """
    def get(self, request):
        user = User.objects.get(id=request.user.pk)
        projects_administrator_to = Project.objects.filter(administrator=user)
        # projects_contributor_to - projects that user is contributor but not administrator
        projects_contributor_to = None
        return render(request, "project/home.html", {'projects_admin': projects_administrator_to,
                                                     'projects_contributor': projects_contributor_to})


class ProjectsCreate(View):
    def get(self, request):
        return render(request, "project/create.html")

    def post(self, request):
        project = Project.objects.create(name=request.POST["project_name"],
                                         description=request.POST["project_description"],
                                         administrator=User.objects.get(id=request.user.pk)
                                         )
        project.save()
        return redirect('project:home')


class ProjectView(View):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        content = {"project": project}
        project_participants = self.get_project_participants(project_id)
        project_invitees = self.get_invited_to_participate(project_id)
        content.update(**project_participants, **project_invitees)
        return render(request, "project/project.html", content)

    @staticmethod
    def get_project_participants(project_id: int) -> Dict[str, List]:
        try:
            project_with_participants = ProjectParticipants.objects.get(project=project_id)
            project_participants = project_with_participants.user.all()
        except ProjectParticipants.DoesNotExist:
            project_participants = None
        return {"project_participants": project_participants}

    @staticmethod
    def get_invited_to_participate(project_id: int) -> Dict[str, List]:
        try:
            invites = ProjectParticipantsInvites.objects.filter(project=project_id)
            project_invitees = [invite.to_user for invite in invites]
        except ProjectParticipantsInvites.DoesNotExist:
            project_invitees = None
        return {"project_invitees": project_invitees}


class ProjectChangeView(View):
    def get(self, request, project_id):
        project = Project.objects.filter(id=project_id).first()
        content = {"project_id": project.id,
                   "project_name": project.name,
                   "project_description": project.description}
        return render(request, "project/change.html", content)

    def post(self, request, project_id):
        project = Project.objects.filter(id=project_id).first()
        project.name = request.POST["project_name"]
        project.description = request.POST["project_description"]
        project.save()
        return redirect("project:project", project_id)


class ProjectInviteView(View):
    def get(self, request, project_id):
        email = request.GET.get('email_to_check')
        project = Project.objects.get(id=project_id)
        if not email:
            return render(request, "project/search_participants.html", {'project': project})
        else:
            # Check if user already is participating or is invited.
            invite_result, invite_message, contributor_found = ProjectParticipantsInvites.check_participant(project_id=project_id,
                                                                                         to_user_email=email)
            # Gives ERROR alert that user can not be added.
            if invite_result == "Error":
                return render(request, "project/search_participants.html", {'project': project,
                                                                            'invite_result': invite_result,
                                                                            'invite_message': invite_message})
            # Is returned if user with current email could be added as contributor.
            return render(request, "project/search_participants.html", {'project': project,
                                                                        'contributor_found': contributor_found})

    def post(self, request, project_id, participant_id):
        invite_result, invite_message = ProjectParticipantsInvites.add_invite(project_id=project_id,
                                                                              from_user_id=request.user.id,
                                                                              to_user_id=participant_id)
        project = Project.objects.get(id=project_id)
        content = {'project': project,
                   "invite_result": invite_result,
                   "invite_message": invite_message}
        if invite_result == "Successful":
            return render(request, "project/project.html", content)
        else:
            request.method = "GET"
            return render(request, "project/search_participants.html", content)

    def put(self, request):
        return HttpResponse("PUT is not implemented")

    def delete(self, request, project_id, participant_id):
        result, message = ProjectParticipantsInvites.delete_invite(project_id=project_id, to_user_id=participant_id)
        project = Project.objects.get(id=project_id)
        content = {'project': project,
                   "invite_delete_result": result,
                   "invite_delete_message": message}

        return render(request, "project/project.html", content)
