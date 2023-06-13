from django.db import models
from django.contrib.auth import get_user_model
from procurement.models import MasterProcurement

User = get_user_model()
# Create your models here.
class ApproverMatrix(models.Model):
    request_type = models.CharField(max_length=100, blank=True, null=True)
    primary_approver = models.CharField(max_length=100, blank=True, null=True)
    secondary_approver = models.CharField(max_length=100, blank=True, null=True)
    sequence = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = "ApproverMatrix"
        verbose_name_plural = "ApproverMatrix"


class ApprovalTransaction(models.Model):
    CHOICES = (('BuHead', 'BuHead'), ('DSINHead', 'DSINHead'),('FinanceHead', 'FinanceHead'),('MD', 'MD'),
    ('DSINMPR', 'DSINMPR'))
    procurementId = models.ForeignKey(MasterProcurement, on_delete=models.CASCADE)
    approvalUserName = models.CharField(max_length=100, blank=True, null=True)
    approverEmail = models.EmailField(max_length=100, blank=True, null=True)
    sequence = models.IntegerField(default=0, blank=True, null=True)
    approverType = models.CharField(max_length=100, blank=True, null=True, choices=CHOICES)
    status = models.CharField(max_length=100, blank=True, null=True, default='Pending')
    remarks = models.CharField(max_length=100, blank=True, null=True)
    approvaldatetime = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "ApprovalTransaction"
        verbose_name_plural = "ApprovalTransaction"
        ordering = ['id']




# class LoggedInApprovalProcurementPendingList(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         ApprovalUser = ApprovalTransaction.objects.filter(Q(approvalUserName = user) & Q(status='Pending'))
#         ApproverSequence = ApprovalUser.values_list('sequence', flat=True)
#         print(ApproverSequence)
#         ProcurementId = ApprovalUser.values_list('procurementId', flat=True)
#         ProcurementDetails = MasterProcurement.objects.filter(id__in=ProcurementId)
#         if ApprovalUser.exists():
#             serializer = MasterProcurementSerializer(ProcurementDetails, many=True)
#             return Response(serializer.data)
#         else:
#             return Response({'error': 'No pending approval'})




# class LoggedInApprovalProcurementPendingList(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         ApprovalUser = ApprovalTransaction.objects.filter(Q(approvalUserName = user) & Q(status='Pending'))
#         if ApprovalUser.exists():
#             serializer = ApprovalTransactionSerializer(ApprovalUser, many=True)
#             for data in serializer.data:
#                 procurement = MasterProcurement.objects.get(id=data['procurementId'])
#                 procurement_serializer = MasterProcurementSerializer(procurement)
#                 data['procurementId'] = procurement_serializer.data
#             return Response(serializer.data)
            
#         else:
#             return Response({'error': 'No pending approval'})


# class LoggedInApprovalProcurementPendingList(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         ApprovalUser = ApprovalTransaction.objects.filter(Q(approvalUserName = user) & Q(status='Pending'))
#         if ApprovalUser.exists():
#             serializer = ApprovalTransactionSerializer(ApprovalUser, many=True)
#             procurementData = []
#             for data in serializer.data:
#                 procurement = MasterProcurement.objects.get(id=data['procurementId'])
#                 procurement_serializer = MasterProcurementSerializer(procurement)
#                 procurementData.append(procurement_serializer.data)
#             return Response(procurementData)
            
#         else:
#             return Response({'error': 'No pending approval'})
    
        



# class LoggedInApprovalProcurementPendingList(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         user = request.user
#         ApprovalUser = ApprovalTransaction.objects.filter(Q(approvalUserName=user) & Q(status='Pending'))
#         if ApprovalUser.exists():
#             serializer = ApprovalTransactionSerializer(ApprovalUser, many=True)
#             data_list = []
#             for data in serializer.data:
#                 procurement = MasterProcurement.objects.get(id=data['procurementId'])
#                 procurement_serializer = MasterProcurementSerializer(procurement)
#                 updated_data = {
#                     'id': data['id'],
#                     'approvalUserName': data['approvalUserName'],
#                     'approverEmail': data['approverEmail'],
#                     'sequence': data['sequence'],
#                     'approverType': data['approverType'],
#                     'status': data['status'],
#                     'procurementId': {
#                         'id': data['procurementId'],
#                         'sequence': data['sequence'],  # Include the sequence here
#                         'approverType': data['approverType'],
#                         'RequestNumber': procurement_serializer.data['RequestNumber'],
#                         'RequestType': procurement_serializer.data['RequestType'],
#                         'Name': procurement_serializer.data['Name'],
#                         'Status': procurement_serializer.data['Status'],
#                     }
#                 }
#                 data_list.append(updated_data)
#             return Response(data_list)
#         else:
#             return Response({'error': 'No pending approval'})

