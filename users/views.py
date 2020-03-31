from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User


# Create your views here.


def create_user(request):
    if request.method == "POST":
        user = User.objects.create_user(username=request.POST["username"],
                                        password=request.POST["password"],
                                        email=request.POST["email"],
                                        )
        user.save()
        return render(request, 'users/create.html')
    else:
        return render(request, 'users/create.html')

