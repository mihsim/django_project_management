from django.db import models
from django.contrib.auth.models import User

progress = (
    ('1', 'Backlog'),
    ('2', 'To do'),
    ('3', 'In Progress'),
    ('4', 'QA'),
    ('5', 'Done')
)

weight = (
    ('1', '2', '3', '4', '5')
)


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    administrator = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class ProjectParticipants(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.project


class Sprint(models.Model):
    name = models.CharField(max_length=100)
    date_from = models.DateField()
    date_to = models.DateField()
    planned_story_points = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    story_points = models.CharField(max_length=200)
    assigned_person = models.ManyToManyField(User)
    task_name = models.CharField(max_length=80)

    def __str__(self):
        return self.name
