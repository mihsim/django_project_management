from django.contrib import admin
from .models import Project, Task, Sprint, ProjectParticipants
# Register your models here.

admin.site.register((Project, Task, Sprint, ProjectParticipants))
