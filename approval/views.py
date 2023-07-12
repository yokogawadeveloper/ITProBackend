from django.db.models import Q
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from procurement.serializers import *
from .serializers import *

User = get_user_model()

# Create your views here.
class GetModuleAccessViewSet(viewsets.ModelViewSet):
    serializer_class = ModuleAccessSerializer
    queryset = ModuleAccess.objects.all()

    def get_queryset(self):
        queryset = ModuleAccess.objects.all()
        return queryset

    @action(methods=['post'], detail=False, url_path='getModuleAccess')
    def getModuleAccess(self, request):
        data = request.data
        is_admin = data['is_admin']
        is_approver = data['is_approver']
        is_dsin = data['is_dsin']
        is_requester = data['is_requester']
        arr = []
        module_ids = []

        if is_admin == True:
            queryset = ModuleAccess.objects.filter(is_admin=True).values_list('moduleId_id', flat=True)
            module_ids = list(queryset)

        if is_approver == True:
            queryset = ModuleAccess.objects.filter(is_approver=True).values_list('moduleId_id', flat=True)
            module_ids.extend(list(queryset))

        if is_dsin == True:
            queryset = ModuleAccess.objects.filter(is_dsin=True).values_list('moduleId_id', flat=True)
            module_ids.extend(list(queryset))

        if is_requester == True:
            queryset = ModuleAccess.objects.filter(is_requester=True).values_list('moduleId_id', flat=True)
            module_ids.extend(list(queryset))

        module_ids = list(set(module_ids))

        for i in module_ids:
            root = ModuleMaster.objects.filter(moduleId=i).values('root')[0]['root']
            if root == 'ROOT':
                filter_module_root = ModuleMaster.objects.filter(moduleId=i)
                filter_module_root = ModuleMasterSerializer(filter_module_root, many=True, context={'request': request})
                filter_module_root = filter_module_root.data
                filter_module_submenu = ModuleMaster.objects.filter(root=i, moduleId__in=module_ids)
                filter_module_submenu = ModuleMasterSerializer(filter_module_submenu, many=True,
                                                               context={'request': request})
                filter_module_submenu = filter_module_submenu.data

                arr.append({"module_id": filter_module_root[0]['moduleId'],
                            "module_name": filter_module_root[0]['module_name'],
                            "module_slug": filter_module_root[0]['module_slug'],
                            "root": filter_module_root[0]['root'],
                            "m_color": filter_module_root[0]['m_color'],
                            "m_icon_name": filter_module_root[0]['m_icon_name'],
                            "m_link": filter_module_root[0]['m_link'],
                            "root_module": filter_module_submenu})

        return Response({
            'message': 'success',
            'module_ids': arr
        })



class ApprovalProcurementPendingList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        transaction = ApprovalTransaction.objects.filter(approvalUserName=user, status='Pending')
        serializer = ApprovalTransactionSerializer(transaction, many=True, context={'request': request})

        if serializer.data[0]['sequence'] == 1:
            return Response({
                'message': 'success',
                'data': serializer.data
            })

        elif serializer.data[0]['sequence'] > 1:
            previous_transaction = ApprovalTransaction.objects.filter(procurementId=serializer.data[0]['procurementId'], sequence=serializer.data[0]['sequence']-1)
            # check if previous transaction is approved
            if previous_transaction:
                status = previous_transaction[0].status
                if status == 'Approved':
                    return Response({
                        'message': 'success',
                        'data': serializer.data
                    })
                else:
                    return Response({
                        'message': 'failed',
                        'data': []
                    })

            else:
                return Response({
                    'message': 'failed',
                    'data': []
                })



class ApprovalUpdateStatusAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        if request.query_params.get('procurementId') and request.query_params.get('sequenceId'):
            procurement_id = int(request.query_params.get('procurementId'))
            sequence = int(request.query_params.get('sequenceId'))
            try:
                instance = ApprovalTransaction.objects.get(procurementId=procurement_id, sequence=sequence)

            except ApprovalTransaction.DoesNotExist:
                return Response({
                    'message': 'Approval transaction does not exist',
                    'status': 'failed'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = ApprovalTransactionSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            if sequence == 1:
                previous_approver_email = instance.approverEmail
                previous_approver_sequence = instance.sequence
                instance.status = request.data['status']
                instance.approvaldatetime = datetime.datetime.now(tz=timezone.utc)
                instance.create_by = request.user
                instance.update_by = request.user
                instance.save()
                # Update the next approver status
                new_sequence_number = previous_approver_sequence + 1
                if new_sequence_number == 2:
                    next_approver = ApprovalTransaction.objects.filter(procurementId=procurement_id,
                                                                       sequence=new_sequence_number).values(
                        'approverEmail')[0]['approverEmail']
                    if next_approver == previous_approver_email:
                        ApprovalTransaction.objects.filter(procurementId=procurement_id,
                                                           sequence=new_sequence_number).update(
                            status=request.data['status'], approvaldatetime=datetime.datetime.now(tz=timezone.utc))
                # Update the MasterProcurement instance
                procurement_instance = MasterProcurement.objects.get(id=instance.procurementId.id)
                procurement_instance.Status = request.data['status']
                procurement_instance.save()
                serializer.save()
                return Response(serializer.data)


            elif sequence != 1:
                instance.status = request.data['status']
                instance.approvaldatetime = datetime.datetime.now(tz=timezone.utc)
                instance.create_by = request.user
                instance.update_by = request.user
                instance.save()
                # Update the MasterProcurement instance
                procurement_instance = MasterProcurement.objects.get(id=instance.procurementId.id)
                procurement_instance.Status = request.data['status']
                procurement_instance.save()
                serializer.save()
                return Response(serializer.data)
        else:
            return Response({
                'message': 'Please provide the procurementId and sequenceId',
                'status': 'failed'
            }, status=status.HTTP_400_BAD_REQUEST)


class ApprovalProcurementModificationList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        ApprovalUser = ApprovalTransaction.objects.filter(
            ApprovalTransaction.objects.filter(Q(approvalUserName=user) & Q(status='Modification')))

        if ApprovalUser.exists():
            serializer = ApprovalTransactionSerializer(ApprovalUser, many=True)
            data_list = []
            for data in serializer.data:
                procurement = MasterProcurement.objects.get(id=data['procurementId'])
                procurement_serializer = MasterProcurementSerializer(procurement)
                updated_data = {
                    'id': data['id'],
                    'approvalUserName': data['approvalUserName'],
                    'approverEmail': data['approverEmail'],
                    'sequence': data['sequence'],
                    'approverType': data['approverType'],
                    'status': data['status'],
                    'procurementId': {
                        'id': data['procurementId'],
                        'sequence': data['sequence'],  # Include the sequence here
                        'approverType': data['approverType'],
                        'sequence_status': data['status'],  # Include the status here
                        'RequestNumber': procurement_serializer.data['RequestNumber'],
                        'RequestType': procurement_serializer.data['RequestType'],
                        'Name': procurement_serializer.data['Name'],
                        'Status': procurement_serializer.data['Status'],
                        'TotalBudget': procurement_serializer.data['TotalBudget'],
                        'UtilizedBudget': procurement_serializer.data['UtilizedBudget'],
                        'Department': procurement_serializer.data['Department'],
                    }
                }
                data_list.append(updated_data)
            return Response(data_list)
        else:
            return Response({'error': 'No pending approval'})


class GetProcurementApprovalTransactionDetails(APIView):
    serializer_class = ApprovalTransactionSerializer

    def get(self, request, *args, **kwargs):
        if request.query_params.get('procurementId') and request.query_params.get('sequenceId'):
            # get the procurement id and sequence id
            procurement_id = int(request.query_params.get('procurementId'))
            sequence = int(request.query_params.get('sequenceId'))
            try:
                instance = ApprovalTransaction.objects.get(procurementId=procurement_id, sequence=sequence)
            except ApprovalTransaction.DoesNotExist:
                return Response({'error': 'Approval transaction does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            # 
            serializer = ApprovalTransactionSerializer(instance)
            procurement_instance = MasterProcurement.objects.get(id=serializer.data['procurementId'])
            procurement_serializer = MasterProcurementSerializer(procurement_instance)

            return Response({
                'procurementId': serializer.data['procurementId'],
                'sequence': serializer.data['sequence'],
                'Approver': serializer.data['approvalUserName'],
                'Email': serializer.data['approverEmail'],
                'RequestNumber': procurement_serializer.data['RequestNumber'],
                'RequestType': procurement_serializer.data['RequestType'],
                'Name': procurement_serializer.data['Name'],
                'Status': procurement_serializer.data['Status'],
                'IsExpenditure': procurement_serializer.data['IsExpenditure'],
                'TotalBudget': procurement_serializer.data['TotalBudget'],
                'UtilizedBudget': procurement_serializer.data['UtilizedBudget'],
                'Department': procurement_serializer.data['Department'],
                'inlineitem': procurement_serializer.data['inlineitem'],
            })
        else:
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

#
# class ApprovalProcurementPendingList(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         ApprovalUser = ApprovalTransaction.objects.filter(Q(approvalUserName=user) & Q(status='Pending'))
#         if ApprovalUser.exists():
#             serializer = ApprovalTransactionSerializer(ApprovalUser, many=True)
#             data_list = []
#             for data in serializer.data:
#                 procurement = MasterProcurement.objects.get(id=data['procurementId'])
#                 if procurement:
#                     procurement_serializer = MasterProcurementSerializer(procurement)
#                     updated_data = {
#                         'id': data['id'],
#                         'approvalUserName': data['approvalUserName'],
#                         'approverEmail': data['approverEmail'],
#                         'sequence': data['sequence'],
#                         'approverType': data['approverType'],
#                         'status': data['status'],
#                         'procurementId': {
#                             'id': data['procurementId'],
#                             'sequence': data['sequence'],  # Include the sequence here
#                             'approverType': data['approverType'],
#                             'sequence_status': data['status'],  # Include the status here
#                             'RequestNumber': procurement_serializer.data['RequestNumber'],
#                             'RequestType': procurement_serializer.data['RequestType'],
#                             'Name': procurement_serializer.data['Name'],
#                             'Status': procurement_serializer.data['Status'],
#                             'TotalAmount': procurement_serializer.data['TotalAmount'],
#                             'TotalBudget': procurement_serializer.data['TotalBudget'],
#                             'UtilizedBudget': procurement_serializer.data['UtilizedBudget'],
#                             'Department': procurement_serializer.data['Department'],
#                         }
#                     }
#                     data_list.append(updated_data)
#                     return Response(data_list)
#                 else:
#                     return Response({'error': 'No pending approval'})
#         else:
#             return Response({'error': 'No pending approval'})

#
# class ApprovalProcurementPendingList(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         transaction = ApprovalTransaction.objects.filter(approverEmail=user.email, status='Pending').values(
#             'procurementId')
#         procurement_ids = [i['procurementId'] for i in transaction]
#         previous_sequence = 1
#         if len(procurement_ids) > 0:
#             previous_sequence = \
#             ApprovalTransaction.objects.filter(procurementId__in=procurement_ids).values('sequence').order_by(
#                 '-sequence')[0]['sequence']
#
#         procurement_list = MasterProcurement.objects.filter(id__in=procurement_ids)
#         serializer = MasterProcurementSerializer(procurement_list, many=True, context={'request': request})
#         return Response({
#             'message': 'success',
#             'procurement_list': serializer.data
#         })
