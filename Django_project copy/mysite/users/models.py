from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # You can add custom fields if needed, like:
    bio = models.TextField(null=True, blank=True)
    # Other custom fields here


