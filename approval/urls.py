from django.urls import path
from .views import *



urlpatterns = [
    path('approvalAuth/', ApprovalAuthenticateAPIView.as_view(), name='approvalAuth'),
    path('approvalPendingList/', LoggedInApprovalProcurementPendingList.as_view(), name='approvalPendingList'),
    path('approvalProcurementDetails/<int:pk>/', ApprovalProcurementDetailsByID.as_view(), name='approvalProcurementDetails'),
]
