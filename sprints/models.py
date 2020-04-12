from django.db import models

from project.models import Project


class Sprint(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()
    planned_story_points = models.CharField(max_length=200)

    def __str__(self):
        return self.name
