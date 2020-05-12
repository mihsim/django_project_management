from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm

from .models import MyUser
from .forms import RegistrationForm, UserAuthenticationForm, MyUserChangeForm


def user_create(request):
    context = {}
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect("home:home")
        else:
            context["registration_form"] = form
    else:
        form = RegistrationForm()
        context["registration_form"] = form
    return render(request, "users/create.html", context)


def user_logout(request):
    logout(request)
    return redirect("home:home")


def user_login(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        # If user is authenticated, then there is no need to show login screen.
        redirect("home:home")

    if request.method == "POST":
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)

            if user:
                # if user exists then it means that user was successfully authenticated.
                login(request, user)
                return redirect("home:home")

    else:
        form = UserAuthenticationForm()

    context["login_form"] = form
    return render(request, "users/login.html", context)


def view_myself(request):
    user = MyUser.objects.get(pk=request.user.pk)
    return render(request, 'users/view_myself.html', {'date_registered': user.date_joined})


def change(request):
    context = {}
    if request.method == 'POST':
        form = MyUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect("users:view_myself")
    else:
        form = MyUserChangeForm(instance=request.user)
        context['form'] = form
        return render(request, 'users/change.html', context)


@login_required
def account_delete(request):
    if request.method == 'GET':
        warning_message = "Deleted account can not be restored!"
        return render(request, 'users/delete.html', {'warning_message': warning_message})

    if request.method == 'POST':
        user = MyUser.objects.get(username=request.user.username)
        user.delete()
        return redirect("home:home")