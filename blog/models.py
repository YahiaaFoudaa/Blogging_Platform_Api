from django.db import models
from accounts.models import User

class Blog(models.Model):
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=255)
    Content = models.TextField()
    Created_Date = models.DateTimeField(auto_now_add=True)
    Published_Date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

# Create your models here.
