from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
from procurement.models import *
from django.db.models import Q

User =  get_user_model()

# Create serialiazers here..
class ApproverMatrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApproverMatrix
        fields = '__all__'



class ApprovalTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalTransaction
        fields = '__all__'




class ProcurementApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterProcurement
        fields = '__all__'
        depth = 1

class ApprovalProcurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterProcurement
        fields = '__all__'
        depth = 1


class ApprovalProcurementDetailsByIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterProcurement
        fields = '__all__'
        depth = 1

class ApprovalProcurementDetailsByProcurementIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = MasterProcurement
        fields = '__all__'
        depth = 1
        
        
        





        
