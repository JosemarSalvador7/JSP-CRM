from multiprocessing import AuthenticationError

from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.transaction import atomic
from accounts.forms import FormLogin
from accounts.models import Profile


def login_view(requests):
    if requests.method == "POST":
        user = requests.POST.get("username")
        password = requests.POST.get("password")
        result = authenticate(requests, username=user, password=password)
        print(result)
        if not result:
            raise AuthenticationError
        login(requests, user=result)
        return redirect("dashboard:home")

    return render(requests, "login.html", {"form": FormLogin})


def logout_view(requests):
    logout(requests)
    return redirect("acconts:login")


@atomic()
def register_view(requests):
    if requests.method == "POST":
        user = requests.POST.get("username")
        password = requests.POST.get("password")
        email = requests.POST.get("email")
        avatar = requests.FILE.get("photo")
        role = requests.POST.get("role")
        # TODO: aplicar seguraça

        user = User.objects.create_user(username=user, password=password, email=email)
        Profile.objects.create(user=user, role=role, avatar=avatar)
        return redirect("")
    return render(requests, "register.html", {})
