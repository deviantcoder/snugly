from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser


class AppUser(AbstractUser):
    class Roles(models.TextChoices):
        USER = ('user', 'Regular')
        MENTOR = ('mentor', 'Mentor')
        MANAGER = ('manager', 'Manager')
        ADMIN = ('admin', 'Admin')

    role = models.CharField(max_length=50, choices=Roles.choices, default=Roles.USER)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if self.role == self.Roles.MANAGER:
            self.is_staff = True
        elif self.role == self.Roles.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False

        return super().save(*args, **kwargs)


class AppUserManager(models.Manager):
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
    objects = AppUserManager()

    def has_role(self, role):
        return self.role == role
    
    class Meta:
        proxy = True


def upload_to(instance, filename):
    return f'profiles/{instance.user.username}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='user_profile')
    image = models.ImageField(default='img/def.png', upload_to=upload_to, blank=True)

    bio = models.TextField(null=True, blank=True)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.user.username


class MentorProfile(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='mentor_profile')
    image = models.ImageField(default='img/def.png', upload_to=upload_to, blank=True)

    bio = models.TextField(null=True, blank=True)

    specialization = models.CharField(max_length=100, null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    availability = models.CharField(max_length=50, null=True, blank=True)

    verified = models.BooleanField(default=False)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.user.username


class ManagerProfile(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='manager_profile')
    image = models.ImageField(default='img/def.png', upload_to=upload_to, blank=True)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.user.username
