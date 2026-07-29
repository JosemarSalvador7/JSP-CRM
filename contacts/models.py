from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome", validators=[])
    surname = models.CharField(max_length=100, verbose_name="Sobrenome")
    phone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(
        max_length=100, null=True, blank=True, verbose_name="E-mail"
    )
    company = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Empresa"
    )
    job_title = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Cargo"
    )
    address = models.TextField(null=True, blank=True, verbose_name="Endereço")
    city = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Cidade"
    )
    state = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Estado"
    )
    country = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="País"
    )
    postal_code = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Código Postal"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="assigned_contacts",
        verbose_name="Atribuído a",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_contacts",
        verbose_name="Criado por",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"
        ordering = ["name"]  # Adicionado para ordenar por nome
