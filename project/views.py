from django.shortcuts import render, HttpResponse, redirect
from .models import Project

from django.contrib.auth.models import User


def project_home(request):
    return render(request, "project/home.html")


def project_create(request):
    if request.method == "GET":
        return render(request, "project/create.html")
    else:
        project = Project.objects.create(name=request.POST["project_name"],
                                         description=request.POST["project_description"],
                                         administrator=User.objects.get(id=request.user.pk)
                                         )
        project.save()
        return redirect('project:home')
