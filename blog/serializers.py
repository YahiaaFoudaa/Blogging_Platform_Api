from rest_framework import serializers
from .models import Blog, Category, Tag
from django.utils.timezone import now

# Serializer for handling a list of Tag objects.
class TagSerializer(serializers.ListField):
    # Meta class to specify the model and fields to be serialized.
    class Meta:
        model = Tag
        fields = ['name']
    
    # Custom method to create a new Tag object from validated data.
    def create(self, validated_data):
        # Creates a new Tag object with the provided validated data.
        tag = Tag.objects.create(**validated_data)
        return tag
    
    # Custom method to represent the Tag objects in a specific format.
    # Returns a list of tag names (flat list).
    def to_representation(self, data):
        return data.values_list('name', flat=True)
 
# BlogSerializer class to handle serialization and deserialization of Blog model
class BlogSerializer(serializers.ModelSerializer):
    # Serializes tags, allows immediate publishing, and formats published date.
    tags = TagSerializer(required=False)
    published_now = serializers.BooleanField(required=False, write_only=True, default=False)
    Published_Date = serializers.SerializerMethodField()
    
    # Specifies the Blog model and the fields to serialize.
    class Meta:
        model = Blog
        fields = ['Title', 'Content', 'Author', 'tags', 'Category', 'Published_Date', 'published_now']

    def get_Published_Date(self, obj):
        # Returns the formatted published date or None if not available.
        if obj.Published_Date:
            return obj.Published_Date.strftime('%d-%m-%Y %H:%M:%S')
        else:
            return None

    # Custom create method to handle creation of a new Blog instance
    def create(self, validated_data):
        # Extracts the 'tags' and 'published_now' data from the validated data.
        tag_names = validated_data.pop('tags', [])
        published_now = validated_data.pop('published_now', False)
        # If 'published_now' is True, set the 'Published_Date' to the current time, otherwise set it to None.
        if published_now:
            validated_data['Published_Date'] = now()
        else:
            validated_data['Published_Date'] = None

        # Creates a new Blog object using the remaining validated data.
        blog = Blog.objects.create(**validated_data)

        # If there are tags provided, create or get the Tag objects and associate them with the blog.
        if tag_names:
            tags = []
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                tags.append(tag)
            blog.tags.set(tags) # Sets the tags for the blog.
        
        # Returns the created blog instance.
        return blog
    
    def update(self, instance, validated_data):
        # Extracts the 'tags' and 'published_now' data from the validated data.
        tag_names = validated_data.pop('tags', [])
        published_now = validated_data.pop('published_now', False)
        # If 'published_now' is True, set the 'Published_Date' to the current time, otherwise set it to None.
        if published_now:
            validated_data['Published_Date'] = now()
        else:
            validated_data['Published_Date'] = None
        
        # Calls the parent class's update method to update the blog instance with the validated data.
        blog = super().update(instance, validated_data)
        # If there are tags provided, create or get the Tag objects and associate them with the blog.
        if tag_names:
            tags = []
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                tags.append(tag)
            blog.tags.set(tags) # Sets the tags for the blog.
        # Returns the updated blog instance.
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