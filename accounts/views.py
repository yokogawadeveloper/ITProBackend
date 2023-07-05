from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from approval.models import ApproverMatrix
from master.models import OrgDepartmentHead
from .models import *
from .serializers import *

User = get_user_model()
# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

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
            if ApproverMatrix.objects.filter(primary_approver=user.email).exists():
                return Response({
                    'message': 'Approver login',
                    'access': serializer.validated_data['access'],
                    'refresh': serializer.validated_data['refresh'],
                    'username': user.username,
                    'name': user.name,
                    'is_approver': True,
                    
                })
            else:
                if OrgDepartmentHead.objects.filter(Head=user.username).exists():
                    return Response({
                        'message': 'Department Head login',
                        'access': serializer.validated_data['access'],
                        'refresh': serializer.validated_data['refresh'],
                        'username': user.username,
                        'name': user.name,
                        'is_approver': True,
                        
                    })
            return Response({
                'message': 'Normal User login',
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
                'username': user.username,
                'name': user.name,
                'is_approver': False,
                
            })
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
           


class EmployeeUserAPIView(generics.RetrieveAPIView):
    serializer_class = EmployeeUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


