from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Now


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=100, null=True, blank=True)
    assigned_to = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="cliente"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="clientes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.updated_at = Now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return self.name
