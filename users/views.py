from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout


# Create your views here.


def account_create(request):
    if request.method == "POST":
        user = User.objects.create_user(username=request.POST["username"],
                                        password=request.POST["password"],
                                        email=request.POST["email"],
                                        )
        user.save()
        return render(request, 'users/create.html')
    else:
        return render(request, 'users/create.html')


@login_required
def account_logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('project:home')
        

