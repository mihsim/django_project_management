from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from typing import List, Dict

from .models import Project, ProjectParticipants, ProjectParticipantsInvites


class ProjectView(View):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        context = {"project": project}
        return render(request, "project/project.html", context)

    @classmethod
    def participants(cls, request, project_id):
        project = Project.objects.get(id=project_id)
        context = {"project": project}
        project_participants = cls.get_project_participants(project_id)
        project_invitees = cls.get_invited_to_participate(request, project_id)
        context.update(**project_participants, **project_invitees)
        return render(request, "project/participants.html", context)

    @staticmethod
    def get_project_participants(project_id: int) -> Dict[str, List]:
        try:
            participation = ProjectParticipants.objects.get(project=project_id)
        except ProjectParticipants.DoesNotExist:
            participation = None
        return {"participation": participation}

    @staticmethod
    def get_invited_to_participate(request, project_id: int) -> Dict[str, List]:
        try:
            invites = ProjectParticipantsInvites.objects.filter(project=project_id, from_user=request.user.pk)
        except ProjectParticipantsInvites.DoesNotExist:
            invites = None
        return {"invites_to_participate_in_project": invites}

    @staticmethod
    def delete(request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        if request.method == "POST" and request.user == project.administrator:
            project.delete()
            return redirect('projects:overview')
        elif request.method == "GET":
            context = {'project': project,
                       'warning_message': 'Deleted project can not be restored!'}
            return render(request, 'project/delete.html', context)
        else:
            # If request.method was 'POST' but user was not administrator for project:
            return redirect('home:home')


class ProjectChangeView(View):
    def get(self, request, project_id):
        project = Project.objects.get(pk=project_id)
        context = {"project": project}
        return render(request, "project/change.html", context)

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
        context = {'project': project,
                   "invite_result": invite_result,
                   "invite_message": invite_message}
        if invite_result == "Successful":
            return render(request, "project/project.html", context)
        else:
            request.method = "GET"
            return render(request, "project/search_participants.html", context)


class ManageInvite(View):
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
            return redirect('projects:overview')
        elif action == 'delete' and invitation.from_user.id == request.user.id:
            invitation.delete()
            return redirect('projects:overview')
        
        # 'HttpResponse('NO')'  is met for cases where user tries to change things he is not allowed
        # or typing 'acton' that does not exist.
        # FIXME HttpResponse('NO') is not working and returns "HTTP ERROR 405" instead.
        return HttpResponse('NO')


class ManageParticipation(View):
    @staticmethod
    def post(request, participation_id, user_id, action):
        participation = get_object_or_404(ProjectParticipants, pk=participation_id)
        user = get_object_or_404(User, pk=user_id)
        if action == "remove" and participation.project.administrator == request.user:
            participation.user.remove(user)
        return redirect('project:project', participation.project.pk)
