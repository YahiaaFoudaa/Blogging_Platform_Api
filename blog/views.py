from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer, CategorySerializer, TagSerializer
from .models import Blog
from rest_framework.permissions import IsAdminUser
from django.db.models import Q
from rest_framework.generics import GenericAPIView


# Create your views here.

#BlogCreationView to handle the creation of a new Blog through an API request
class BlogCreateView(APIView):

    #Handle POST requests for creating a new blog
    def post(self, request, *args, **kwargs):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

# BlogDetailView to handle the retrieval of a specific Blog via an API request
class BlogDetailView(APIView):

    # Handle GET requests to retrieve details of a specific blog by its ID
    def get(self, request, *args, **kwargs):
        blog = Blog.objects.get(id=kwargs['id'])
        serializer = BlogSerializer(blog)
        return Response(serializer.data, status=200)
    
# BlogUpdateView to handle the updating of an existing Blog via an API request
class BlogUpdateView(APIView):

    # Handle PUT requests to update a specific blog's data by its ID
    def put(self, request, *args, **kwargs):
        blog = Blog.objects.get(id=kwargs['id'])
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
# BlogDeleteView to handle the deletion of a specific Blog via an API request
class BlogDeleteView(APIView):

    # Handle DELETE requests to delete a specific blog by its ID
    def delete(self, request, *args, **kwargs):
        blog = Blog.objects.get(id=kwargs['id'])
        blog.delete()
        return Response(status=204)
    
#TagCreateView to handle the creation of a new Tag via an API request
class TagCreateView(APIView):

    # Handle POST requests to create a new tag
    def post(self, request, *args, **kwargs):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
#CategoryCreateView to handle the creation of a new Category via an API request
class CategoryCreateView(APIView):
    permission_classes = [IsAdminUser]

    # Handle POST requests to create a new category by admin user
    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class SearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', '')
        blogs = Blog.objects.filter(Q(Title__icontains=query) | Q(Content__icontains=query)
                                    | Q(tag__name__icontains=query) | Q(Author__username__icontains=query))
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=200)
    
class BlogFilterView(APIView):
    def get(self, request, *args, **kwargs):
        category = request.query_params.get('category', '')
        author = request.query_params.get('author', '')
        blogs = Blog.objects.filter(Category__name=category, Author__username=author)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=200)