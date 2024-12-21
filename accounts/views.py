from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.exceptions import NotFound
from django.contrib.auth import logout


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
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        users = User.objects.exclude(is_staff=True)
        serializer = UserRegisterSerializer(users, many=True)
        return Response(serializer.data)
    
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found")

    def put(self, request, *args, **kwargs):
        # Get the current user (or you could retrieve by user_id)
        user = request.user  # Assuming user is logged in

        # Pass the user object into the serializer for updating
        serializer = UserSerializer(user, data=request.data, partial=True)  # partial=True allows partial updates

        if serializer.is_valid():
            serializer.save()  # Save the updated data
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
