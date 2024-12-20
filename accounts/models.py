from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# Define a custom user model by extending the built-in AbstractUser class
class User(AbstractUser):
    # Bio field for user description (optional, max 500 characters)
    bio = models.TextField(max_length=500, default="",null=True, blank=True, 
                           help_text="A short bio about the user.")
    # Profile picture field for uploading images (optional)
    profile_pic = models.ImageField(upload_to="profile_pics", default="",null=True, blank=True, 
                                    help_text="Upload a profile picture.")