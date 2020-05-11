from django.db import models
from django.contrib.auth.models import User

from sprints.models import Sprint
from project.models import Project


class Task(models.Model):
    class Priority(models.IntegerChoices):
        high = 3
        medium = 2
        medium_low = 1
        low = 0

    class Progress(models.TextChoices):
        backlog = 'Backlog'
        todo = 'To Do'
        in_progress = 'In Progress'
        quality_assurance = 'QA'
        done = 'Done'

    @property
    def progress_sequence(self):
        return ['Backlog', 'To Do', 'In Progress', 'QA', 'Done']

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.IntegerField(choices=Priority.choices, default=1)
    progress = models.CharField(choices=Progress.choices, max_length=12, default='Backlog')
    story_points = models.IntegerField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, blank=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True, blank=True)
    assignee = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.name
