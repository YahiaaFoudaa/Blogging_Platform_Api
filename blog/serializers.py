from rest_framework import serializers
from .models import Blog, Tag, Category

# BlogSerializer class to handle serialization and deserialization of Blog model
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'blog']
    
    def create(self, validated_data):
        tag = Tag.objects.create(**validated_data)
        return tag
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
    
    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category
    
class BlogSerializer(serializers.ModelSerializer):
    Tags = TagSerializer(many=True, required=False)
    Categories = CategorySerializer(many=False, required=False)
    class Meta:
        model = Blog
        fields = ['Title', 'Content', 'Author', 'Tags', 'Categories']

    # Custom create method to handle creation of a new Blog instance
    def create(self, validated_data):
        blog = Blog.objects.create(**validated_data)
        return blog