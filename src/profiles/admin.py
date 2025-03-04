from django.contrib import admin

from . import models


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'image', 'created')
    search_fields = ('user__username',)


@admin.register(models.ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'image', 'created')
    search_fields = ('user__username',)


@admin.register(models.MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'verified', 'image', 'user__created')
    list_filter = ('verified',)
    search_fields = ('user__username', 'specialization')
