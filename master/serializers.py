from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *


User = get_user_model()
# Create your serializers here.

class MasterDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterDepartment
        fields = '__all__'
        read_only_fields = ['id']
        

    def create(self, validated_data):
        return MasterDepartment.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.DepartmentName = validated_data.get('DepartmentName', instance.DepartmentName)
        instance.DepartmentHead = validated_data.get('DepartmentHead', instance.DepartmentHead)
        instance.DepartmentAdministrator = validated_data.get('DepartmentAdministrator', instance.DepartmentAdministrator)
        instance.DepartmentSubAdministrator = validated_data.get('DepartmentSubAdministrator', instance.DepartmentSubAdministrator)
        instance.BUCode = validated_data.get('BUCode', instance.BUCode)
        instance.BoolInUse = validated_data.get('BoolInUse', instance.BoolInUse)
        instance.save()
        return instance
    
    def validated_name(self, value):
        qs = MasterDepartment.objects.filter(DepartmentName__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("The DepartmentName must be unique")
        


class MasterCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterCategory
        fields = '__all__'
        read_only_fields = ['id']
        

    def create(self, validated_data):
        return MasterCategory.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.ItemCategory = validated_data.get('ItemCategory', instance.ItemCategory)
        instance.BoolInUse = validated_data.get('BoolInUse', instance.BoolInUse)
        instance.save()
        return instance
    
    def validated_ItemCategory(self, value):
        qs = MasterCategory.objects.filter(ItemCategory__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("The ItemCategory must be unique")
    
    

class MasterItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='ItemCategoryId.ItemCategory', read_only=True)
    class Meta:
        model = MasterItem
        fields = '__all__'
        read_only_fields = ['id']


    def create(self, validated_data):
        return MasterItem.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        instance.ItemName = validated_data.get('ItemName', instance.ItemName)
        instance.ItemCategoryId = validated_data.get('ItemCategoryId', instance.ItemCategoryId)
        instance.UnitPrice = validated_data.get('UnitPrice', instance.UnitPrice)
        instance.BoolInUse = validated_data.get('BoolInUse', instance.BoolInUse)
        instance.save()
        return instance
    
    def validated_name(self, value):
        qs = MasterItem.objects.filter(ItemName__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("The ItemName must be unique")
    


class MasterCostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterCostCenter
        fields = '__all__'
        read_only_fields = ['id']


    def create(self, validated_data):
        return MasterCostCenter.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.CostCenter = validated_data.get('CostCenter', instance.CostCenter)
        instance.Name = validated_data.get('Name', instance.Name)
        instance.BUSA = validated_data.get('BUSA', instance.BUSA)
        instance.IsExisting = validated_data.get('IsExisting', instance.IsExisting)
        instance.save()
        return instance
    

        

    
    
    



