from django.contrib import admin
from clientes.models import Cliente


# Register your models here.
@admin.register(Cliente)
class Clientes(admin.ModelAdmin):
    list_display = ["name", "surname", "phone", "job_title",]
    search_fields = [
        "name",
        "job_title",
        "company",
    ]
    ordering = [
        "name",
        "surname",
    ]
    empty_value_display = "-empty-"
