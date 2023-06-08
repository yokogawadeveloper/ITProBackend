from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from .models import MasterProcurement
from django.contrib.auth import get_user_model
from rest_framework import permissions

# Create your views here.
class MasterProcurementViewSet(viewsets.ModelViewSet):
    queryset = MasterProcurement.objects.all()
    serializer_class = MasterProcurementSerializer
    permission_classes = [permissions.IsAuthenticated]






    
