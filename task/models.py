from django.db import models
from contacts.models import Contact
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("LOW", "Baixa"),
        ("MEDIUM", "Média"),
        ("HIGH", "Alta"),
    )

    STATUS_CHOICES = (
        ("PENDING", "Pendente"),
        ("IN_PROGRESS", "Em Andamento"),
        ("DONE", "Concluída"),
    )

    title = models.CharField(max_length=250, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    due_date = models.DateField(verbose_name="Data de Vencimento")
    priority = models.CharField(
        max_length=30,
        choices=PRIORITY_CHOICES,
        default="MEDIUM",
        verbose_name="Prioridade",
    )
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default="PENDING", verbose_name="Status"
    )
    assigned_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tasks_assigned",
        verbose_name="Atribuído a",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks_created",
        verbose_name="Criado por",
    )
    contact = models.ForeignKey(
        Contact,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Contato",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"
