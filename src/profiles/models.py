import os
import logging
import shortuuid

from uuid import uuid4

from django.db import models

from accounts.models import AppUser

from utils.logging import send_log
from utils.image_compression import compress


DEFAULT_IMAGE_PATH = 'img/def.png'

logger = logging.getLogger(__name__)


def upload_to(instance, filename):
    ext = os.path.splitext(filename)[-1].lower()
    new_filename = shortuuid.uuid()
    filename = f'{new_filename}{ext}'

    return f'profiles/{instance.user.username}/{filename}'


class BaseProfile(models.Model):
    """
    BaseProfile is an abstract base class for user profile models.
    Attributes:
        user (OneToOneField): A one-to-one relationship with the AppUser model.
        image (ImageField): An image field for the user's profile picture.
        bio (TextField): A text field for the user's biography.
    Methods:
        __str__(): Returns the username of the associated user.
        save(*args, **kwargs): Custom save method that handles image compression and logging.
        username: Returns the username of the associated user.
        full_name: Returns the full name of the associated user.
    """
    
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to=upload_to, default=DEFAULT_IMAGE_PATH, blank=True)

    bio = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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

    @property
    def username(self):
        return self.user.username

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'


class UserProfile(BaseProfile):
    """
    UserProfile model extends the BaseProfile and represents additional information
    about the user.
    """

    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='user_profile')
    display_name = models.CharField(max_length=50, null=True, blank=True)


class MentorProfile(BaseProfile):
    """
    MentorProfile model extends the BaseProfile model to include additional fields specific to mentors.
    Properties:
        all_skills (QuerySet): Returns a queryset of all skills associated with the mentor.
    """

    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='mentor_profile')

    experience = models.TextField(null=True, blank=True)
    availability = models.CharField(max_length=150, null=True, blank=True)

    verified = models.BooleanField(default=False)

    @property
    def all_skills(self):
        return self.skills.all()
    
    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'


class ManagerProfile(BaseProfile):
    """
    ManagerProfile model that extends the BaseProfile.
    """

    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='manager_profile')
