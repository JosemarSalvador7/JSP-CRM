from django.contrib import admin

from opportunities.models import Opportunity


# Register your models here.
@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    search_fields = ["name", "stage", "assigned_to", "contact__user__name"]
    list_display = ["name", "stage", "value", "contact", "assigned_to", "created_by"]
    list_filter = [
        "stage",
    ]
    ordering = ["created_at"]
