from django.db import models
from django.contrib.auth.models import User
from contacts.models import Contact

# Create your models here.


class Opportunity(models.Model):
    STAGE_CHOICES = (
        ("PROSPECTING", "Prospecção"),
        ("QUALIFICATION", "Qualificação"),
        ("PROPOSAL", "Proposta"),
        ("NEGOTIATION", "Negociação"),
        ("CLOSED_WON", "Fechada Ganha"),
        ("CLOSED_LOST", "Fechada Perdida"),
    )

    name = models.CharField(max_length=255, verbose_name="Nome")
    value = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="Valor Estimado"
    )
    stage = models.CharField(
        max_length=50,
        choices=STAGE_CHOICES,
        default="PROSPECTING",
        verbose_name="Estágio",
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        verbose_name="Contato",
        related_name="opportunities",
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Atribuído a/ao",
        related_name="opportunities_assigned",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Criado por",
        related_name="opportunities_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_stage_display()}"  # type: ignore

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Oportunidade"
        verbose_name_plural = "Oportunidades"
