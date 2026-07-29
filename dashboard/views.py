from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import timedelta

from contacts.models import Contact
from interations.models import Interaction
from task.models import Task
from opportunities.models import Opportunity  # 🔥 Adicionar import

# Create your views here.


@login_required(login_url="accounts:login")
def home_view(request):
    # Dados do usuário atual
    user = request.user

    # ==================== CONTATOS ====================
    total_contacts = Contact.objects.filter(created_by=user).count()
    contacts_with_email = (
        Contact.objects.filter(created_by=user)
        .filter(Q(email__isnull=False) & ~Q(email=""))
        .count()
    )
    contacts_without_email = (
        Contact.objects.filter(created_by=user)
        .filter(Q(email__isnull=True) | Q(email=""))
        .count()
    )
    contacts_with_company = (
        Contact.objects.filter(created_by=user)
        .filter(Q(company__isnull=False) & ~Q(company=""))
        .count()
    )

    # Últimos contatos adicionados
    recent_contacts = Contact.objects.filter(created_by=user).order_by("-created_at")[
        :5
    ]

    # ==================== INTERAÇÕES ====================
    total_interactions = Interaction.objects.filter(created_by=user).count()
    calls_count = Interaction.objects.filter(
        created_by=user, type_interaction="C"
    ).count()
    emails_count = Interaction.objects.filter(
        created_by=user, type_interaction="E"
    ).count()
    meetings_count = Interaction.objects.filter(
        created_by=user, type_interaction="M"
    ).count()

    # Últimas interações
    recent_interactions = (
        Interaction.objects.filter(created_by=user)
        .select_related("contact")
        .order_by("-date_time")[:5]
    )

    # ==================== TAREFAS ====================
    total_tasks = Task.objects.filter(created_by=user).count()
    pending_tasks = Task.objects.filter(created_by=user, status="PENDING").count()
    in_progress_tasks = Task.objects.filter(
        created_by=user, status="IN_PROGRESS"
    ).count()
    done_tasks = Task.objects.filter(created_by=user, status="DONE").count()

    # Tarefas com vencimento próximo (próximos 7 dias)
    today = timezone.now().date()
    next_week = today + timedelta(days=7)
    upcoming_tasks = Task.objects.filter(
        created_by=user,
        due_date__gte=today,
        due_date__lte=next_week,
        status__in=["PENDING", "IN_PROGRESS"],
    ).order_by("due_date")[:5]

    # Tarefas atrasadas
    overdue_tasks = Task.objects.filter(
        created_by=user, due_date__lt=today, status__in=["PENDING", "IN_PROGRESS"]
    ).order_by("due_date")[:5]

    # Estatísticas de tarefas por prioridade
    high_priority_tasks = Task.objects.filter(created_by=user, priority="HIGH").count()
    medium_priority_tasks = Task.objects.filter(
        created_by=user, priority="MEDIUM"
    ).count()
    low_priority_tasks = Task.objects.filter(created_by=user, priority="LOW").count()

    # ==================== OPORTUNIDADES ====================
    total_opportunities = Opportunity.objects.filter(created_by=user).count()

    # Oportunidades por estágio
    prospecting_count = Opportunity.objects.filter(
        created_by=user, stage="PROSPECTING"
    ).count()
    qualification_count = Opportunity.objects.filter(
        created_by=user, stage="QUALIFICATION"
    ).count()
    proposal_count = Opportunity.objects.filter(
        created_by=user, stage="PROPOSAL"
    ).count()
    negotiation_count = Opportunity.objects.filter(
        created_by=user, stage="NEGOTIATION"
    ).count()
    closed_won_count = Opportunity.objects.filter(
        created_by=user, stage="CLOSED_WON"
    ).count()
    closed_lost_count = Opportunity.objects.filter(
        created_by=user, stage="CLOSED_LOST"
    ).count()

    # Valor total das oportunidades
    total_opportunity_value = (
        Opportunity.objects.filter(created_by=user).aggregate(Sum("value"))[
            "value__sum"
        ]
        or 0
    )

    # Oportunidades em andamento (excluindo fechadas)
    active_opportunities = (
        Opportunity.objects.filter(created_by=user)
        .exclude(stage__in=["CLOSED_WON", "CLOSED_LOST"])
        .count()
    )

    # Últimas oportunidades adicionadas
    recent_opportunities = (
        Opportunity.objects.filter(created_by=user)
        .select_related("contact")
        .order_by("-created_at")[:5]
    )

    # ==================== ATIVIDADE RECENTE ====================
    recent_activity = []

    # Adiciona contatos recentes
    for contact in Contact.objects.filter(created_by=user).order_by("-updated_at")[:3]:
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
    for interaction in Interaction.objects.filter(created_by=user).order_by(
        "-updated_at"
    )[:3]:
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
    for task in Task.objects.filter(created_by=user).order_by("-updated_at")[:3]:
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
    for opp in Opportunity.objects.filter(created_by=user).order_by("-updated_at")[:3]:
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
