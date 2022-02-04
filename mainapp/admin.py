from django.contrib import admin

from .models import Profile, Relationship


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    """Профиль пользователя"""
    list_display = ('__str__',)


@admin.register(Relationship)
class RelationshipModelAdmin(admin.ModelAdmin):
    """Симпатии пользователя"""
    list_display = ('__str__',)
