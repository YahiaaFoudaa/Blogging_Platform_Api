from django.db import models
from accounts.models import User

# Model to represent a Tag with a unique name.
class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True, default="")

# Model to represent a Category with a name.
class Category(models.Model):
    name = models.CharField(max_length=30)


# Model to represent a Blog post.
class Blog(models.Model):
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=255)
    Content = models.TextField()
    Created_Date = models.DateTimeField(auto_now_add=True)
    Published_Date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    Category = models.ForeignKey('Category', on_delete=models.RESTRICT)
    tags = models.ManyToManyField('Tag', related_name='blogs', blank=True)
