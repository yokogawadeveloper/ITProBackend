from django.urls import path
from .views import *



urlpatterns = [
    path('approvalAuth/', ApprovalAuthenticateAPIView.as_view(), name='approvalAuth'),
    path('approvalPendingList/', LoggedInApprovalProcurementPendingList.as_view(), name='approvalPendingList'),
    path('approvalProcurementDetails/<int:pk>/', ApprovalProcurementDetailsByID.as_view(), name='approvalProcurementDetails'),
    path('approvalProcurementDetails/<int:pk>/approve/', ApprovalProcurementDetailsByID.as_view(), name='approvalProcurementDetails'),
]



# 'id': serializer.data['id'],
#             'sequence': approval_transaction_serializer.data[0]['sequence'],
#             'procurement': serializer.data,
#             'inlineitem': serializer.data['inlineitem'],