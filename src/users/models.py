from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser


class AppUser(AbstractUser):
    class Role(models.TextChoices):
        USER = ('user', 'Regular')
        MENTOR = ('mentor', 'Mentor')
        MANAGER = ('manager', 'Manager')
        ADMIN = ('admin', 'Admin')

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.USER)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.username

    @property
    def is_mentor(self):
        return self.role == self.Role.MENTOR
    
    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER
    
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if self.role == self.Role.MANAGER:
            self.is_staff = True
        elif self.role == self.Role.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        return super().save(*args, **kwargs)


class UserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=AppUser.Role.USER)
    

class MentorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=AppUser.Role.MENTOR)
    

class ManagerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=AppUser.Role.MANAGER)


class UserProxy(AppUser):
    objects = UserManager()

    class Meta:
        proxy = True


class MentorProxy(AppUser):
    objects = MentorManager()

    class Meta:
        proxy = True


class ManagerProxy(AppUser):
    objects = ManagerManager()

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
