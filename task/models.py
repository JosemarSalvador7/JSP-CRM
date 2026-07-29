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

    title = models.CharField(max_length=250)  # ❌ Estava faltando max_length
    description = models.TextField()  # ❌ Estava faltando os parênteses
    due_date = models.DateField()  # ❌ Estava faltando os parênteses
    priority = models.CharField(
        max_length=30,
        choices=PRIORITY_CHOICES,
        default="MEDIUM",  # Adicionar valor padrão
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="PENDING",
    )
    assigned_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tasks_assigned",  # Adicionar related_name
    )
    created_by = models.ForeignKey(  # Adicionar campo created_by
        User, on_delete=models.CASCADE, related_name="tasks_created"
    )
    contact = models.ForeignKey(
        Contact, null=True, blank=True, on_delete=models.CASCADE, related_name="tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"
