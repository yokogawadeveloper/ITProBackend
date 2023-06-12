from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *


User = get_user_model()
# Create your serializers here.

class InlineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InlineItem
        fields = ['category','item','costcenter','quantity','unitprice','totalprice']

class MasterProcurementSerializer(serializers.ModelSerializer):
    inlineitem = InlineItemSerializer(many=True)
    department_name = serializers.ReadOnlyField(source='DepartmentId.DepartmentName')
    class Meta:
        model = MasterProcurement
        fields = ['id','RequestNumber','RequestType','Name','DepartmentId', 'department_name','IsExpenditure','TotalBudget','UtilizedBudget','Remarks','PurchaseDate','Age', 'DeviceType','Status','inlineitem']

    def create(self, validated_data):
        inlineitems_data = validated_data.pop('inlineitem')
        request = self.context.get('request')
        user = request.user
        masterprocurement = MasterProcurement.objects.create(Created_by=user,Updated_by=user,**validated_data)
        for track_data in inlineitems_data:
            InlineItem.objects.create(procurement=masterprocurement, **track_data)
        return masterprocurement
    














    
    



    
    
    
    
