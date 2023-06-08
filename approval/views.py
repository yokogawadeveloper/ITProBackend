from rest_framework import permissions
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import *

# Create your views here.
class ApproverMatrixViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ApproverMatrix.objects.all()
    
    def get_serializer_class(self):
        return ApproverMatrixSerializer
    
    def create(self, request, *args, **kwargs):
        primary_approver = request.data['primary_approver']
        secondary_approver = request.data['secondary_approver']
        primary_approver = User.objects.filter(username=primary_approver).values_list('id', flat=True).first()
        secondary_approver = User.objects.filter(username=secondary_approver).values_list('id', flat=True).first()

        request.data._mutable = True # make it mutable
        request.data['primary_approver'] = primary_approver
        request.data['secondary_approver'] = secondary_approver

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['post'])
    def authenticate_approver(self, request, *args , **kwargs):
        user = request.user
        approver = ApproverMatrix.objects.filter(Q(primary_approver=user) | Q(secondary_approver=user)).first()
        if approver:
            return Response({'is_approver': True}, status=status.HTTP_200_OK)
        else:
            return Response({'is_approver': False}, status=status.HTTP_200_OK)
        
        

    

        

        
    
    