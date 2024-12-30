from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# Serializer for user data (id, username, email, bio, and profile_pic).
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_pic']

    # Custom update method to update user information.
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.save()
        return instance
    

# Serializer for registering a new user, used to validate input data and create a new user.
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    # Create a new user instance using the validated data (password is hashed).
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'], 
            email=validated_data['email'], 
            password=validated_data['password']
            )
        return user
    
# Serializer for user login, validating the username and password.
class UserLoginSerializer(serializers.Serializer):
    # Fields: username, password (write-only), and token (read-only)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    # Custom validation checks if credentials are valid, user is active, 
    # and generates a token for successful login.
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
            if not user.is_active:
                raise serializers.ValidationError("User is inactive")
            token, created = Token.objects.get_or_create(user=user)
            data['token'] = token.key
            data['user'] = user
            return data
        else:
            raise serializers.ValidationError("Username and password are required")

