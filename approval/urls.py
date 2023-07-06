from django.urls import path
from .views import *



urlpatterns = [
    path('approvalAuth/', ApprovalAuthenticateAPIView.as_view(), name='approvalAuth'),
    path('approvalPendingList/', ApprovalProcurementPendingList.as_view(), name='approvalPendingList'),
    path('approvalUpdateStatus/', ApprovalUpdateStatusAPIView.as_view(), name='approvalUpdateStatus'),
    path('approvalDetailsList/', GetProcurementApprovalTransactionDetails.as_view(), name='approvalDetailsList'),

]


