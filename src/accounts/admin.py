from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


@admin.register(models.AppUser)
class AppUserAdmin(UserAdmin):
    model = models.AppUser
    list_display = (
        'username', 'email', 'role', 'email_verified', 'is_active', 'is_staff', 'is_superuser', 'created'
    )
    list_filter = ('role', 'is_active', 'is_staff', 'email_verified')
    search_fields = ('username', 'email')
    ordering = ('-created',)
    readonly_fields = ('created', 'updated')

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
        (None, {'fields': ('email_verified',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
        (None, {'fields': ('email_verified',)}),
    )
