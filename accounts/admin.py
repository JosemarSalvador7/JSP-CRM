from django.contrib import admin

from accounts.models import Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["avatar", "code", "role"]
    search_fields = ["code", "role"]
