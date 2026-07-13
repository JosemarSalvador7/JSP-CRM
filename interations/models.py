from django.db import models
from django.contrib.auth.models import User

from contacts.models import Contact


# Create your models here.
class Interation(models.Model):
    interaction_choices = (
        ("C", "CALL"),
        ("E", "EMAIL"),
        ("M", "MEETING"),
        ("O", "OTHER"),
    )
    type_interaction = models.CharField(max_length=50, choices=interaction_choices)
    date_time = models.DateTimeField()
    description = models.TextField()
    # models contact
    contact = models.ForeignKey(Contact, on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
