from django.contrib import admin
from interations.models import Interaction


# Register your models here.
@admin.register(Interaction)
class InteractionModel(admin.ModelAdmin):
    search_fields = ["type"]
