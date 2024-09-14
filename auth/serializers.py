# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .task import send_admin_registration_email, send_welcome_email

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError("Passwords must match.")
        
        if User.objects.filter(username=data['username']).exists():
            raise ValidationError({'username': "A user with that username already exists."})

        if User.objects.filter(email=data['email']).exists():
            raise ValidationError({"email": "Email already exists."})

        return data

    def create(self, validated_data):
        # Create the user object
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        # Send emails asynchronously using Celery tasks
        send_admin_registration_email.delay(user.username, user.email)
        send_welcome_email.delay(user.email)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user
        }
