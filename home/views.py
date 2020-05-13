from django.shortcuts import render, redirect


def home(request):
    # if user is logged in, then homepage is page with all projects
    # if user is not logged in, then homepage is login page
    if request.user.is_authenticated:
        return redirect("projects:overview")
    else:
        return redirect("users:login")
