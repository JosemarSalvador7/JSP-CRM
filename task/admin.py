from django.contrib import admin
from task.models import Task


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = [
        "title",
        "status",
        "due_date",
    ]
    list_display = ["title", "status", "contact", "due_date", "priority", "created_by"]
    list_filter = ["status", "priority"]
    ordering = ["due_date"]
    empty_value_display = "-empty-"
