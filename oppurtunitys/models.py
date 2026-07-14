from django.db import models
from django.contrib.auth.models import User
from contacts.models import Contact
from django.db.models.functions import Now


#  PROSPECTING, QUALIFICATION, PROPOSAL, NEGOTIATION, CLOSED_WON, CLOSED_LOST
# Create your models here.
class Oppurtunity(models.Model):
    opu_choices = (
        ("PROSPECTING", "PROSPECTING"),
        ("QUALIFICATION", "QUALIFICATION"),
        ("PROPOSAL", "PROPOSAL"),
        ("NEGOTIATION", "NEGOTIATION"),
        ("CLOSED_WON", "CLOSED_WON"),
        ("CLOSED_LOST", "CLOSED_LOST"),
    )
    name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    stage = models.CharField(max_length=50, choices=opu_choices)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.updated_at = Now()
        super().save(*args, **kwargs)
