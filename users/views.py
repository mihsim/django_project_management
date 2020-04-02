from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate


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


def account_login(request):
    if request.method == "GET":
        return render(request, 'users/login.html')
    else:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect("project:home")
        else:
            return render(request, 'users/login.html', {'error': 'Username and password did not match!'})


@login_required
def account_logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('project:home')
        

