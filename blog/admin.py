from django.contrib import admin
from .models import Tag, Blog, Category

# Registers the Tag, Blog, and Category models with the admin site for management.
admin.site.register(Tag)
admin.site.register(Blog)
admin.site.register(Category)

