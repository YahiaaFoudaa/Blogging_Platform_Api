from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from .models import Blog


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