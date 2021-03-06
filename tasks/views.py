from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import ModelChoiceField

from project.models import Project, ProjectParticipants
from sprints.models import Sprint
from project_management.settings import LOGIN_REDIRECT_URL
from .models import Task
from .forms import TaskCreateForm, TaskChangeForProjectAdministratorForm, TaskChangeForProjectParticipantForm


@login_required(login_url=LOGIN_REDIRECT_URL)
def tasks_all(request, project_pk):
    context = {}
    project = get_object_or_404(Project, pk=project_pk)
    context['project'] = project

    tasks = Task.objects.filter(project=project)
    tasks_sorted_by_sprints = {}
    for task in tasks:
        if not task.sprint:
            try:
                tasks_sorted_by_sprints['tasks_without_sprint'].append(task)
            except KeyError:
                tasks_sorted_by_sprints['tasks_without_sprint'] = [task, ]
            continue
        try:
            tasks_sorted_by_sprints[task.sprint].append(task)
        except KeyError:
            tasks_sorted_by_sprints[task.sprint] = [task, ]
    context['tasks_sorted_by_sprints'] = tasks_sorted_by_sprints
    return render(request, "tasks/all_tasks.html", context)


def recalculate_sprint_story_points():
    # Used when changing and creating tasks.
    sprints = Sprint.objects.all()
    for sprint in sprints:
        tasks_in_sprint = Task.objects.filter(sprint=sprint)

        total_points = 0
        for task_in_sprint in tasks_in_sprint:
            if task_in_sprint.story_points is not None:
                total_points += task_in_sprint.story_points
        sprint.planned_story_points = total_points
        sprint.save()
    return None


@login_required(login_url=LOGIN_REDIRECT_URL)
def create_view(request, project_pk):
    form = TaskCreateForm(request.POST or None)
    project = get_object_or_404(Project, pk=project_pk)
    sprints = Sprint.objects.filter(project=project)

    # Task assignees may be selected from project participants.
    assignee_selection = ProjectParticipants.get_project_participants(project)
    form.fields["assignee"] = ModelChoiceField(queryset=assignee_selection, required=False)

    # Sprint may be selected from sprints that are created for this particular project.
    form.fields["sprint"] = ModelChoiceField(queryset=Sprint.objects.filter(project=project), required=False)

    if form.is_valid():
        # As task is created under specific project,
        # 'ForeignKey(Project)' is excluded from 'form.fields', and is added here.
        task_object = form.save(commit=False)
        task_object.project = project
        task_object.save()
        recalculate_sprint_story_points()
        return redirect("tasks:all", project.pk)

    context = {'form': form, 'project': project, 'sprints': sprints}
    return render(request, "tasks/create.html", context)


@login_required(login_url=LOGIN_REDIRECT_URL)
def change_view(request, project_pk, task_pk):
    project = get_object_or_404(Project, pk=project_pk)
    participants = ProjectParticipants.objects.get(project=project).user.all()
    task = get_object_or_404(Task, pk=task_pk)
    if request.user == project.administrator:
        form = TaskChangeForProjectAdministratorForm(request.POST or None, instance=task)
        assignee_selection = ProjectParticipants.get_project_participants(project)
        form.fields["assignee"] = ModelChoiceField(queryset=assignee_selection, required=False)
        form.fields["sprint"] = ModelChoiceField(queryset=Sprint.objects.filter(project=project), required=False)
    elif request.user in participants:
        form = TaskChangeForProjectParticipantForm(request.POST or None, instance=task)
    else:
        return redirect('home:home')

    if form.is_valid():
        form.save()
        recalculate_sprint_story_points()
        return redirect('tasks:all', project.pk)

    context = {'form': form, 'project': project, 'task': task}
    return render(request, "tasks/change.html", context)
