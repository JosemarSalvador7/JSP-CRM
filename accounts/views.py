from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from accounts.forms import EditUserForm, FormLogin, RegisterUserForm
from accounts.models import Profile


def login_view(requests):
    if requests.method == "POST":
        user = requests.POST.get("username")
        password = requests.POST.get("password")
        result = authenticate(requests, username=user, password=password)
        if result is None:
            messages.error(requests, _("Senha ou email ERRADO"))
            return redirect("accounts:login")
        login(requests, user=result)
        return redirect("dashboard:home")

    return render(requests, "login.html", {"form": FormLogin})


def logout_view(requests):
    logout(requests)
    return redirect("accounts:login")


@atomic
def register_view(requests):
    if requests.method == "POST":
        user = requests.POST.get("username")
        password = requests.POST.get("password")
        email = requests.POST.get("email")
        role = requests.POST.get("role")
        avatar = requests.FILES.get("avatar")
        user = User.objects.create_user(username=user, password=password, email=email)
        Profile.objects.create(user=user, role=role, avatar=avatar)  # type: ignore
        messages.success(requests, _("Usuario cadastrado com sucesso"))
        return redirect("accounts:register")
    return render(requests, "register.html", {"form": RegisterUserForm()})


def list_view(requests):
    users = User.objects.all()
    return render(
        requests,
        "list_accounts.html",
        {
            "users": users,
            "total_users": User.objects.count(),
            "sellers_count": User.objects.filter(profile__role="V").count(),
            "managers_count": User.objects.filter(profile__role="G").count(),
            "users_with_avatar": User.objects.filter(
                profile__avatar__isnull=False
            ).count(),
        },
    )


@atomic
def edit_view(requests, user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)
    if requests.method == "POST":
        user.username = requests.POST.get("username") or user.username
        user.set_password(requests.POST.get("password") or user.password)
        user.email = requests.POST.get("email") or user.email
        user.save()
        profile.role = requests.POST.get("role") or profile.role
        profile.avatar = requests.FILES.get("avatar") or profile.avatar  # type: ignore
        profile.save()
        messages.success(requests, _("Dados do Usuario Atualizado com sucesso"))
        return redirect("accounts:list")

    return render(
        requests,
        "update_account.html",
        {
            "user_edit": user,
            "form": EditUserForm(
                data={
                    "username": user.username,
                    "avatar": profile.avatar,
                    "email": user.email,
                    "role": profile.role,
                }
            ),
        },
    )


def delete_view(requests, user_id):
    user = User.objects.get(id=user_id)
    username = user.username
    user.delete()
    messages.success(requests, _(f"Usuário {username} Eliminado Com Sucesso"))
    return redirect("accounts:list")
