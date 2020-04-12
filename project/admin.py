from django.contrib import admin
from .models import Project, ProjectParticipants, ProjectParticipantsInvites
from sprints.models import Sprint
from tasks.models import Task
# Register your models here.

admin.site.register((Project, Task, Sprint, ProjectParticipants, ProjectParticipantsInvites))
