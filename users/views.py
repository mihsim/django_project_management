from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash


def account_create(request):
    if request.method == "POST":
        user = User.objects.create_user(username=request.POST["username"],
                                        password=request.POST["password"],
                                        email=request.POST["email"],
                                        )
        user.save()
        login(request, user)
        return render(request, 'users/create.html')
    else:
        return render(request, 'users/create.html')


@login_required
def account_modify(request):
    if request.method == "GET":
        return render(request, "users/account_modify.html")
    else:
        pass


@login_required
def change_password(request):
    if request.method == "POST":
        if request.user.check_password(request.POST['old_password']):
            if request.POST['new_password1'] == request.POST['new_password2']:
                request.user.set_password(request.POST['new_password1'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                return render(request, 'users/account_modify.html', {'password_changed': 'Password change successful!'})
            else:
                return render(request, 'users/account_modify.html', {'password_change_error': 'New passwords did not match!'})
        else:
            return render(request, 'users/account_modify.html', {'password_change_error': 'Current password was wrong!'})
    else:
        return redirect("users:modify")


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
        

