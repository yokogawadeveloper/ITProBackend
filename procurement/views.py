from rest_framework import viewsets, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import *

User = get_user_model()


# Create your views here.
class MasterProcurementViewSet(viewsets.ModelViewSet):
    queryset = MasterProcurement.objects.all()
    serializer_class = MasterProcurementSerializer
    permission_classes = [permissions.IsAuthenticated]


class MoreAttachmentsViewSet(viewsets.ModelViewSet):
    queryset = MoreAttachments.objects.all()
    serializer_class = MoreAttachmentsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = MoreAttachments.objects.all()
        procurement_id = self.request.query_params.get('procurement_id', None)
        if procurement_id is not None:
            queryset = queryset.filter(procurement=procurement_id)
        return queryset
    
    def create(self, request, *args, **kwargs):
        procurement_id = request.data.get('procurement_id')
        attachment = request.FILES.getlist('attachment')
        try:
            procurement = MasterProcurement.objects.get(id=procurement_id)
            for i in attachment:
                MoreAttachments.objects.create(procurement=procurement,attachment=i)
            return Response({'status': 'success'})
        except MasterProcurement.DoesNotExist:
            return Response({'status': 'failed', 'message': 'Procurement not found'}, status=status.HTTP_404_NOT_FOUND)
        




        
    

