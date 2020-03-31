from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Профиль"""
    list_display = ('id', 'user')
    list_display_links = ("user",)
