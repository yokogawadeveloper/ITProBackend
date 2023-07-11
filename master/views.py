from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .serializers import *
from .models import *


User = get_user_model()


# Create your views here.
class MasterCategoryViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return MasterCategory.objects.filter(IsActive=True)
    
    def get_serializer_class(self):
        return MasterCategorySerializer
    

    def list(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)
    
    
    def create(self, request, *args, **kwargs):
        serializer = MasterCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MasterCategorySerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MasterCategorySerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class MasterItemViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return MasterItem.objects.filter(IsActive=True)
    
    def get_serializer_class(self):
        return MasterItemSerializer
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
    def create(self, request, *args, **kwargs):
        serializer = MasterItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MasterItemSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MasterItemSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='getItemListBasedOnCategory')
    def getItemListBasedOnCategory(self, request):
        data = request.data
        ItemCategoryId = data['ItemCategoryId']
        filter_data = self.get_queryset().filter(ItemCategoryId=ItemCategoryId)
        serializer = MasterItemSerializer(filter_data, many=True, context={'request': request})
        serializer_data = serializer.data
        return Response(serializer_data)
    


class MasterDepartmentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return MasterDepartment.objects.filter(IsActive=True)
    
    def get_serializer_class(self):
        return MasterDepartmentSerializer
    

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
    def create(self, request, *args, **kwargs):
        serializer = MasterDepartmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MasterDepartmentSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MasterDepartmentSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class MasterCostCenterViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return MasterCostCenter.objects.all()
    
    def get_serializer_class(self):
        return MasterCostCenterSerializer
    

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = MasterCostCenterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MasterCostCenterSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MasterCostCenterSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


    
