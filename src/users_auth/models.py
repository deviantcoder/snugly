import logging

from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.image_compression import compress
from utils.logging import send_log


DEFAULT_IMAGE_PATH = 'img/def.png'

logger = logging.getLogger(__name__)


class AppUser(AbstractUser):
    """
    A custom user model that extends the AbstractUser model.

    Attributes:
        role (str): The role of the user, chosen from predefined roles (USER, MENTOR, MANAGER, ADMIN).
        created (datetime): The date and time when the user was created.
        updated (datetime): The date and time when the user was last updated.
        id (UUID): The unique identifier for the user.

    Methods:
        __str__(): Returns the username of the user.
        save(*args, **kwargs): Overrides the save method to set is_staff and is_superuser based on the user's role.
    """

    class Roles(models.TextChoices):
        USER = ('user', 'Regular')
        MENTOR = ('mentor', 'Mentor')
        MANAGER = ('manager', 'Manager')
        ADMIN = ('admin', 'Admin')

    role = models.CharField(max_length=50, choices=Roles.choices, default=Roles.USER)

    email_verified = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['role'], name='appuser_role_idx'),
            models.Index(fields=['created'], name='appuser_created_idx'),
        ]

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
        if self.role == self.Roles.USER:
            try:
                return self.user_profile
            except UserProfile.DoesNotExist:
                return None
        elif self.role == self.Roles.MENTOR:
            try:
                return self.mentor_profile
            except MentorProfile.DoesNotExist:
                return None
        elif self.role == self.Roles.MANAGER:
            try:
                return self.manager_profile
            except ManagerProfile.DoesNotExist:
                return None
        return None


class AppUserManager(models.Manager):
    """
    Custom manager for AppUser model to filter users by their roles.
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
    A proxy model for the AppUser model that provides additional functionality.
    This proxy model uses a custom manager `AppUserManager` and adds a method
    to check if the user has a specific role.
    """
    
    objects = AppUserManager()

    def has_role(self, role):
        return self.role == role
    
    class Meta:
        proxy = True


def upload_to(instance, filename):
    return f'profiles/{instance.user.username}/{filename}'


class BaseProfile(models.Model):
    """
    BaseProfile is an abstract base class for user profile models.
    Attributes:
        user (OneToOneField): A one-to-one relationship with the AppUser model.
        image (ImageField): An optional image field for the user's profile picture.
        id (UUID): A unique identifier for the profile, generated by default.
    Methods:
        save(*args, **kwargs): Overrides the default save method to handle image compression and logging.
    """

    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default=DEFAULT_IMAGE_PATH, upload_to=upload_to, blank=True)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        is_new = self._state.adding

        if not is_new and self.image:
            try:
                old_instance = type(self).objects.get(id=self.id)
                if old_instance.image == self.image:
                    super().save(*args, **kwargs)
                    return
            except type(self).DoesNotExist:
                send_log(logger, f'Instance with id {self.id} not found during update.', level='warning')

        if self.image and self.image != DEFAULT_IMAGE_PATH:
            try:
                self.image = compress(self.image)
            except Exception as error:
                send_log(logger, f'Image compression failed for {self.user.username}: {error}.', level='error')
                raise

        super().save(*args, **kwargs)


class UserProfile(BaseProfile):
    """
    UserProfile model that extends the BaseProfile.

    """
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='user_profile')
    bio = models.TextField(null=True, blank=True)


class MentorProfile(BaseProfile):
    """
    MentorProfile model that extends the BaseProfile.
    """
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='mentor_profile')
    bio = models.TextField(null=True, blank=True)

    experience = models.TextField(null=True, blank=True)
    availability = models.CharField(max_length=50, null=True, blank=True)

    verified = models.BooleanField(default=False)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    @property
    def username(self):
        return self.user.username
    
    @property
    def all_skills(self):
        return self.skills.all()
    

class MentorSkill(models.Model):
    profile = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name


class ManagerProfile(BaseProfile):
    """
    ManagerProfile model that extends BaseProfile.
    """

    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='manager_profile')
    bio = models.TextField(null=True, blank=True)
