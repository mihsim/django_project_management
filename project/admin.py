from django.contrib import admin
from .models import Project, Task, Sprint, ProjectParticipants, ProjectParticipantsInvites
# Register your models here.

admin.site.register((Project, Task, Sprint, ProjectParticipants, ProjectParticipantsInvites))
