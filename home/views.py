from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def home(request):
    # if user is logged in, then homepage is page with all projects
    # if user is not logged in, then homepage is login page
    if request.user.is_authenticated:
        return redirect("projects:overview")
    else:
        return render(request, 'users/login.html')