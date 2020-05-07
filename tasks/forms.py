from django import forms

from .models import Task


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'priority',
            'progress',
            'story_points',
            'sprint',
            'assignee',
        ]


class TaskChangeForProjectAdministratorForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'priority',
            'progress',
            'story_points',
            'sprint',
            'assignee',
        ]


class TaskChangeForProjectParticipantForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'priority',
            'progress',
            'story_points',
        ]
