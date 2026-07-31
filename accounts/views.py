from io import BytesIO
from django.http import FileResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from fpdf import FPDF
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


@login_required()
def logout_view(requests):
    logout(requests)
    return redirect("accounts:login")


@login_required()
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


@login_required()
def list_view(requests):
    users = User.objects.only("username",'is_active','email')
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


@login_required()
@atomic
def edit_view(requests, user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user_id=user)
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


@login_required()
def delete_view(request, user_id):
    user = User.objects.get(id=user_id)
    username = user.username
    if user.id == request.user.id:  # type:ignore
        messages.error(request, "Não Pode Apagar a sua Própria conta")
        return redirect("accounts:list")
    user.delete()
    messages.success(request, _(f"Usuário {username} Eliminado Com Sucesso"))
    return redirect("accounts:list")


@login_required()
def users_pdf_view(requets):
    pdf = FPDF()
    pdf.add_page(orientation="l")
    pdf.set_font("Arial", "B", 20)
    pdf.set_fill_color(200, 200, 200)

    pdf.cell(w=40, h=20, txt=_("Lista de Usuários do Sistema"), ln=1)  # type:ignore
    pdf.set_font("Arial", "B", 14)
    pdf.cell(w=72, h=10, txt=_("Nome de Usuário"), border=1, fill=1)  # type:ignore
    pdf.cell(w=72, h=10, txt=_("Nome completo"), border=1, fill=1)  # type:ignore
    pdf.cell(w=72, h=10, txt=_("E-mail"), border=1, fill=1)  # type:ignore
    pdf.cell(w=30, h=10, txt=_("Função"), border=1, fill=1)  # type:ignore
    pdf.cell(w=30, h=10, txt=_("Estado"), border=1, ln=1, fill=1)  # type:ignore
    pdf.set_font("Arial", "", 12)
    for user in User.objects.all():
        pdf.cell(w=72, h=10, txt=_("Nome de Usuário"), border=1)  # type:ignore
        pdf.cell(
            w=72,
            h=10,
            txt=_(f"{(user.get_full_name()) or 'Não Informado'}"),
            border=1,  # type:ignore
        )  # type:ignore
        pdf.cell(w=72, h=10, txt=_(f"{user.email or 'Não Informado'}"), border=1)  # type:ignore
        pdf.cell(w=30, h=10, txt=_(f"{user.profile.get_role_display()}"), border=1)  # type:ignore
        pdf.cell(
            w=30,
            h=10,
            txt=_(f"{'ativo' if user.is_active else 'inativo'}"),  # type:  ignore
            border=1,
            ln=1,
        )  # type:ignore
    pdf_out = pdf.output(dest="S").encode("latin1")  # type:ignore
    return FileResponse(BytesIO(pdf_out), filename=str(_("Lista de Usuarios.pdf")))


@login_required(login_url="accounts:login")
def profile_view(request):
    """Exibe o perfil do usuário logado"""
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    # Estatísticas do usuário
    from contacts.models import Contact
    from interations.models import Interaction
    from task.models import Task
    from opportunities.models import Opportunity

    total_contacts = Contact.objects.filter(created_by=user).count()
    total_interactions = Interaction.objects.filter(created_by=user).count()
    total_tasks = Task.objects.filter(created_by=user).count()
    total_opportunities = Opportunity.objects.filter(created_by=user).count()

    context = {
        "user": user,
        "profile": profile,
        "total_contacts": total_contacts,
        "total_interactions": total_interactions,
        "total_tasks": total_tasks,
        "total_opportunities": total_opportunities,
    }
    return render(request, "profile.html", context)


@login_required(login_url="accounts:login")
def profile_edit_view(request):
    """Edita o perfil do usuário logado"""
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        form = EditUserForm(request.POST, request.FILES)
        if form.is_valid():
            # Atualiza dados do usuário
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            if username and username != user.username:
                if User.objects.filter(username=username).exclude(id=user.id).exists():
                    messages.error(request, _("Este nome de usuário já está em uso."))
                    return render(
                        request,
                        "profile_edit.html",
                        {"form": form, "user": user, "profile": profile},
                    )
                user.username = username

            if email and email != user.email:
                if User.objects.filter(email=email).exclude(id=user.id).exists():
                    messages.error(request, _("Este email já está em uso."))
                    return render(
                        request,
                        "profile_edit.html",
                        {"form": form, "user": user, "profile": profile},
                    )
                user.email = email

            if password:
                user.set_password(password)

            user.save()

            # Atualiza o perfil
            if "avatar" in request.FILES:
                profile.avatar = request.FILES["avatar"]

            role = form.cleaned_data.get("role")
            if role and role != profile.role:
                profile.role = role
                profile.save()  # O save() atualiza o code automaticamente

            profile.save()

            messages.success(request, _("Perfil atualizado com sucesso!"))
            return redirect("accounts:profile")
        else:
            messages.error(request, _("Erro ao atualizar perfil. Verifique os dados."))
    else:
        initial_data = {
            "username": user.username,
            "email": user.email,
            "role": profile.role,
        }
        form = EditUserForm(initial=initial_data)

    return render(
        request, "profile_edit.html", {"form": form, "user": user, "profile": profile}
    )
