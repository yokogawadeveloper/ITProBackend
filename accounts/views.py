from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from approval.models import ApprovalTransaction,ApproverMatrix
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
            if user is  not None:
                
                approver = ApprovalTransaction.objects.filter(approvalUserName = user.username).order_by('-id').first()
                if approver is not None:
                    return Response({
                        'access': serializer.validated_data['access'],
                        'refresh': serializer.validated_data['refresh'],
                        'username': user.username,
                        'email': user.email,
                        'name': user.name,
                        'is_approver': True,
                    })
                else:
                    return Response({
                        'access': serializer.validated_data['access'],
                        'refresh': serializer.validated_data['refresh'],
                        'username': user.username,
                        'email': user.email,
                        'name': user.name,
                        'is_approver': False,
                    })
            else:
                return Response({
                    'access': serializer.validated_data['access'],
                    'refresh': serializer.validated_data['refresh'],
                    'username': user.username,
                    'email': user.email,
                    'name': user.name,
                    'is_approver': False,
                }, status=status.HTTP_200_OK)

        else:
            return Response({
                'message': 'Invalid username or password',
                'data': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)


class EmployeeUserAPIView(generics.RetrieveAPIView):
    serializer_class = EmployeeUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


