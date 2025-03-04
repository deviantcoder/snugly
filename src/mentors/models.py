from uuid import uuid4

from django.db import models
from profiles.models import MentorProfile


class MentorSkill(models.Model):
    """
    Model representing a skill associated with a mentor profile.
    """
    
    profile = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=50)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name