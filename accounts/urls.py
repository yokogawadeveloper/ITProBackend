from django.urls import path
from .views import *

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('userprofile/', EmployeeUserAPIView.as_view(), name='employee'),
]

