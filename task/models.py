from django.db import models

from contacts.models import Contact
from django.contrib.auth.models import User
from django.db.models.functions import Now
# Create your models here.

class Task(models.Model):
    title = models.CharField
    description = models.TextField
    due_date = models.DateField
    priority = models.CharField(
        max_length=30, choices=(("LOW", "LOW"), ("MEDIUM", "MEDIUM"), ("HIGH", "HIGH"))
    )
    status = models.CharField(
        max_length=30,
        choices=(
            ("PENDING", "PENDING"),
            ("IN_PROGRESS", "IN_PROGRESS"),
            ("DONE", "DONE"),
        ),
    )
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL)
    contact = models.ForeignKey(
        Contact, null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = Now()
        super().save(*args, **kwargs)

