from rest_framework import routers
from django.urls import path, include
from .views import *



urlpatterns = [
    path('createprocurement/', MasterProcurementCreateAPIView.as_view()),
    ]