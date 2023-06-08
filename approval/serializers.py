from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

User =  get_user_model()

# Create serialiazers here..
class ApproverMatrixSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source="User.username")
    class Meta:
        model = ApproverMatrix
        fields = '__all__'




        
