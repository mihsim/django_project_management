from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.db import IntegrityError


def account_create(request):
    if request.method == "POST":
        if request.POST['password1'] != request.POST['password2']:
            return render(request, 'users/create.html',
                          {'error_message': 'Passwords did not match!'})
        try:
            user = User.objects.create_user(username=request.POST["username"],
                                            password=request.POST["password1"],
                                            email=request.POST["email"],
                                            )
            user.save()
        except IntegrityError:
            return render(request, 'users/create.html', {'error_message': 'Selected username is not available, please select another username.'})
        login(request, user)
        return redirect('home:home')
    else:
        return render(request, 'users/create.html')


def view_myself(request):
    user = User.objects.get(pk=request.user.pk)
    return render(request, 'users/view_myself.html', {'date_registered': user.date_joined})


@login_required
def change_username_email(request):
    if request.method == "GET":
        return render(request, "users/change.html")
    else:
        if request.user.check_password(request.POST['password']):
            request.user.username = request.POST['username']
            request.user.email = request.POST['email']
            request.user.save()
            return render(request, "users/change.html", {'account_modification_success': 'Your data was successfully updated"'})
        else:
            return render(request, "users/change.html", {'account_modify_error': 'Wrong password!'})


@login_required
def change_password(request):
    if request.method == "POST":
        if request.user.check_password(request.POST['old_password']):
            if request.POST['new_password1'] == request.POST['new_password2']:
                request.user.set_password(request.POST['new_password1'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                return render(request, 'users/change.html', {'password_changed': 'Password change successful!'})
            else:
                return render(request, 'users/change.html', {'password_change_error': 'New passwords did not match!'})
        else:
            return render(request, 'users/change.html', {'password_change_error': 'Current password was wrong!'})
    else:
        return redirect("users:change")


def account_login(request):
    if request.method == "GET":
        return render(request, 'users/login.html')
    else:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect("projects:overview")
        else:
            return render(request, 'users/login.html', {'error': 'Username and password did not match!'})


@login_required
def account_logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home:home')


@login_required
def account_delete(request):
    if request.method == 'GET':
        warning_message = "Deleted account can not be restored!"
        return render(request, 'users/delete.html', {'warning_message': warning_message})

    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        user.delete()
        return redirect("home:home")


        

