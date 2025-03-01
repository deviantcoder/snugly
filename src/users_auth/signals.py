import os
import shutil
import logging

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .models import UserProfile, MentorProfile, ManagerProfile

from utils.logging import send_log

User = get_user_model()
Roles = User.Roles

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a user profile when a new user is created.

    Raises:
        IntegrityError: If there is an issue creating the profile.

    The function creates a corresponding profile based on the user's role:
        - UserProfile for users with the role `Roles.USER`
        - MentorProfile for users with the role `Roles.MENTOR`
        - ManagerProfile for users with the role `Roles.MANAGER`
    """

    if created:
        try:
            if instance.role == Roles.USER:
                UserProfile.objects.create(
                    user=instance
                )
            elif instance.role == Roles.MENTOR:
                MentorProfile.objects.create(
                    user=instance
                )
            elif instance.role == Roles.MANAGER:
                ManagerProfile.objects.create(
                    user=instance
                )
        except IntegrityError as error:
            send_log(logger, f'Failed to create profile for {instance.username}: {error}', level='error')


@receiver(post_delete, sender=UserProfile)
@receiver(post_delete, sender=MentorProfile)
@receiver(post_delete, sender=ManagerProfile)
def delete_profile_media(sender, instance, **kwargs):
    """
    Deletes the media files associated with a user's profile after profile deletion.
    """

    try:
        path = f'media/profiles/{instance.user.username}'
        if os.path.exists(path):
            shutil.rmtree(path)
    except Exception as error:
        send_log(logger, f'Error occured while deleting profile media: {error}', level='error')
