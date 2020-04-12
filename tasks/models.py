from django.db import models
from django.contrib.auth.models import User

from sprints.models import Sprint


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    story_points = models.CharField(max_length=200)
    assigned_person = models.ManyToManyField(User)
    task_name = models.CharField(max_length=80)

    def __str__(self):
        return self.name
