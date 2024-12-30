from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.exceptions import NotFound
from django.contrib.auth import logout
from rest_framework.authentication import TokenAuthentication


# Create your views here.

# API view for user registration.
class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    
    # Handle POST requests for registering a new user.
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view for handling user login.
class UserLoginView(APIView):  
    permission_classes = [AllowAny]
    
    # Handle POST request for user login.
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(APIView):
    # Only accessible by admin users.
    permission_classes = [IsAdminUser]

    # Handles GET requests to list non-admin users.
    def get(self, request):
        # Excludes admin users and serializes the remaining users.
        users = User.objects.exclude(is_staff=True)
        serializer = UserRegisterSerializer(users, many=True)
        # Returns serialized user data.
        return Response(serializer.data)
    
# View to handle user update requests (PUT requests) for authenticated users.
class UserUpdateView(APIView):
    # Only authenticated users can access this view.
    permission_classes = [IsAuthenticated]
    # Token authentication is required for accessing the view.
    authentication_classes = [TokenAuthentication]
    
    # Helper method to retrieve a user by ID, raises a NotFound error if the user doesn't exist.
    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found")

    # Handles PUT requests to update user data.
    def put(self, request, *args, **kwargs):
        # Serialize the current user with the new data from the request (partial update allowed).
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        # If the data is valid, save the updated user and return the serialized data.   
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        # If validation fails, return the error messages with a 400 status code
        return Response(serializer.errors, status=400)
    
# View to handle user logout functionality.
class UserLogoutView(APIView):
    # Only authenticated users can access this view.
    permission_classes = [IsAuthenticated]
    # Token authentication is required for accessing the view.
    authentication_classes = [TokenAuthentication]

    # Handles POST requests for logging out a user.
    def post(self, request, *args, **kwargs):
        # Deletes the user's authentication token to log them out.
        request.user.auth_token.delete()
        # Save the user instance after logging out (optional step to refresh user state).
        user = request.user
        user.save()
        # Call Django's logout function to clear the session.
        logout(request)
        # Return a success message indicating successful logout.
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
