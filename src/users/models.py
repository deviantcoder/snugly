import logging

from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from utils.image_compression import compress


DEFAULT_IMAGE_PATH = 'img/def.png'

logger = logging.getLogger(__name__)

def send_log(message, level='info'):
    LEVEL_MAP = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }

    try:
        log_level = LEVEL_MAP[level.lower().strip()]
    except KeyError:
        raise ValueError(f'Invalid log level: {level}')
    
    current_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f'{current_time}: {message}'

    logger.log(log_level, message)


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


class BaseProfile(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    image = models.ImageField(default=DEFAULT_IMAGE_PATH, upload_to=upload_to, blank=True)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        send_log(f'Saving profile for {self.user.username}.', level='debug')

        is_new = self._state.adding

        if not is_new and self.image:
            try:
                old_instance = type(self).objects.get(id=self.id)
                if old_instance.image == self.image:
                    super().save(*args, **kwargs)
                    return
            except type(self).DoesNotExist:
                send_log(f'Instance with if {self.id} not found during update.', level='warning')

        if self.image and self.image != DEFAULT_IMAGE_PATH:
            try:
                send_log(f'Compressing image for {self.user.username}.', level='debug')
                self.image = compress(self.image)
                send_log(f'Image successfully compressed for {self.user.username}.', level='debug')
            except Exception as error:
                send_log(f'Image compression failed for {self.user.username}: {error}.', level='error')
                raise

        super().save(*args, **kwargs)


class UserProfile(BaseProfile):
    bio = models.TextField(null=True, blank=True)


class MentorProfile(BaseProfile):
    bio = models.TextField(null=True, blank=True)

    specialization = models.CharField(max_length=100, null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    availability = models.CharField(max_length=50, null=True, blank=True)

    verified = models.BooleanField(default=False)


class ManagerProfile(BaseProfile):
    bio = models.TextField(null=True, blank=True)
