# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from opportunities.models import Opportunity
from opportunities.forms import OpportunityForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.http import FileResponse
from fpdf import FPDF
from io import BytesIO


@login_required()
def list_view(request):
    """Lista todas as oportunidades com filtros"""
    opportunities = Opportunity.objects.filter(created_by=request.user).select_related(
        "contact", "assigned_to", "created_by"
    )

    # Filtro por estágio
    stage_filter = request.GET.get("stage", "")
    if stage_filter:
        opportunities = opportunities.filter(stage=stage_filter)

    # Filtro por contato
    contact_filter = request.GET.get("contact", "")
    if contact_filter:
        opportunities = opportunities.filter(contact_id=contact_filter)

    # Filtro por nome
    search = request.GET.get("search", "")
    if search:
        opportunities = opportunities.filter(
            Q(name__icontains=search)
            | Q(contact__name__icontains=search)
            | Q(contact__surname__icontains=search)
        )

    # Estatísticas por estágio (para o Kanban)
    stages = dict(Opportunity.STAGE_CHOICES)
    stage_counts = {}
    stage_values = {}

    for stage_code, stage_label in stages.items():
        stage_opportunities = opportunities.filter(stage=stage_code)
        stage_counts[stage_code] = stage_opportunities.count()
        stage_values[stage_code] = (
            stage_opportunities.aggregate(Sum("value"))["value__sum"] or 0
        )

    # Total de oportunidades e valor total
    total_value = opportunities.aggregate(Sum("value"))["value__sum"] or 0

    context = {
        "opportunities": opportunities,
        "stage_counts": stage_counts,
        "stage_values": stage_values,
        "stages": stages,
        "total_count": opportunities.count(),
        "total_value": total_value,
        "stage_filter": stage_filter,
        "contact_filter": contact_filter,
        "search": search,
    }
    return render(request, "opportunity_list.html", context)


@login_required()
def kanban_view(request):
    """Visualização Kanban das oportunidades"""
    opportunities = Opportunity.objects.filter(created_by=request.user).select_related(
        "contact", "assigned_to"
    )

    # Organiza por estágio
    stages = dict(Opportunity.STAGE_CHOICES)
    kanban_data = {}

    for stage_code, stage_label in stages.items():
        kanban_data[stage_code] = {
            "label": stage_label,
            "opportunities": opportunities.filter(stage=stage_code),
            "count": opportunities.filter(stage=stage_code).count(),
            "total_value": opportunities.filter(stage=stage_code).aggregate(
                Sum("value")
            )["value__sum"]
            or 0,
        }

    # Filtro por contato
    contact_filter = request.GET.get("contact", "")
    if contact_filter:
        for stage in kanban_data:
            kanban_data[stage]["opportunities"] = kanban_data[stage][
                "opportunities"
            ].filter(contact_id=contact_filter)
            kanban_data[stage]["count"] = kanban_data[stage]["opportunities"].count()

    context = {
        "kanban_data": kanban_data,
        "stages": stages,
        "contact_filter": contact_filter,
        "total_opportunities": Opportunity.objects.filter(
            created_by=request.user
        ).count(),
    }
    return render(request, "opportunity_kanban.html", context)


@login_required()
def retrieve_view(request, id):
    opportunity = get_object_or_404(Opportunity, id=id, created_by=request.user)
    return render(request, "opportunity_retrieve.html", {"opportunity": opportunity})


@login_required()
def post_view(request):
    if request.method == "POST":
        form = OpportunityForm(request.POST, user=request.user)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.created_by = request.user
            opportunity.save()
            messages.success(request, _("Oportunidade criada com sucesso!"))
            return redirect("opportunities:list")
        else:
            messages.error(
                request, _("Erro ao criar oportunidade. Verifique os dados.")
            )
    else:
        form = OpportunityForm(user=request.user)

    return render(request, "opportunity_post.html", {"form": form})


@login_required()
def put_view(request, id):
    opportunity = get_object_or_404(Opportunity, id=id, created_by=request.user)

    if request.method == "POST":
        form = OpportunityForm(request.POST, instance=opportunity, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Oportunidade atualizada com sucesso!"))
            return redirect("opportunities:list")
        else:
            messages.error(
                request, _("Erro ao atualizar oportunidade. Verifique os dados.")
            )
    else:
        form = OpportunityForm(instance=opportunity, user=request.user)

    return render(request, "opportunity_post.html", {"form": form})


@login_required()
def delete_view(request, id):
    opportunity = get_object_or_404(Opportunity, id=id, created_by=request.user)
    opportunity.delete()
    messages.success(request, _("Oportunidade excluída com sucesso!"))
    return redirect("opportunities:list")


@login_required()
def update_stage_view(request, id):
    """Atualiza apenas o estágio da oportunidade (para o Kanban)"""
    opportunity = get_object_or_404(Opportunity, id=id, created_by=request.user)

    if request.method == "POST":
        new_stage = request.POST.get("stage")
        if new_stage in dict(Opportunity.STAGE_CHOICES):
            opportunity.stage = new_stage
            opportunity.save()
            messages.success(request, _("Estágio atualizado com sucesso!"))
        else:
            messages.error(request, _("Estágio inválido."))

    return redirect("opportunities:list")


@login_required()
def gerar_pdf_opportunities(request):
    """Gera PDF com a lista de todas as oportunidades"""
    opportunities = Opportunity.objects.filter(created_by=request.user).select_related(
        "contact", "assigned_to"
    )

    pdf = FPDF()
    pdf.add_page(orientation="landscape")
    pdf.set_font("Times", "B", 20)
    pdf.set_fill_color(244, 244, 244)
    pdf.set_title("Lista de Oportunidades")

    # Título
    pdf.cell(w=120, h=30)
    pdf.cell(w=60, h=0, txt="LISTA DE OPORTUNIDADES", ln=1, align="c")
    pdf.set_font("Times", "", 10)
    pdf.cell(w=10, h=10, txt="", ln=1, align="c")

    # Cabeçalhos da tabela
    pdf.set_font("Times", "B", 9)
    pdf.cell(w=50, h=10, txt="NOME", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=35, h=10, txt="VALOR", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=40, h=10, txt="ESTÁGIO", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=45, h=10, txt="CONTATO", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=40, h=10, txt="ATRIBUIDO A", border=1, ln=1, align="c", fill=1)

    # Dados
    pdf.set_font("Times", "", 8)
    for opp in opportunities:
        # Nome (truncado)
        nome = opp.name[:25] + ("..." if len(opp.name) > 25 else "")
        pdf.cell(w=50, h=8, txt=nome, border=1, ln=0, align="l")

        # Valor
        pdf.cell(
            w=35,
            h=8,
            txt=f"R$ {opp.value:,.2f}".replace(",", "."),
            border=1,
            ln=0,
            align="r",
        )

        # Estágio
        stage_display = dict(Opportunity.STAGE_CHOICES).get(opp.stage, "")
        pdf.cell(w=40, h=8, txt=stage_display, border=1, ln=0, align="c")

        # Contato
        contato = (
            f"{opp.contact.name} {opp.contact.surname}"
            if opp.contact
            else "Sem contato"
        )
        pdf.cell(w=45, h=8, txt=contato[:20], border=1, ln=0, align="c")

        # Atribuído a
        atribuido = (
            opp.assigned_to.get_full_name() or opp.assigned_to.username
            if opp.assigned_to
            else "Não atribuído"
        )
        pdf.cell(w=40, h=8, txt=atribuido[:20], border=1, ln=1, align="c")

    # Rodapé com totais
    pdf.set_font("Times", "I", 8)
    total_value = opportunities.aggregate(Sum("value"))["value__sum"] or 0
    pdf.cell(
        w=0,
        h=10,
        txt=f"Total de oportunidades: {opportunities.count()} | Valor total: R$ {total_value:,.2f}".replace(
            ",", "."
        ),
        ln=1,
        align="R",
    )

    pdf_out = pdf.output(dest="S").encode("latin1")
    return FileResponse(
        BytesIO(pdf_out), filename=f"oportunidades_{request.user.username}.pdf"
    )


@login_required()
def retrievepdf_opportunity(request, id):
    """Gera PDF de uma oportunidade específica"""
    opportunity = get_object_or_404(Opportunity, id=id, created_by=request.user)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", "B", 24)
    pdf.set_fill_color(244, 244, 244)
    pdf.set_title("Detalhes da Oportunidade")

    # Título
    pdf.cell(w=60, h=30)
    pdf.cell(w=60, h=0, txt="DETALHES DA OPORTUNIDADE", ln=1, align="c")
    pdf.set_font("Times", "", 12)
    pdf.cell(w=10, h=10, txt="", ln=1, align="c")

    # Nome da Oportunidade
    pdf.set_font("Times", "B", 16)
    pdf.cell(w=10, h=10, txt=opportunity.name, ln=1, align="c")
    pdf.cell(w=10, h=5, txt="", ln=1, align="c")

    # Valor
    pdf.set_font("Times", "B", 12)
    pdf.cell(w=40, h=10, txt="Valor Estimado:", ln=0)
    pdf.set_font("Times", "", 12)
    pdf.cell(w=50, h=10, txt=f"R$ {opportunity.value:,.2f}".replace(",", "."), ln=1)

    pdf.cell(w=10, h=5, txt="", ln=1, align="c")

    # Estágio
    pdf.set_font("Times", "B", 12)
    pdf.cell(w=40, h=10, txt="Estágio:", ln=0)
    pdf.set_font("Times", "", 12)
    stage_display = dict(Opportunity.STAGE_CHOICES).get(opportunity.stage, "")
    pdf.cell(w=50, h=10, txt=stage_display, ln=1)

    pdf.cell(w=10, h=5, txt="", ln=1, align="c")

    # Contato
    pdf.set_font("Times", "B", 12)
    pdf.cell(w=40, h=10, txt="Contato:", ln=0)
    pdf.set_font("Times", "", 12)
    contato_nome = f"{opportunity.contact.name} {opportunity.contact.surname}"
    pdf.cell(w=50, h=10, txt=contato_nome, ln=1)

    pdf.set_font("Times", "", 10)
    pdf.cell(w=40, h=8, txt=f"Telefone: {opportunity.contact.phone}", ln=1)
    if opportunity.contact.email:
        pdf.cell(w=40, h=8, txt=f"Email: {opportunity.contact.email}", ln=1)

    pdf.cell(w=10, h=5, txt="", ln=1, align="c")

    # Atribuído a
    pdf.set_font("Times", "B", 12)
    pdf.cell(w=40, h=10, txt="Atribuído a:", ln=0)
    pdf.set_font("Times", "", 12)
    atribuido = (
        opportunity.assigned_to.get_full_name() or opportunity.assigned_to.username
        if opportunity.assigned_to
        else "Não atribuído"
    )
    pdf.cell(w=50, h=10, txt=atribuido, ln=1)

    pdf.cell(w=10, h=5, txt="", ln=1, align="c")

    # Informações do Sistema
    pdf.set_font("Times", "B", 14)
    pdf.cell(w=10, h=10, txt="Informações do Sistema", ln=1, align="c")
    pdf.cell(w=10, h=3, txt="", ln=1, align="c")

    pdf.set_font("Times", "B", 11)
    pdf.cell(w=40, h=8, txt="Criado por:", ln=0)
    pdf.set_font("Times", "", 11)
    criado_por = (
        opportunity.created_by.get_full_name() or opportunity.created_by.username
    )
    pdf.cell(w=80, h=8, txt=criado_por, ln=1)

    pdf.set_font("Times", "B", 11)
    pdf.cell(w=40, h=8, txt="Criado em:", ln=0)
    pdf.set_font("Times", "", 11)
    pdf.cell(w=80, h=8, txt=opportunity.created_at.strftime("%d/%m/%Y %H:%M"), ln=1)

    pdf.set_font("Times", "B", 11)
    pdf.cell(w=40, h=8, txt="Atualizado em:", ln=0)
    pdf.set_font("Times", "", 11)
    pdf.cell(w=80, h=8, txt=opportunity.updated_at.strftime("%d/%m/%Y %H:%M"), ln=1)

    pdf_out = pdf.output(dest="S").encode("latin1")
    nome_arquivo = f"oportunidade_{opportunity.name[:30]}.pdf"
    return FileResponse(BytesIO(pdf_out), filename=nome_arquivo)
