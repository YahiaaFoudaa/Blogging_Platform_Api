from rest_framework import serializers
from .models import Blog, Category, Tag

class TagSerializer(serializers.ListField):
    class Meta:
        model = Tag
        fields = ['name']
    
    def create(self, validated_data):
        tag = Tag.objects.create(**validated_data)
        return tag
    
    def to_representation(self, data):
        return data.values_list('name', flat=True)
 
# BlogSerializer class to handle serialization and deserialization of Blog model
class BlogSerializer(serializers.ModelSerializer):
    tags = TagSerializer(required=False)

    class Meta:
        model = Blog
        fields = ['Title', 'Content', 'Author', 'tags', 'Category']

    # Custom create method to handle creation of a new Blog instance
    def create(self, validated_data):
        tag_names = validated_data.pop('tags', [])
        blog = Blog.objects.create(**validated_data)
        if tag_names:
            tags = []
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                tags.append(tag)
            blog.tags.set(tags)
        return blog
        
class CategorySerializer(serializers.ModelSerializer):
    # To include related blogs, use the reverse relationship (many-to-one from Blog to Category)
    blogs = BlogSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['name', 'blogs']
    
    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category