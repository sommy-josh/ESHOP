from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserRegistrationSerializer



@api_view(['POST'])
def register_user(request):
    serializer=UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        data=serializer.save()
        return Response({
            'message': 'User Registered successfully',
            'refresh': data['refresh'],
            'access': data['access'],
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)