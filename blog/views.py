from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer, CategorySerializer, TagSerializer
from .models import Blog
from rest_framework.permissions import IsAdminUser, BasePermission
from django.db.models import Q
from .pagination import BlogPagination
from rest_framework.filters import OrderingFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound

# Custom permission class to check if the user is the owner (author) of the object.
class IsOwner(BasePermission):
    # Method to check object-level permission, ensuring that the requesting user is the author of the object.
    def has_object_permission(self, request, view, obj):
        # Returns True if the object’s author matches the requesting user, otherwise False.
        return obj.Author == request.user


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
    # Only the owner (author) of the blog can update it.
    permission_classes = [IsOwner]
    
    # Helper method to retrieve the blog object by its ID, and check permissions.
    def get_object(self, id):
        try:
            # Tries to fetch the blog by ID.
            obj = Blog.objects.get(id=id)
            # Checks if the current user has permission to edit the blog.
            self.check_object_permissions(self.request, obj)
            return obj
        except Blog.DoesNotExist:
            # If the blog is not found, raises a 'NotFound' exception.
            raise NotFound("Blog not found")
        
    # Method to handle PUT request for updating a blog.
    def put(self, request, *args, **kwargs):
        # Retrieves the blog object using the ID passed in the URL.
        blog = self.get_object(kwargs['id'])
        # Serializes the blog data, allowing partial updates (not all fields required).
        serializer = BlogSerializer(blog, partial=True, data=request.data)
        # If the serializer data is valid, save the updated blog and return the updated data.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        # If the serializer is not valid, return the errors with a 400 Bad Request status.
        return Response(serializer.errors, status=400)


# BlogDeleteView to handle the deletion of a specific Blog via an API request
class BlogDeleteView(APIView):
    # Permission to delete: owner or admin
    permission_classes = [IsOwner | IsAdminUser]
    # Token-based authentication
    authentication_classes = [TokenAuthentication]

    def get_object(self, id):
        try:
            # Retrieve blog by id and check permissions
            obj = Blog.objects.get(id=id)
            self.check_object_permissions(self.request, obj)
            return obj
        except Blog.DoesNotExist:
            # Return error if blog not found
            raise NotFound("Blog not found")

    def delete(self, request, *args, **kwargs):
        # Get blog object by id and delete
        blog = self.get_object(kwargs['id'])
        blog.delete()
        # Return successful response with no content
        return Response(status=204)
    
    
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
        # Get search query parameter (default is empty string)
        query = request.query_params.get('q', '')
        # Filter blogs based on query in title, content, tags, or author's username
        blogs = Blog.objects.filter(Q(Title__icontains=query) | Q(Content__icontains=query)
                                    | Q(tags__name__icontains=query) | Q(Author__username__icontains=query))
        # Serialize the filtered blogs and return them in the response
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=200) # Return serialized data with a 200 OK status
    
class BlogFilterView(APIView):
    # Handle GET request to filter blogs by category or author
    def get(self, request, *args, **kwargs):
        # Retrieve query parameters for category and author (default empty string)
        category = request.query_params.get('Category', '')
        author = request.query_params.get('Author', '')
        # Filter blogs by matching category or author
        blogs = Blog.objects.filter(Q(Category__name=category) | Q(Author__username=author))
        # Serialize the filtered blogs
        serializer = BlogSerializer(blogs, many=True)
        # Return the serialized blog data with a 200 OK status
        return Response(serializer.data, status=200)
    
class BlogListView(APIView):
    # Set pagination class and filter backends for ordering
    pagination_class = BlogPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['Published_Date', 'Category']

    # Handle GET request to retrieve and paginate blogs
    def get(self, request, *args, **kwargs):
        # Filter blogs with a non-null Published_Date
        blogs = Blog.objects.filter(Published_Date__isnull=False).all()
        # Initialize the paginator
        paginator = self.pagination_class()
        # Get sorting parameter from query and apply ordering if present
        sort_by = request.query_params.get('sort', '')
        if sort_by:
            blogs = blogs.order_by(sort_by)
        # Paginate the queryset if necessary
        page = paginator.paginate_queryset(blogs, request, view=self)
        # If pagination applied, return paginated response
        if page is not None:
            serializer = BlogSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        # Return all blogs without pagination if no pagination is needed
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=200)