from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import MasterProcurement
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import filters
from rest_framework.decorators import action
from .serializers import *
from .models import *


User = get_user_model()
# Create your views here.
class MasterProcurementViewSet(viewsets.ModelViewSet):
    queryset = MasterProcurement.objects.all()
    serializer_class = MasterProcurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = MasterProcurement.objects.filter(Created_by=user)
        serializer = MasterProcurementSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'] , url_path='modifiedprocurementlist', url_name='modifiedprocurementlist')
    def modifiedprocurementlist(self, request, *args, **kwargs):
        user = request.user
        queryset = MasterProcurement.objects.filter(Created_by=user)
        queryset = queryset.filter(Status__icontains='Modification')
        serializer = MasterProcurementSerializer(queryset, many=True)
        return Response(serializer.data)
    

    

