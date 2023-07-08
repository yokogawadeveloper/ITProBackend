from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

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
        # depth = 1

class ModuleMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleMaster
        fields = '__all__'
        # depth = 1

        

class ModuleAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleAccess
        fields = '__all__'
        # depth = 1



        
