from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework.exceptions import ValidationError


User=get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2= serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model=User
        fields=('username', 'email', 'password', 'password2')
        

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError("passwords must match.")
        
        if User.objects.filter(username=data['username']).exists():
            raise ValidationError({'username': "A user with that username exists"})

        if User.objects.filter(email=data['email']).exists():
            raise ValidationError({"email": " Email already exists"})
        

        return data
        
    def create(self, validated_data):
        user=User(
            username=validated_data['username'],
            email=validated_data['email'],  
        )
        user.set_password(validated_data['password'])
        user.save()

        send_mail(
            'New User Registration',
            f'New User registered: {user.username}, email: {user.email}',
            'chisomzzy1@gmail.com',
            ['chisomzzy1@gmail.com'],
        )

        send_mail(
            'Welcome to our E-commerce platform',
            'Thank you for registering with us!',
            'chisomzzy1@gmail.com',
            [user.email],
        )

        refresh=RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access':str(refresh.access_token),
            'user':user
        }
