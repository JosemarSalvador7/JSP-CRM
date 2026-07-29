from django.db import models
from django.contrib.auth.models import User
from contacts.models import Contact


# Create your models here.
class Interaction(models.Model):
    interaction_choices = (
        ("C", "Ligação"),
        ("E", "E-mail"),
        ("M", "Reunião"),
        ("O", "Reunião"),
    )
    type_interaction = models.CharField(
        max_length=50, choices=interaction_choices, verbose_name="Tipo de Interação"
    )
    date_time = models.DateTimeField(verbose_name="Data e Hora")
    description = models.TextField(verbose_name="Descrição")
    # models contact
    contact = models.ForeignKey(
        Contact, on_delete=models.DO_NOTHING, verbose_name="Contato"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Criado por",
        related_name="interaction",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    def __str__(self):
        return f"{self.get_type_interaction_display()} | {self.contact.name if self.contact else 'Sem contato'}"  # type:ignore

    class Meta:
        verbose_name = "Interação"
        verbose_name_plural = "Interações"
