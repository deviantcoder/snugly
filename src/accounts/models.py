import os
import logging
import shortuuid

from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.logging import send_log
from utils.image_compression import compress


DEFAULT_IMAGE_PATH = 'img/def.png'

logger = logging.getLogger(__name__)


class AppUser(AbstractUser):
    """
    AppUser model that extends the AbstractUser model to include additional fields and methods.
    Attributes:
        role (str): The role of the user, chosen from predefined roles (USER, MENTOR, MANAGER, ADMIN).
        email_verified (bool): Indicates whether the user's email has been verified.
    Meta:
        ordering (list): Default ordering of the users by creation date in descending order.
        indexes (list): Database indexes for the role and created fields.
    Methods:
        __str__(): Returns the username of the user.
        save(*args, **kwargs): Custom save method to set is_staff and is_superuser based on the user's role.
        profile: Property that returns the user's profile based on their role.
    """

    class Roles(models.TextChoices):
        USER = ('user', 'Regular')
        MENTOR = ('mentor', 'Mentor')
        MANAGER = ('manager', 'Manager')
        ADMIN = ('admin', 'Admin')

    role = models.CharField(max_length=15, choices=Roles, default=Roles.USER)

    email_verified = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['role'], name='appuser_role_idx'),
            models.Index(fields=['created'], name='appuser_created_idx'),
        ]

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if self.role == self.Roles.MANAGER:
            self.is_staff = True
        elif self.role == self.Roles.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        elif self.is_superuser:
            self.is_staff = True
            self.role = self.Roles.ADMIN
        else:
            self.is_staff = False
            self.is_superuser = False
            
        super().save(*args, **kwargs)

    @property
    def profile(self):
        try:
            if self.role == self.Roles.USER:
                return getattr(self, 'user_profile')
            elif self.role == self.Roles.MENTOR:
                return getattr(self, 'mentor_profile')
            elif self.role == self.Roles.MANAGER:
                return getattr(self, 'manager_profile')
            return None
        except AttributeError:
            return None
    
    
class AppUserManager(models.Manager):
    """
    Custom manager for the AppUser model to filter users by their roles.
    Methods:
        by_role(role): Returns a queryset filtered by the specified role.
        users(): Returns a queryset of users with the role 'USER'.
        mentors(): Returns a queryset of users with the role 'MENTOR'.
        managers(): Returns a queryset of users with the role 'MANAGER'.
        admins(): Returns a queryset of users with the role 'ADMIN'.
    """

    def by_role(self, role):
        return super().get_queryset().filter(role=role)
    
    def users(self):
        return self.by_role(role=AppUser.Roles.USER)
    
    def mentors(self):
        return self.by_role(role=AppUser.Roles.MENTOR)
    
    def managers(self):
        return self.by_role(role=AppUser.Roles.MANAGER)
    
    def admins(self):
        return self.by_role(role=AppUser.Roles.ADMIN)
    

class AppUserProxy(AppUser):
    """
    A proxy model for the AppUser model that provides additional functionality. Uses a custom manager 'AppUserManager'
    Methods:
        has_role(role): Checks if the user has the specified role.
    """
    
    objects = AppUserManager()

    def has_role(self, role):
        return self.role == role
    
    class Meta:
        proxy = True