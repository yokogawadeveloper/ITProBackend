from rest_framework import serializers

from .models import *

User = get_user_model()


# Create your serializers here.
class AttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachments
        fields = ['file', 'filetype']


class InlineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InlineItem
        fields = ['category', 'item', 'costcenter', 'quantity', 'unitprice', 'totalprice']


class MasterProcurementSerializer(serializers.ModelSerializer):
    # inlineitem = InlineItemSerializer(many=True)
    class Meta:
        model = MasterProcurement
        fields = ['id', 'RequestNumber', 'RequestType', 'Name', 'Department', 'IsExpenditure', 'TotalBudget', 'File',
                  'UtilizedBudget', 'Remarks', 'PurchaseDate', 'Age', 'DeviceType', 'Status']

    # def create(self, validated_data):
    #     inlineitems_data = validated_data.pop('inlineitem')
    #     request = self.context['request']
    #     user = request.user
    #     masterprocurement = MasterProcurement.objects.create(Created_by=user, **validated_data)
    #     # create inlineitems
    #     for track_data in inlineitems_data:
    #         InlineItem.objects.create(procurement=masterprocurement, **track_data)

    #     return masterprocurement

    # def update(self, instance, validated_data):
    #     inlineitems_data = validated_data.pop('inlineitem', [])
    #     instance = super().update(instance, validated_data)

    #     # Delete any items not in the request
    #     items = [item['id'] for item in inlineitems_data if 'id' in item]
    #     for item in instance.inlineitem.all():
    #         if item.id not in items:
    #             item.delete()

    #     # Create or update instance items
    #     for item in inlineitems_data:
    #         if 'id' in item:
    #             item_instance = InlineItem.objects.get(id=item['id'])
    #             InlineItem.objects.filter(id=item['id']).update(**item)
    #         else:
    #             InlineItem.objects.create(procurement=instance, **item)

    #     return instance



class MasterProcurementSerializer2(serializers.ModelSerializer):
    attachments = AttachmentsSerializer(many=True, required=False)
    class Meta:
        model = MasterProcurement
        fields = '__all__'

    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments', [])
        master_procurement = MasterProcurement.objects.create(**validated_data)
        for attachment_data in attachments_data:
            Attachments.objects.create(request=master_procurement, **attachment_data)
        return master_procurement

class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = '__all__'