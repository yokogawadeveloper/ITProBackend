from django.db.models import Q
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from approval.serializers import *
from .serializers import *

User = get_user_model()


# Create your views here.
class MasterProcurementViewSet(viewsets.ModelViewSet):
    queryset = MasterProcurement.objects.all()
    serializer_class = MasterProcurementSerializer
    permission_classes = [permissions.IsAuthenticated]


    def list(self, request, *args, **kwargs):
        user = request.user
        # queryset = MasterProcurement.objects.filter(Created_by=user, Status='Pending').order_by('-id')
        queryset = MasterProcurement.objects.filter(Created_by=user).order_by('-id')
        serializer = MasterProcurementSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'getmodificationlist')
    def get(self, request, format=None):
        user = request.user
        procurement = MasterProcurement.objects.filter(Q(Created_by=user) & Q(Status='Modification'))
        serializer = MasterProcurementSerializer(procurement, many=True)
        return Response(serializer.data)
        




class MoreAttachmentsViewSet(viewsets.ModelViewSet):
    queryset = MoreAttachments.objects.all()
    serializer_class = MoreAttachmentsSerializer
    permission_classes = [permissions.IsAuthenticated]

    
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
        




        
    

