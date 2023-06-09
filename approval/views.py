from rest_framework import permissions
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import *
from procurement.models import *

# Create your views here. 
class ApprovalTransactionViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return ApprovalTransaction.objects.all()
    

    def get_serializer_class(self):
        return ApprovalTransactionSerializer
    

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        sequence = instance.sequence   # get sequence number
        if sequence == 1:
            instance.status = request.data['status']
            instance.remarks = request.data['remarks']
            instance.create_by = request.user
            instance.update_by = request.user
            instance.save()
            serializer.save()
            return Response(serializer.data)
    
        elif sequence == 2:
            sequence_1_approved = ApprovalTransaction.objects.filter(procurementId=instance.procurementId, sequence=1, status='Approved').exists()
            if sequence_1_approved:
                instance.status = request.data['status']
                instance.remarks = request.data['remarks']
                instance.create_by = request.user
                instance.update_by = request.user
                instance.save()
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'error': 'Sequence 1 approval is required'}, status=status.HTTP_400_BAD_REQUEST)

        elif sequence == 3:
            sequence_2_approved = ApprovalTransaction.objects.filter(procurementId=instance.procurementId, sequence=2, status='Approved').exists()
            if sequence_2_approved:
                instance.status = request.data['status']
                instance.remarks = request.data['remarks']
                instance.create_by = request.user
                instance.update_by = request.user
                instance.save()
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'error': 'Sequence 2 approval is required'}, status=status.HTTP_400_BAD_REQUEST)


        elif sequence == 4:
            sequence_3_approved = ApprovalTransaction.objects.filter(procurementId=instance.procurementId, sequence=3, status='Approved').exists()
            if sequence_3_approved:
                instance.status = request.data['status']
                instance.remarks = request.data['remarks']
                instance.create_by = request.user
                instance.update_by = request.user
                instance.save()
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'error': 'Sequence 3 approval is required'}, status=status.HTTP_400_BAD_REQUEST)
            


        elif sequence == 5:
            sequence_4_approved = ApprovalTransaction.objects.filter(procurementId=instance.procurementId, sequence=4, status='Approved').exists()
            if sequence_4_approved:
                instance.status = request.data['status']
                instance.remarks = request.data['remarks']
                instance.create_by = request.user
                instance.update_by = request.user
                instance.save()
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'error': 'Sequence 4 approval is required'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Invalid sequence'}, status=status.HTTP_400_BAD_REQUEST)
        
        



        
    
        

    

        
    

    

    