from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    """Профиль пользователя"""
    list_display = ('__str__',)
