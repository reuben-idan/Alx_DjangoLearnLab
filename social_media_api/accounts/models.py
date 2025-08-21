from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    # users who follow this user; symmetrical=False allows directional follow
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def __str__(self) -> str:
        return self.username

# Create your models here.
