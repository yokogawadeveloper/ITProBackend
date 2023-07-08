import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from procurement.serializers import *
from .serializers import *

User = get_user_model()


# Create your views here.
class ApprovalAuthenticateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        ApproverUser1 = ApprovalTransaction.objects.filter(approvalUserName=user).first()
        # get the first object of the queryset

        print('ApproverUser', ApproverUser1)
        ApprovalUser = ApprovalTransaction.objects.filter(Q(approvalUserName=user) & Q(status='Pending')).order_by(
            'sequence')
        # print('ApprovalUser', ApprovalUser)
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


class ApprovalProcurementPendingList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        ApprovalUser = ApprovalTransaction.objects.filter(Q(approvalUserName=user) & Q(status='Pending'))

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
                    }
                }
                data_list.append(updated_data)
            return Response(data_list)
        else:
            return Response({'error': 'No pending approval'})


class ApprovalUpdateStatusAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        if request.query_params.get('procurementId') and request.query_params.get('sequenceId'):
            procurement_id = int(request.query_params.get('procurementId'))
            sequence = int(request.query_params.get('sequenceId'))
            try:
                instance = ApprovalTransaction.objects.get(procurementId=procurement_id, sequence=sequence)
            except ApprovalTransaction.DoesNotExist:
                return Response(
                    {'error': 'Approval transaction does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = ApprovalTransactionSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            if request.data['status'] == 'Approved':

                if sequence == 1:
                    # Update the ApprovalTransaction instance
                    instance.status = request.data['status']
                    instance.create_by = request.user
                    instance.update_by = request.user
                    instance.save()

                    # Update the MasterProcurement instance
                    procurement_instance = MasterProcurement.objects.get(id=instance.procurementId.id)
                    procurement_instance.Status = 'Approved By BuHead'
                    procurement_instance.save()

                    serializer.save()
                    return Response(serializer.data)

                elif sequence == 2:
                    sequence_1_approved = ApprovalTransaction.objects.filter(procurementId=instance.procurementId,
                                                                             sequence=1, status='Approved').exists()
                    if sequence_1_approved:
                        # Update the ApprovalTransaction instance
                        instance.status = request.data['status']
                        instance.create_by = request.user
                        instance.update_by = request.user
                        instance.save()

                        # Update the MasterProcurement instance
                        procurement_instance = MasterProcurement.objects.get(id=instance.procurementId.id)
                        procurement_instance.Status = 'Approved Stage 2'
                        procurement_instance.save()

                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response({'error': 'Sequence 1 approval is required'},
                                        status=status.HTTP_400_BAD_REQUEST)

                elif sequence == 3:
                    sequence_2_approved = ApprovalTransaction.objects.filter(procurementId=instance.procurementId,
                                                                             sequence=2, status='Approved').exists()
                    if sequence_2_approved:
                        instance.status = request.data['status']
                        instance.create_by = request.user
                        instance.update_by = request.user
                        instance.save()

                        # Update the MasterProcurement instance
                        procurement_instance = MasterProcurement.objects.get(id=instance.procurementId.id)
                        procurement_instance.Status = 'Approved Stage 3'
                        procurement_instance.save()

                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response({'error': 'Sequence 2 approval is required'},
                                        status=status.HTTP_400_BAD_REQUEST)

                elif sequence == 4:
                    sequence_3_approved = ApprovalTransaction.objects.filter(procurementId=instance.procurementId,
                                                                             sequence=3, status='Approved').exists()
                    if sequence_3_approved:
                        instance.status = request.data['status']
                        instance.create_by = request.user
                        instance.update_by = request.user
                        instance.save()

                        # Update the MasterProcurement instance
                        procurement_instance = MasterProcurement.objects.get(id=instance.procurementId.id)
                        procurement_instance.Status = 'Approved Stage 4'
                        procurement_instance.save()

                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response({'error': 'Sequence 3 approval is required'},
                                        status=status.HTTP_400_BAD_REQUEST)

                elif sequence == 5:
                    sequence_4_approved = ApprovalTransaction.objects.filter(procurementId=instance.procurementId,
                                                                             sequence=4, status='Approved').exists()
                    if sequence_4_approved:
                        instance.status = request.data['status']
                        instance.create_by = request.user
                        instance.update_by = request.user
                        instance.save()

                        # Update the MasterProcurement instance
                        procurement_instance = MasterProcurement.objects.get(id=instance.procurementId.id)
                        procurement_instance.Status = 'Approved'
                        procurement_instance.save()

                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response({'error': 'Sequence 4 approval is required'},
                                        status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({'error': 'Invalid sequence'}, status=status.HTTP_400_BAD_REQUEST)

            elif request.data['status'] == 'Modification':
                if sequence == 1:
                    instance.status = request.data['status']
                    instance.create_by = request.user
                    instance.update_by = request.user
                    instance.save()
                    # Update the MasterProcurement instance
                    procurement_instance = MasterProcurement.objects.get(id=instance.procurementId.id)
                    procurement_instance.Status = 'Modification By BuHead'
                    procurement_instance.save()

                    serializer.save()
                    return Response(serializer.data)

                elif sequence == 2:
                    sequence_1_approved = ApprovalTransaction.objects.filter(procurementId=instance.procurementId,
                                                                             sequence=1, status='Approved').exists()
                    if sequence_1_approved:
                        instance.status = request.data['status']
                        instance.create_by = request.user
                        instance.update_by = request.user
                        instance.save()
                        # Update the MasterProcurement instance
                        procurement_instance = MasterProcurement.objects.get(id=instance.procurementId.id)
                        procurement_instance.Status = 'Approved Stage 2'
                        procurement_instance.save()
                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response({'error': 'Sequence 1 approval is required'},
                                        status=status.HTTP_400_BAD_REQUEST)

                elif sequence == 3:
                    sequence_2_approved = ApprovalTransaction.objects.filter(procurementId=instance.procurementId,
                                                                             sequence=2, status='Approved').exists()
                    if sequence_2_approved:
                        instance.status = request.data['status']
                        instance.create_by = request.user
                        instance.update_by = request.user
                        instance.save()
                        # Update the MasterProcurement instance
                        procurement_instance = MasterProcurement.objects.get(id=instance.procurementId.id)
                        procurement_instance.Status = 'Approved Stage 3'
                        procurement_instance.save()
                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response({'error': 'Sequence 2 approval is required'},
                                        status=status.HTTP_400_BAD_REQUEST)

                elif sequence == 4:
                    sequence_3_approved = ApprovalTransaction.objects.filter(procurementId=instance.procurementId,
                                                                             sequence=3, status='Approved').exists()
                    if sequence_3_approved:
                        instance.status = request.data['status']
                        instance.create_by = request.user
                        instance.update_by = request.user
                        instance.save()
                        # Update the MasterProcurement instance
                        procurement_instance = MasterProcurement.objects.get(id=instance.procurementId.id)
                        procurement_instance.Status = 'Approved Stage 4'
                        procurement_instance.save()
                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response({'error': 'Sequence 3 approval is required'},
                                        status=status.HTTP_400_BAD_REQUEST)

                elif sequence == 5:
                    sequence_4_approved = ApprovalTransaction.objects.filter(procurementId=instance.procurementId,
                                                                             sequence=4, status='Approved').exists()
                    if sequence_4_approved:
                        instance.status = request.data['status']
                        instance.create_by = request.user
                        instance.update_by = request.user
                        instance.save()
                        # Update the MasterProcurement instance
                        procurement_instance = MasterProcurement.objects.get(id=instance.procurementId.id)
                        procurement_instance.Status = 'Approved'
                        procurement_instance.save()

                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response({'error': 'Sequence 4 approval is required'},
                                        status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({'error': 'Invalid sequence'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'error': 'You are not authorized to perform this action'
            }, status=status.HTTP_401_UNAUTHORIZED)


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
                'inlineitem': procurement_serializer.data['inlineitem'],
            })
        else:
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


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
        print(is_admin, is_approver, is_dsin, is_requester)

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
                filter_module_submenu = ModuleMasterSerializer(filter_module_submenu, many=True, context={'request': request})
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