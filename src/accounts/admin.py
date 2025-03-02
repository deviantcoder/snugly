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


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'image', 'created')
    search_fields = ('user__username',)


@admin.register(models.ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'image', 'created')
    search_fields = ('user__username',)


admin.site.register(models.MentorSkill)


class MentorSkillInline(admin.StackedInline):
    model = models.MentorSkill
    extra = 1


@admin.register(models.MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'verified', 'image', 'user__created')
    list_filter = ('verified',)
    search_fields = ('user__username', 'specialization')

    inlines = [MentorSkillInline]
