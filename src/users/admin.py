from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin


@admin.register(models.AppUser)
class AppUserAdmin(UserAdmin):
    model = models.AppUser
    list_display = ('username', 'email', 'role', 'email_verified', 'is_active', 'is_staff', 'is_superuser', 'created',)
    list_filter = ('role', 'is_active', 'is_staff')
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


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user__email_verified', 'user__created')
    search_fields = ('user__username',)


@admin.register(models.MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'user__email_verified', 'verified', 'image')
    list_filter = ('verified',)
    search_fields = ('user__username', 'specialization')


@admin.register(models.ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
