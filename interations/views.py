from django.shortcuts import render, get_object_or_404, redirect
from interations.models import Interaction
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from interations.forms import InteractionForm
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from fpdf import FPDF
from io import BytesIO

@login_required()
def list_view(request):
    interactions = Interaction.objects.filter(created_by=request.user).select_related('contact', 'created_by')
    
    # Contadores por tipo
    calls_count = interactions.filter(type_interaction='C').count()
    emails_count = interactions.filter(type_interaction='E').count()
    meetings_count = interactions.filter(type_interaction='M').count()
    
    context = {
        'interactions': interactions,
        'calls_count': calls_count,
        'emails_count': emails_count,
        'meetings_count': meetings_count,
    }
    return render(request, "interaction_list.html", context)

@login_required()
def retrieve_view(request, id):
    interaction = get_object_or_404(Interaction, id=id, created_by=request.user)
    return render(request, "interaction_retrieve.html", {"interaction": interaction})

@login_required()
def put_view(request, id):
    interaction = get_object_or_404(Interaction, id=id, created_by=request.user)
    if request.method == "POST":
        form = InteractionForm(request.POST, instance=interaction)
        if form.is_valid():
            form.save()
            messages.success(request, _('Interação atualizada com sucesso'))
            return redirect('interations:list')
        else:
            messages.error(request, _('Erro ao atualizar interação'))
    else:
        form = InteractionForm(instance=interaction)
    return render(request, 'interaction_post.html', {'form': form})

@login_required()
def post_view(request):
    if request.method == "POST":
        form = InteractionForm(request.POST)
        if form.is_valid():
            form_interaction = form.save(commit=False)
            form_interaction.created_by = request.user
            form_interaction.save()
            messages.success(request, _('Interação cadastrada com sucesso'))
            return redirect('interations:list')
        else:
            messages.error(request, _('Erro ao cadastrar interação'))
    else:
        form = InteractionForm()
    return render(request, 'interaction_post.html', {'form': form})

@login_required()
def delete_view(request, id):
    interaction = get_object_or_404(Interaction, id=id, created_by=request.user)
    interaction.delete()
    messages.success(request, _("Interação deletada com sucesso"))
    return redirect("interations:list")

@login_required()
def gerar_pdf_interactions(request):
    """Gera PDF com a lista de todas as interações do usuário"""
    interactions = Interaction.objects.filter(created_by=request.user).select_related('contact', 'created_by')
    
    pdf = FPDF()
    pdf.add_page(orientation="landscape")
    pdf.set_font("Times", "B", 20)
    pdf.set_fill_color(244, 244, 244)
    pdf.set_title("Lista de Interações")
    
    # Título
    pdf.cell(w=120, h=30)
    pdf.cell(w=60, h=0, txt="LISTA DE INTERAÇÕES", ln=1, align="c")
    pdf.set_font("Times", "", 10)
    pdf.cell(w=10, h=10, txt="", ln=1, align="c")
    
    # Cabeçalhos da tabela
    pdf.set_font("Times", "B", 9)
    pdf.cell(w=30, h=10, txt="TIPO", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=50, h=10, txt="CONTATO", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=40, h=10, txt="DATA/HORA", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=80, h=10, txt="DESCRIÇÃO", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=40, h=10, txt="CRIADO POR", border=1, ln=1, align="c", fill=1)
    
    # Dados
    pdf.set_font("Times", "", 8)
    for interaction in interactions:
        # Tipo
        tipo_display = dict(Interaction.interaction_choices).get(interaction.type_interaction, '')
        pdf.cell(w=30, h=8, txt=f"{tipo_display}", border=1, ln=0, align="c")
        
        # Contato
        nome_contato = f"{interaction.contact.name} {interaction.contact.surname}"
        pdf.cell(w=50, h=8, txt=nome_contato[:25], border=1, ln=0, align="c")
        
        # Data/Hora
        pdf.cell(w=40, h=8, txt=interaction.date_time.strftime("%d/%m/%Y %H:%M"), border=1, ln=0, align="c")
        
        # Descrição (truncada)
        descricao = interaction.description[:60] + ("..." if len(interaction.description) > 60 else "")
        pdf.cell(w=80, h=8, txt=descricao, border=1, ln=0, align="l")
        
        # Criado por
        criado_por = interaction.created_by.get_full_name() or interaction.created_by.username
        pdf.cell(w=40, h=8, txt=criado_por[:20], border=1, ln=1, align="c")
    
    # Rodapé com total
    pdf.set_font("Times", "I", 8)
    pdf.cell(w=0, h=10, txt=f"Total de interações: {interactions.count()}", ln=1, align="R")
    
    pdf_out = pdf.output(dest="S").encode("latin1")
    return FileResponse(BytesIO(pdf_out), filename=f"interacoes_{request.user.username}.pdf")

@login_required()
def retrievepdf_interaction(request, id):
    """Gera PDF de uma interação específica"""
    interaction = get_object_or_404(Interaction, id=id, created_by=request.user)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", "B", 24)
    pdf.set_fill_color(244, 244, 244)
    pdf.set_title("Detalhes da Interação")
    
    # Título
    pdf.cell(w=60, h=30)
    pdf.cell(w=60, h=0, txt="DETALHES DA INTERAÇÃO", ln=1, align="c")
    pdf.set_font("Times", "", 12)
    pdf.cell(w=10, h=10, txt="", ln=1, align="c")
    
    # Tipo e Data
    pdf.set_font("Times", "B", 14)
    pdf.cell(w=10, h=10, txt="Tipo de Interação", ln=1, align="c")
    pdf.set_font("Times", "", 12)
    tipo_display = dict(Interaction.interaction_choices).get(interaction.type_interaction, '')
    pdf.cell(w=10, h=10, txt=f"{tipo_display}", ln=1, align="c")
    pdf.cell(w=10, h=5, txt="", ln=1, align="c")
    
    # Data/Hora
    pdf.set_font("Times", "B", 14)
    pdf.cell(w=10, h=10, txt="Data/Hora", ln=1, align="c")
    pdf.set_font("Times", "", 12)
    pdf.cell(w=10, h=10, txt=interaction.date_time.strftime("%d/%m/%Y às %H:%M"), ln=1, align="c")
    pdf.cell(w=10, h=5, txt="", ln=1, align="c")
    
    # Contato
    pdf.set_font("Times", "B", 14)
    pdf.cell(w=10, h=10, txt="Contato", ln=1, align="c")
    pdf.set_font("Times", "", 12)
    nome_contato = f"{interaction.contact.name.capitalize()} {interaction.contact.surname.capitalize()}"
    pdf.cell(w=10, h=10, txt=f"{nome_contato}", ln=1, align="c")
    pdf.set_font("Times", "", 10)
    pdf.cell(w=10, h=8, txt=f"Telefone: {interaction.contact.phone}", ln=1, align="c")
    if interaction.contact.email:
        pdf.cell(w=10, h=8, txt=f"Email: {interaction.contact.email}", ln=1, align="c")
    pdf.cell(w=10, h=5, txt="", ln=1, align="c")
    
    # Descrição
    pdf.set_font("Times", "B", 14)
    pdf.cell(w=10, h=10, txt="Descrição", ln=1, align="c")
    pdf.set_font("Times", "", 11)
    
    # Quebra a descrição em várias linhas
    descricao_lines = interaction.description.split('\n')
    for line in descricao_lines:
        pdf.multi_cell(w=180, h=7, txt=line, align="L", border=0)
    
    pdf.cell(w=10, h=5, txt="", ln=1, align="c")
    
    # Informações do Sistema
    pdf.set_font("Times", "B", 14)
    pdf.cell(w=10, h=10, txt="Informações do Sistema", ln=1, align="c")
    pdf.cell(w=10, h=3, txt="", ln=1, align="c")
    
    pdf.set_font("Times", "B", 11)
    pdf.cell(w=40, h=8, txt="Criado por:", ln=0)
    pdf.set_font("Times", "", 11)
    criado_por = interaction.created_by.get_full_name() or interaction.created_by.username
    pdf.cell(w=80, h=8, txt=f"{criado_por}", ln=1)
    
    pdf.set_font("Times", "B", 11)
    pdf.cell(w=40, h=8, txt="Criado em:", ln=0)
    pdf.set_font("Times", "", 11)
    pdf.cell(w=80, h=8, txt=interaction.created_at.strftime("%d/%m/%Y %H:%M"), ln=1)
    
    pdf.set_font("Times", "B", 11)
    pdf.cell(w=40, h=8, txt="Atualizado em:", ln=0)
    pdf.set_font("Times", "", 11)
    pdf.cell(w=80, h=8, txt=interaction.updated_at.strftime("%d/%m/%Y %H:%M"), ln=1)
    
    pdf_out = pdf.output(dest="S").encode("latin1")
    nome_arquivo = f"interacao_{interaction.contact.name}_{interaction.contact.surname}.pdf"
    return FileResponse(BytesIO(pdf_out), filename=nome_arquivo)