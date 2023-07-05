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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response({'detail': 'No active account found with the given credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if serializer.is_valid():
            if user is  not None:
                if ApproverMatrix.objects.filter(primary_approver=user.email).exists():
                    if MasterRoleMapping.objects.filter(employeeId=user.username).exists():
                        user_type = MasterRoleMapping.objects.filter(employeeId=user.username).values('roleId')
                        if user_type is not None:
                            role_name = MasterRole.objects.filter(roleId=user_type).values('rolename')
                            if role_name == 'Admin':
                                return Response({
                                    'access': serializer.validated_data['access'],
                                    'refresh': serializer.validated_data['refresh'],
                                    'is_admin':True,
                                    'is_dsin':False,
                                    'is_requester':False,
                                    'is_approver':True,
                                    'user_id': user.username,
                                    'user_name': user.name,
                                    'user_email': user.email,
                                })
                            elif role_name == 'DSIN':
                                return Response({
                                    'access': serializer.validated_data['access'],
                                    'refresh': serializer.validated_data['refresh'],
                                    'is_admin':False,
                                    'is_dsin':True,
                                    'is_requester':False,
                                    'is_approver':True,
                                })
                            else:
                                return Response({
                                    'access': serializer.validated_data['access'],
                                    'refresh': serializer.validated_data['refresh'],
                                    'is_admin':False,
                                    'is_dsin':False,
                                    'is_requester':False,
                                    'is_approver':True,
                                    # 'user_id': user.username,
                                    # 'user_name': user.name,
                                    # 'user_email': user.email,
                                })
                else:
                    if OrgDepartmentHead.objects.filter(Head=user.username).exists():
                        if MasterRoleMapping.objects.filter(employeeId=user.username).exists():
                            user_type = MasterRoleMapping.objects.filter(employeeId=user.username).values('roleId')
                            if user_type is not None:
                                role_name = MasterRole.objects.filter(roleId=user_type).values('rolename')
                                if role_name == 'Admin':
                                    return Response({
                                        'access': serializer.validated_data['access'],
                                        'refresh': serializer.validated_data['refresh'],
                                        'is_admin':True,
                                        'is_dsin':False,
                                        'is_requester':False,
                                        'is_approver':True,
                                        # 'user_id': user.username,
                                        # 'user_name': user.name,
                                        # 'user_email': user.email,
                                    })
                                elif role_name == 'DSIN':
                                    return Response({
                                        'access': serializer.validated_data['access'],
                                        'refresh': serializer.validated_data['refresh'],
                                        'is_admin':False,
                                        'is_dsin':True,
                                        'is_requester':False,
                                        'is_approver':True,
                                        # 'user_id': user.username,
                                        # 'user_name': user.name,
                                        # 'user_email': user.email,
                                    })
                                else:
                                    return Response({
                                        'access': serializer.validated_data['access'],
                                        'refresh': serializer.validated_data['refresh'],
                                        'is_admin':False,
                                        'is_dsin':False,
                                        'is_requester':False,
                                        'is_approver':True,
                                        # 'user_id': user.username,
                                        # 'user_name': user.name,
                                        # 'user_email': user.email,
                                    })
                    else:
                        if MasterRoleMapping.objects.filter(employeeId=user.username).exists():
                            user_type = MasterRoleMapping.objects.filter(employeeId=user.username).values('roleId')
                            if user_type is not None:
                                role_name = MasterRole.objects.filter(roleId=user_type).values('rolename')
                                if role_name == 'Admin':
                                    return Response({
                                        'access': serializer.validated_data['access'],
                                        'refresh': serializer.validated_data['refresh'],
                                        'is_admin':True,
                                        'is_dsin':False,
                                        'is_requester':True,
                                        'is_approver':False,
                                        # 'user_id': user.username,
                                        # 'user_name': user.name,
                                        # 'user_email': user.email,
                                    })
                                elif role_name == 'DSIN':
                                    return Response({
                                        'access': serializer.validated_data['access'],
                                        'refresh': serializer.validated_data['refresh'],
                                        'is_admin':False,
                                        'is_dsin':True,
                                        'is_requester':True,
                                        'is_approver':False,
                                        # 'user_id': user.username,
                                        # 'user_name': user.name,
                                        # 'user_email': user.email,
                                    })
                                else:
                                    return Response({
                                        'access': serializer.validated_data['access'],
                                        'refresh': serializer.validated_data['refresh'],
                                        'is_admin':False,
                                        'is_dsin':False,
                                        'is_requester':True,
                                        'is_approver':False,
                                        # 'user_id': user.username,
                                        # 'user_name': user.name,
                                        # 'user_email': user.email,
                                    })
            else:
                return Response({
                'message': 'Invalid username or password',
                'data': serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
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


