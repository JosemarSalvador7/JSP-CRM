from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nome"))
    surname = models.CharField(max_length=100, verbose_name=_("Sobrenome"))
    phone = models.CharField(max_length=20, verbose_name=_("Telefone"))
    email = models.EmailField(
        max_length=100, null=True, blank=True, verbose_name=_("E-mail")
    )
    company = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("Empresa")
    )
    job_title = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("Cargo")
    )
    address = models.TextField(null=True, blank=True, verbose_name=_("Endereço"))
    city = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("Cidade")
    )
    state = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("Estado")
    )
    country = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("País")
    )
    postal_code = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("Código Postal")
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="assigned_contacts",
        verbose_name=_("Atribuído a"),
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_contacts",
        verbose_name=_("Criado por"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"
        ordering = ["name"]
