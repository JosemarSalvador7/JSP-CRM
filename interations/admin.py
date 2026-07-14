from django.contrib import admin
from interations.models import Interation


# Register your models here.
@admin.register(Interation)
class InterationModel(admin.ModelAdmin):
    search_fields = ["type"]
