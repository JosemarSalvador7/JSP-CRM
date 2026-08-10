from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import timedelta

from contacts.models import Contact
from interations.models import Interaction
from task.models import Task
from opportunities.models import Opportunity
# Create your views here.


@login_required(login_url="accounts:login")
def home_view(request):
    # Dados do usuário atual
    user = request.user

    # ==================== CONTATOS ====================
    if request.user.profile.role == "G":
        contacts = Contact.objects.all()
    else:
        contacts = Contact.objects.filter(assigned_to=user)

    total_contacts = contacts.count()

    contacts_with_email = contacts.filter(Q(email__isnull=False) & ~Q(email="")).count()
    contacts_without_email = contacts.filter(
        Q(email__isnull=True) | Q(email="")
    ).count()
    contacts_with_company = contacts.filter(
        Q(company__isnull=False) & ~Q(company="")
    ).count()

    # Últimos contatos adicionados
    recent_contacts = contacts.order_by("-created_at")[:5]

    # ==================== INTERAÇÕES ====================

    if request.user.profile.role == "G":
        interactions = Interaction.objects.all()
    else:
        interactions = Interaction.objects.filter(created_by=user)

    total_interactions = interactions.count()
    calls_count = interactions.filter(type_interaction="C").count()
    emails_count = interactions.filter(type_interaction="E").count()
    meetings_count = interactions.filter(type_interaction="M").count()

    # Últimas interações
    recent_interactions = interactions.order_by("-date_time")[:5]

    # ==================== TAREFAS ====================
    if request.user.profile.role == "G":
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=user)

    total_tasks = tasks.count()
    pending_tasks = tasks.filter(status="PENDING").count()
    in_progress_tasks = tasks.filter(status="IN_PROGRESS").count()
    done_tasks = tasks.filter(status="DONE").count()

    # Tarefas com vencimento próximo (próximos 7 dias)
    today = timezone.now().date()
    next_week = today + timedelta(days=7)
    upcoming_tasks = tasks.filter(
        due_date__gte=today,
        due_date__lte=next_week,
        status__in=["PENDING", "IN_PROGRESS"],
    ).order_by("due_date")[:5]

    # Tarefas atrasadas
    overdue_tasks = tasks.filter(
        due_date__lt=today, status__in=["PENDING", "IN_PROGRESS"]
    ).order_by("due_date")[:5]

    # Estatísticas de tarefas por prioridade
    high_priority_tasks = tasks.filter(priority="HIGH").count()

    medium_priority_tasks = tasks.filter(priority="MEDIUM").count()
    low_priority_tasks = tasks.filter(priority="LOW").count()

    # ==================== OPORTUNIDADES ====================
    if request.user.profile.role == "G":
        opportunities = Opportunity.objects.all()
    else:
        opportunities = Opportunity.objects.filter(assigned_to=user)

    total_opportunities = opportunities.count()

    # Oportunidades por estágio
    prospecting_count = opportunities.filter(stage="PROSPECTING").count()
    qualification_count = opportunities.filter(stage="QUALIFICATION").count()
    proposal_count = opportunities.filter(stage="PROPOSAL").count()
    negotiation_count = opportunities.filter(stage="NEGOTIATION").count()
    closed_won_count = opportunities.filter(stage="CLOSED_WON").count()
    closed_lost_count = opportunities.filter(stage="CLOSED_LOST").count()

    # Valor total das oportunidades
    total_opportunity_value = opportunities.aggregate(Sum("value"))["value__sum"] or 0

    # Oportunidades em andamento (excluindo fechadas)
    active_opportunities = opportunities.exclude(
        stage__in=["CLOSED_WON", "CLOSED_LOST"]
    ).count()

    # Últimas oportunidades adicionadas
    recent_opportunities = opportunities.select_related("contact").order_by(
        "-created_at"
    )[:5]

    # ==================== ATIVIDADE RECENTE ====================
    recent_activity = []

    # Adiciona contatos recentes
    for contact in contacts.order_by("-updated_at")[:3]:
        recent_activity.append(
            {
                "type": "contact",
                "action": "atualizou",
                "object": f"{contact.name} {contact.surname}",
                "date": contact.updated_at,
                "url": f"/pt/contacts/retrieve/{contact.pk}/",
            }
        )

    # Adiciona interações recentes
    for interaction in interactions.order_by("-updated_at")[:3]:
        recent_activity.append(
            {
                "type": "interaction",
                "action": "registrou",
                "object": f"Interação com {interaction.contact.name} {interaction.contact.surname}",
                "date": interaction.updated_at,
                "url": f"/pt/interations/retrieve/{interaction.pk}/",
            }
        )

    # Adiciona tarefas recentes
    for task in tasks.order_by("-updated_at")[:3]:
        recent_activity.append(
            {
                "type": "task",
                "action": "atualizou",
                "object": f"Tarefa: {task.title}",
                "date": task.updated_at,
                "url": f"/pt/task/retrieve/{task.pk}/",
            }
        )

    # Adiciona oportunidades recentes
    for opp in opportunities.order_by("-updated_at")[:3]:
        recent_activity.append(
            {
                "type": "opportunity",
                "action": "atualizou",
                "object": f"Oportunidade: {opp.name}",
                "date": opp.updated_at,
                "url": f"/pt/opportunities/retrieve/{opp.pk}/",
            }
        )

    # Ordena atividades por data (mais recente primeiro)
    recent_activity.sort(key=lambda x: x["date"], reverse=True)
    recent_activity = recent_activity[:5]

    # ==================== CONTEXTO ====================
    context = {
        # Contatos
        "total_contacts": total_contacts,
        "contacts_with_email": contacts_with_email,
        "contacts_without_email": contacts_without_email,
        "contacts_with_company": contacts_with_company,
        "recent_contacts": recent_contacts,
        # Interações
        "total_interactions": total_interactions,
        "calls_count": calls_count,
        "emails_count": emails_count,
        "meetings_count": meetings_count,
        "recent_interactions": recent_interactions,
        # Tarefas
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "done_tasks": done_tasks,
        "upcoming_tasks": upcoming_tasks,
        "overdue_tasks": overdue_tasks,
        "high_priority_tasks": high_priority_tasks,
        "medium_priority_tasks": medium_priority_tasks,
        "low_priority_tasks": low_priority_tasks,
        # Oportunidades
        "total_opportunities": total_opportunities,
        "prospecting_count": prospecting_count,
        "qualification_count": qualification_count,
        "proposal_count": proposal_count,
        "negotiation_count": negotiation_count,
        "closed_won_count": closed_won_count,
        "closed_lost_count": closed_lost_count,
        "total_opportunity_value": total_opportunity_value,
        "active_opportunities": active_opportunities,
        "recent_opportunities": recent_opportunities,
        # Atividade recente
        "recent_activity": recent_activity,
        # Sistema
        "total_users": User.objects.count(),
        "total_system_contacts": Contact.objects.count(),
    }

    return render(request, "home.html", context)


def sobre_view(request):
    return render(request, "sobre.html", {})
