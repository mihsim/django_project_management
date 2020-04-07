from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import Http404
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
        projects_user_is_administrator_to = Project.objects.filter(administrator=user)
        projects_user_is_participant_to = ProjectParticipants.objects.filter(user=user)
        projects_user_is_invited_to = ProjectParticipantsInvites.objects.filter(to_user=user)
        return render(request, "project/home.html", {'administrator_to_projects': projects_user_is_administrator_to,
                                                     'participations_to_projects': projects_user_is_participant_to,
                                                     'invitations_to_projects': projects_user_is_invited_to})


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
        project_invitees = self.get_invited_to_participate(request, project_id)
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
    def get_invited_to_participate(request, project_id: int) -> Dict[str, List]:
        try:
            invites = ProjectParticipantsInvites.objects.filter(project=project_id, from_user=request.user.pk)
        except ProjectParticipantsInvites.DoesNotExist:
            invites = None
        return {"invites_to_participate_in_project": invites}


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


class CreateInviteToProject(View):
    @staticmethod
    def get(request, project_id):
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

    @staticmethod
    def post(request, project_id, participant_id):
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


class ManageInvites(View):
    def post(self, request, invitation_id, action):
        """
        :type request: HttpRequest
        :type invitation_id: int
        :type action: str - accept, decline, delete
        :rtype: HttpResponse
        """

        invitation = get_object_or_404(ProjectParticipantsInvites, pk=invitation_id)
        # Invitee can accept and decline invite
        # Invitor can delete invite
        if action == 'accept' and invitation.to_user.id == request.user.id:
            try:
                project_participants = ProjectParticipants.objects.get(project=invitation.project)
                project_participants.user.add(invitation.to_user)
                invitation.delete()
            except ProjectParticipants.DoesNotExist:
                project_participants = ProjectParticipants.objects.create(project=invitation.project)
                project_participants.user.add(invitation.to_user)
                invitation.delete()
            return redirect('project:project', project_participants.project.id)

        elif action == 'decline' and invitation.to_user.id == request.user.id:
            invitation.status = 'Declined'
            invitation.save()
            return redirect('project:home')
        elif action == 'delete' and invitation.from_user.id == request.user.id:
            invitation.delete()
            return redirect('project:home')

        # 'HttpResponse('NO')'  is met for cases where user tries to change things he is not allowed
        # or typing 'acton' that does not exist.
        # Not sure why but this HttpResponse('NO') is not working and returns "HTTP ERROR 405" instead
        return HttpResponse('NO')
