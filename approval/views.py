from rest_framework import permissions
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action

from django.contrib.auth import get_user_model
from .serializers import *
from procurement.serializers import *
from procurement.models import *
from .models import *



User = get_user_model()
# Create your views here. 
class ApprovalAuthenticateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        ApprovalUser = ApprovalTransaction.objects.filter(Q(approvalUserName = user) & Q(status='Pending')).order_by('sequence')
        if ApprovalUser.exists():
            serializer = ApprovalTransactionSerializer(ApprovalUser, many=True)
            is_approver = True
            return Response({
                'is_approver': is_approver,
                'username': serializer.data[0]['approvalUserName'],
                'email': serializer.data[0]['approverEmail'],
                })
        else:
            is_approver = False
            return Response({'is_approver': is_approver})


class LoggedInApprovalProcurementPendingList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        ApprovalUser = ApprovalTransaction.objects.filter(Q(approvalUserName = user) & Q(status='Pending')).order_by('sequence')
        ProcurementId = ApprovalUser.values_list('procurementId', flat=True)
        ProcurementDetails = MasterProcurement.objects.filter(id__in=ProcurementId)
        if ApprovalUser.exists():
            serializer = MasterProcurementSerializer(ProcurementDetails, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'No pending approval'})
        

class ApprovalProcurementDetailsByID(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk ,*args, **kwargs):
        procurement = MasterProcurement.objects.get(id=pk)
        serializer = MasterProcurementSerializer(procurement)
        return Response(serializer.data)
    


# Transaction ..
class ApprovalTransactionViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return ApprovalTransaction.objects.all()
    

    def get_serializer_class(self):
        return ApprovalTransactionSerializer
   

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        sequence = instance.sequence
        if sequence == 1:
            # Update the ApprovalTransaction instance
            instance.status = request.data['status']
            instance.remarks = request.data['remarks']
            instance.create_by = request.user
            instance.update_by = request.user
            instance.save()
            # Update the MasterProcurement instance
            procurement_instance = MasterProcurement.objects.get(id=instance.procurementId.id)
            procurement_instance.Status = request.data['status']
            procurement_instance.save()
            # Update the MasterProcurement instance
            serializer.save()
            return Response(serializer.data)
    
        elif sequence == 2:
            sequence_1_approved = ApprovalTransaction.objects.filter(procurementId=instance.procurementId, sequence=1, status='Approved').exists()
            if sequence_1_approved:
                # Update the ApprovalTransaction instance
                instance.status = request.data['status']
                instance.remarks = request.data['remarks']
                instance.create_by = request.user
                instance.update_by = request.user
                instance.save()
                # Update the MasterProcurement instance
                procurement_instance = MasterProcurement.objects.get(id=instance.procurementId.id)
                procurement_instance.Status = request.data['status']
                procurement_instance.save()
                # Update the MasterProcurement instance
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
    
        

        





        
    
        

    

        
    

    

    