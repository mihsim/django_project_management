from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Project, ProjectParticipants, ProjectParticipantsInvites



@login_required
def project_home(request):
    user = User.objects.get(id=request.user.pk)
    projects_administrator_to = Project.objects.filter(administrator=user)
    # projects_contributor_to - projects that user is contributor but not administrator
    projects_contributor_to = None
    return render(request, "project/home.html", {'projects_admin': projects_administrator_to,
                                                 'projects_contributor': projects_contributor_to})


@login_required
def project_create(request):
    if request.method == "GET":
        return render(request, "project/create.html")
    else:
        project = Project.objects.create(name=request.POST["project_name"],
                                         description=request.POST["project_description"],
                                         administrator=User.objects.get(id=request.user.pk)
                                         )
        project.save()
        return redirect('project:home')


@login_required
def project_view(request, project_id):
    project = Project.objects.get(id=project_id)
    try:
        project_with_participants = ProjectParticipants.objects.get(project=project_id)
        project_participants = project_with_participants.user.all()
    except ProjectParticipants.DoesNotExist:
        project_participants = None
    content = {"project": project,
               "project_participants": project_participants,
               }
    return render(request, "project/project.html", content)


@login_required
def project_modify(request, project_id):
    project = Project.objects.filter(id=project_id).first()
    content = {"project": project}
    if request.method == "GET":
        return render(request, "project/modify.html", content)
    else:
        project = Project.objects.filter(id=project_id).first()
        project.name = request.POST["project_name"]
        project.description = request.POST["project_description"]
        project.save()
        return redirect("project:project", project_id)


def search_participants(request, project_id):
    project = Project.objects.filter(id=project_id).first()
    if request.method == "GET":
        return render(request, "project/search_participants.html", {'project': project})
    else:
        email = request.POST['email_to_check']
        if email:
            try:
                contributor_found = User.objects.get(email=email)
            except User.DoesNotExist:
                content = {'project': project,
                           'contributor_not_found': 'No registered user has that email.'}
                return render(request, "project/search_participants.html", content)
            return render(request, "project/search_participants.html", {'project': project,
                                                                        'contributor_found': contributor_found})
        return HttpResponse("POST not implemented yet")


def invite_participant(request, project_id, participant_id):
    invite_result, invite_message = ProjectParticipantsInvites.add_invite(project_id=project_id, from_user_id=request.user.id, to_user_id=participant_id)
    project = Project.objects.filter(id=project_id).first()
    content = {'project': project,
               "invite_result": invite_result,
               "invite_message": invite_message}

    return render(request, "project/project.html", content)
    #return redirect('project:project', project_id,)
