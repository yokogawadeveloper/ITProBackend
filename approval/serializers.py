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





        
