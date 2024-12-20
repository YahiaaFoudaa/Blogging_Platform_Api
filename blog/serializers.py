from rest_framework import serializers
from .models import Blog

# BlogSerializer class to handle serialization and deserialization of Blog model
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['Title', 'Content', 'Author']

    # Custom create method to handle creation of a new Blog instance
    def create(self, validated_data):
        blog = Blog.objects.create(**validated_data)
        return blog