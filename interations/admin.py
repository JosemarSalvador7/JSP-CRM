from django.contrib import admin
from interations.models import Interaction


# Register your models here.
@admin.register(Interaction)
class InteractionModel(admin.ModelAdmin):
    list_display = [
        "type_interaction",
        "created_by",
        "contact__name",
        "date_time",
        "description",
    ]
    search_fields = [
        "contact__name",
    ]
    list_filter = [
        "type_interaction",
    ]
    empty_value_display = "-empty-"
