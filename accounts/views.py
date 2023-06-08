from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from .serializers import *

User = get_user_model()
# Create your views here.


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response({'detail': 'No active account found with the given credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if serializer.is_valid():
            return Response({
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
                'username': user.username,
                'email': user.email,
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeUserAPIView(generics.RetrieveAPIView):
    serializer_class = EmployeeUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


