from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from datetime import datetime

from .models import Sprint
from project.models import Project, ProjectParticipants
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

        # Check that request.post start_date is before than end_date.
        if request.POST["start_date"] > request.POST["end_date"]:
            content["error"] = "End date can not be before start date"
            return render(request, 'sprints/create.html', content)

        # Check that request.post start_date is after latest end_date in database.
        last_sprint_end_date = Sprint.objects.filter()
        if last_sprint_end_date:
            form_start_date = datetime.strptime(request.POST['start_date'], "%Y-%m-%d").date()
            db_last_date = last_sprint_end_date.latest('date_to').date_to
            if form_start_date <= db_last_date:
                content["error"] = "New sprint can not start before previous ones have ended. Latest end date: {}".format(db_last_date)
                return render(request, 'sprints/create.html', content)

        Sprint.objects.create(
            name="Sprint {0}".format(sprint_number),
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

    # Key-s are named same as CSS classes so it would possible to loop in HTML file.
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


def get_current_progress_index(project_pk, sprint_pk, task_pk, request_user):
    project = get_object_or_404(Project, pk=project_pk)
    sprint = get_object_or_404(Sprint, pk=sprint_pk)
    task = get_object_or_404(Task, pk=task_pk)

    if sprint != task.sprint:
        return redirect("home:home")
    if project != sprint.project:
        return redirect("home:home")
    if request_user not in ProjectParticipants.get_project_participants(project):
        return redirect("home:home")

    progress_index = task.progress_sequence.index(task.progress)
    return project, sprint, task, progress_index


@login_required(login_url=LOGIN_REDIRECT_URL)
def increase_task_progress(request, project_pk, sprint_pk, task_pk):
    project, sprint, task, progress_index = get_current_progress_index(project_pk=project_pk,
                                                                       sprint_pk=sprint_pk,
                                                                       task_pk=task_pk,
                                                                       request_user=request.user,
                                                                       )
    if task.progress == task.progress_sequence[-1]:
        # It should not be possible to reach progress increase function if task has last progress option.
        return redirect("home:home")

    task.progress = task.progress_sequence[progress_index + 1]
    task.save()
    return redirect("sprints:sprint", project_pk, sprint_pk)


@login_required(login_url=LOGIN_REDIRECT_URL)
def decrease_task_progress(request, project_pk, sprint_pk, task_pk):
    project, sprint, task, progress_index = get_current_progress_index(project_pk=project_pk,
                                                                       sprint_pk=sprint_pk,
                                                                       task_pk=task_pk,
                                                                       request_user=request.user,
                                                                       )
    if task.progress == task.progress_sequence[0]:
        # It should not be possible to reach progress decrease function if task has first progress option.
        return redirect("home:home")

    task.progress = task.progress_sequence[progress_index - 1]
    task.save()
    return redirect("sprints:sprint", project_pk, sprint_pk)

