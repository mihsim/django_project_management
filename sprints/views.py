from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Sprint
from project.models import Project
from tasks.models import Task
from project_management.settings import LOGIN_REDIRECT_URL


@login_required(login_url=LOGIN_REDIRECT_URL)
def all_sprints(request, project_pk):
    content = {}
    project = get_object_or_404(Project, pk=project_pk)
    sprints = Sprint.objects.filter(project=project)
    content['project'] = project
    content['sprints'] = sprints
    return render(request, "sprints/sprints.html", content)


@login_required(login_url=LOGIN_REDIRECT_URL)
def create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)

    if project.administrator != request.user:
        # Only project administrator may create sprints.
        return redirect('home:home')

    content = {'project': project}
    sprint_number = len(Sprint.objects.filter(project=project)) + 1

    if request.method == "POST":
        if request.POST["start_date"] > request.POST["end_date"]:
            content["error"] = "End date can not be before start date"
            return render(request, 'sprints/create.html', content)

        Sprint.objects.create(
            name=f"Sprint {sprint_number}",
            project=project,
            date_from=request.POST["start_date"],
            date_to=request.POST["end_date"],
            planned_story_points=0,
        )
        return redirect('sprints:all', project_pk)
    else:
        return render(request, 'sprints/create.html', content)


@login_required(login_url=LOGIN_REDIRECT_URL)
def sprint_view(request, project_pk, sprint_pk):
    project = get_object_or_404(Project, pk=project_pk)
    sprint = get_object_or_404(Sprint, pk=sprint_pk)
    tasks = Task.objects.filter(sprint=sprint)

    tasks_by_progress = {'backlog': [],
                         'todo': [],
                         'inprogress': [],
                         'qa': [],
                         'done': [],
                         }
    progress_options = [option for option in tasks_by_progress]

    for task in tasks:
        tasks_by_progress[task.progress.lower().replace(" ", "")].append(task)

    context = {'project': project,
               'sprint': sprint,
               'progress_options': progress_options,
               'tasks_by_progress': tasks_by_progress,
               }
    return render(request, 'sprints/sprint.html', context)


def increase_task_progress(request, project_pk, sprint_pk, task_pk):
    return HttpResponse("This will increase task status.")


def decrease_task_progress(request, project_pk, sprint_pk, task_pk):
    return HttpResponse("This will decrease task progress")
