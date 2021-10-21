"""
models.py contain information regarding the models that users app is using
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    """
    User class extends and implements the Django AbstractUser class that has all
    the functionality e.g. User Authentication already implemented
    """

    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        """
        funtion returns the username of particular instance of User object

        Return:
            it returns the username of particular instance of User object
        """
        return f"{self.username} Profile"
