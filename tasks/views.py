from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.forms import ModelChoiceField

from project.models import Project, ProjectParticipants
from sprints.models import Sprint
from .forms import TaskCreateForm


def tasks_all(request, project_pk):
    return HttpResponse("Here will be all created tasks.")


def create_view(request, project_pk):
    form = TaskCreateForm(request.POST or None)
    project = get_object_or_404(Project, pk=project_pk)
    sprints = Sprint.objects.filter(project=project)

    # Task assignees may be selected from project participants.
    try:
        project_participants = ProjectParticipants.objects.get(project=project)
        form.fields["assignee"] = ModelChoiceField(queryset=project_participants.user.all(), required=False)
    except ProjectParticipants.DoesNotExist:
        form.fields["assignee"] = ModelChoiceField(queryset=User.objects.none(), required=False)

    # Sprint may be selected from sprints that are created for this particular project.
    form.fields["sprint"] = ModelChoiceField(queryset=Sprint.objects.filter(project=project), required=False)

    if form.is_valid():
        form.save()
        return redirect("tasks:all", project.pk)

    context = {'form': form, 'project': project, 'sprints': sprints}
    return render(request, "tasks/create.html", context)
