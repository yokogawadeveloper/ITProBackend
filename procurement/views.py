from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import MasterProcurement
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.views import APIView
from django.db.models import Q
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
    


class GetProcurementModificationAPIView(APIView):
    serializer_class = MasterProcurementSerializer

    def get(self, request, format=None):
        user = request.user
        procurement = MasterProcurement.objects.filter(Q(Created_by=user) & Q(Status='Modification'))
        serializer = MasterProcurementSerializer(procurement, many=True)
        return Response(serializer.data)










    
