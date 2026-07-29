from django.shortcuts import render, get_object_or_404, redirect
from task.models import Task
from task.forms import TaskForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from fpdf import FPDF
from io import BytesIO

@login_required()
def list_view(request):
    tasks = Task.objects.filter(created_by=request.user).select_related('assigned_to', 'contact')
    
    # Contadores por status
    pending_count = tasks.filter(status='PENDING').count()
    in_progress_count = tasks.filter(status='IN_PROGRESS').count()
    done_count = tasks.filter(status='DONE').count()
    
    # Contadores por prioridade
    high_count = tasks.filter(priority='HIGH').count()
    medium_count = tasks.filter(priority='MEDIUM').count()
    low_count = tasks.filter(priority='LOW').count()
    
    context = {
        'tasks': tasks,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'done_count': done_count,
        'high_count': high_count,
        'medium_count': medium_count,
        'low_count': low_count,
    }
    return render(request, "task_list.html", context)

@login_required()
def retrieve_view(request, id):
    task = get_object_or_404(Task, id=id, created_by=request.user)
    return render(request, "task_retrieve.html", {"task": task})

@login_required()
def post_view(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, _('Tarefa criada com sucesso!'))
            return redirect('tasks:list')
        else:
            messages.error(request, _('Erro ao criar tarefa. Verifique os dados.'))
    else:
        form = TaskForm(user=request.user)
    
    return render(request, 'task_post.html', {'form': form})

@login_required()
def put_view(request, id):
    task = get_object_or_404(Task, id=id, created_by=request.user)
    
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Tarefa atualizada com sucesso!'))
            return redirect('tasks:list')
        else:
            messages.error(request, _('Erro ao atualizar tarefa. Verifique os dados.'))
    else:
        form = TaskForm(instance=task, user=request.user)
    
    return render(request, 'task_post.html', {'form': form})

@login_required()
def delete_view(request, id):
    task = get_object_or_404(Task, id=id, created_by=request.user)
    task.delete()
    messages.success(request, _('Tarefa excluída com sucesso!'))
    return redirect('tasks:list')

@login_required()
def gerar_pdf_tasks(request):
    """Gera PDF com a lista de todas as tarefas do usuário"""
    tasks = Task.objects.filter(created_by=request.user).select_related('assigned_to', 'contact')
    
    pdf = FPDF()
    pdf.add_page(orientation="landscape")
    pdf.set_font("Times", "B", 20)
    pdf.set_fill_color(244, 244, 244)
    pdf.set_title("Lista de Tarefas")
    
    # Título
    pdf.cell(w=120, h=30)
    pdf.cell(w=60, h=0, txt="LISTA DE TAREFAS", ln=1, align="c")
    pdf.set_font("Times", "", 10)
    pdf.cell(w=10, h=10, txt="", ln=1, align="c")
    
    # Cabeçalhos da tabela
    pdf.set_font("Times", "B", 9)
    pdf.cell(w=50, h=10, txt="TÍTULO", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=30, h=10, txt="STATUS", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=30, h=10, txt="PRIORIDADE", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=35, h=10, txt="VENCIMENTO", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=40, h=10, txt="ATRIBUIDO A", border=1, ln=0, align="c", fill=1)
    pdf.cell(w=40, h=10, txt="CONTATO", border=1, ln=1, align="c", fill=1)
    
    # Dados
    pdf.set_font("Times", "", 8)
    for task in tasks:
        # Título (truncado)
        titulo = task.title[:30] + ("..." if len(task.title) > 30 else "")
        pdf.cell(w=50, h=8, txt=titulo, border=1, ln=0, align="l")
        
        # Status
        status_display = dict(Task.STATUS_CHOICES).get(task.status, '')
        pdf.cell(w=30, h=8, txt=status_display, border=1, ln=0, align="c")
        
        # Prioridade
        priority_display = dict(Task.PRIORITY_CHOICES).get(task.priority, '')
        pdf.cell(w=30, h=8, txt=priority_display, border=1, ln=0, align="c")
        
        # Data de Vencimento
        pdf.cell(w=35, h=8, txt=task.due_date.strftime("%d/%m/%Y"), border=1, ln=0, align="c")
        
        # Atribuído a
        atribuido = task.assigned_to.get_full_name() or task.assigned_to.username if task.assigned_to else "Não atribuído"
        pdf.cell(w=40, h=8, txt=atribuido[:20], border=1, ln=0, align="c")
        
        # Contato
        contato = f"{task.contact.name} {task.contact.surname}" if task.contact else "Sem contato"
        pdf.cell(w=40, h=8, txt=contato[:20], border=1, ln=1, align="c")
    
    # Rodapé com total
    pdf.set_font("Times", "I", 8)
    pdf.cell(w=0, h=10, txt=f"Total de tarefas: {tasks.count()}", ln=1, align="R")
    
    pdf_out = pdf.output(dest="S").encode("latin1")
    return FileResponse(BytesIO(pdf_out), filename=f"tarefas_{request.user.username}.pdf")

@login_required()
def retrievepdf_task(request, id):
    """Gera PDF de uma tarefa específica"""
    task = get_object_or_404(Task, id=id, created_by=request.user)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", "B", 24)
    pdf.set_fill_color(244, 244, 244)
    pdf.set_title("Detalhes da Tarefa")
    
    # Título
    pdf.cell(w=60, h=30)
    pdf.cell(w=60, h=0, txt="DETALHES DA TAREFA", ln=1, align="c")
    pdf.set_font("Times", "", 12)
    pdf.cell(w=10, h=10, txt="", ln=1, align="c")
    
    # Título da Tarefa
    pdf.set_font("Times", "B", 16)
    pdf.cell(w=10, h=10, txt=task.title, ln=1, align="c")
    pdf.cell(w=10, h=5, txt="", ln=1, align="c")
    
    # Status e Prioridade
    pdf.set_font("Times", "B", 12)
    pdf.cell(w=30, h=10, txt="Status:", ln=0)
    pdf.set_font("Times", "", 12)
    status_display = dict(Task.STATUS_CHOICES).get(task.status, '')
    pdf.cell(w=50, h=10, txt=status_display, ln=0)
    
    pdf.set_font("Times", "B", 12)
    pdf.cell(w=30, h=10, txt="Prioridade:", ln=0)
    pdf.set_font("Times", "", 12)
    priority_display = dict(Task.PRIORITY_CHOICES).get(task.priority, '')
    pdf.cell(w=50, h=10, txt=priority_display, ln=1)
    
    pdf.cell(w=10, h=5, txt="", ln=1, align="c")
    
    # Data de Vencimento
    pdf.set_font("Times", "B", 12)
    pdf.cell(w=40, h=10, txt="Data de Vencimento:", ln=0)
    pdf.set_font("Times", "", 12)
    pdf.cell(w=50, h=10, txt=task.due_date.strftime("%d/%m/%Y"), ln=1)
    
    pdf.cell(w=10, h=5, txt="", ln=1, align="c")
    
    # Atribuído a
    pdf.set_font("Times", "B", 12)
    pdf.cell(w=40, h=10, txt="Atribuído a:", ln=0)
    pdf.set_font("Times", "", 12)
    atribuido = task.assigned_to.get_full_name() or task.assigned_to.username if task.assigned_to else "Não atribuído"
    pdf.cell(w=50, h=10, txt=atribuido, ln=1)
    
    pdf.cell(w=10, h=5, txt="", ln=1, align="c")
    
    # Contato
    if task.contact:
        pdf.set_font("Times", "B", 12)
        pdf.cell(w=40, h=10, txt="Contato:", ln=0)
        pdf.set_font("Times", "", 12)
        contato_nome = f"{task.contact.name} {task.contact.surname}"
        pdf.cell(w=50, h=10, txt=contato_nome, ln=1)
        
        pdf.set_font("Times", "", 10)
        pdf.cell(w=40, h=8, txt=f"Telefone: {task.contact.phone}", ln=1)
        if task.contact.email:
            pdf.cell(w=40, h=8, txt=f"Email: {task.contact.email}", ln=1)
    
    pdf.cell(w=10, h=5, txt="", ln=1, align="c")
    
    # Descrição
    pdf.set_font("Times", "B", 14)
    pdf.cell(w=10, h=10, txt="Descrição", ln=1, align="c")
    pdf.set_font("Times", "", 11)
    
    # Quebra a descrição em várias linhas
    descricao_lines = task.description.split('\n')
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
    criado_por = task.created_by.get_full_name() or task.created_by.username
    pdf.cell(w=80, h=8, txt=criado_por, ln=1)
    
    pdf.set_font("Times", "B", 11)
    pdf.cell(w=40, h=8, txt="Criado em:", ln=0)
    pdf.set_font("Times", "", 11)
    pdf.cell(w=80, h=8, txt=task.created_at.strftime("%d/%m/%Y %H:%M"), ln=1)
    
    pdf.set_font("Times", "B", 11)
    pdf.cell(w=40, h=8, txt="Atualizado em:", ln=0)
    pdf.set_font("Times", "", 11)
    pdf.cell(w=80, h=8, txt=task.updated_at.strftime("%d/%m/%Y %H:%M"), ln=1)
    
    pdf_out = pdf.output(dest="S").encode("latin1")
    nome_arquivo = f"tarefa_{task.title[:30]}.pdf"
    return FileResponse(BytesIO(pdf_out), filename=nome_arquivo)