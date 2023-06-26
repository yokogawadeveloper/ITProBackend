from django.contrib.auth import get_user_model
from django.db import models
from master.models import *
import datetime


User = get_user_model()

# Create your models here.
class MasterProcurement(models.Model):
    CHOICES2 = (('New', 'New'), ('Rental', 'Rental'))
    RequestNumber = models.CharField(max_length=100, null=True, blank=True)
    RequestType = models.CharField(max_length=100, null=True, blank=True)
    Name = models.CharField(max_length=100, null=True, blank=True)
    Department = models.CharField(max_length=100, null=True, blank=True)
    IsExpenditure = models.CharField(max_length=100, null=True, blank=True, default='No')
    TotalBudget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    UtilizedBudget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Remarks = models.TextField(null=True, blank=True)
    PurchaseDate = models.DateField(null=True, blank=True,default=datetime.date.today)
    Age = models.IntegerField(default=0, null=True, blank=True)
    Status = models.CharField(max_length=100, null=True, blank=True, default='Pending')
    DeviceType = models.CharField(max_length=100, choices=CHOICES2, default='New', null=True, blank=True)
    File = models.ImageField(upload_to='procurement/', null=True, blank=True)
    Created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    Updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    Created_at = models.DateTimeField(auto_now_add=True, null=True)
    Updated_at = models.DateTimeField(auto_now_add=True, null=True)

    # def save(self, *args, **kwargs):
    #     if self.RequestNumber is None or self.RequestType is not None:
    #         cureentYear = str(datetime.datetime.now().year)
    #         self.RequestNumber = ''.join([word[0] for word in self.RequestType.split()]) + cureentYear[:] + str(MasterProcurement.objects.filter(RequestType=self.RequestType).count() + 1).zfill(4)
        
    #     else:
    #         self.RequestNumber = 'PR0001'
    #     super().save(*args, **kwargs)
     
    class Meta:
        db_table = "MasterProcurement"
        ordering = ['id']
              

class InlineItem(models.Model):
    procurement = models.ForeignKey(MasterProcurement, related_name='inlineitem', on_delete=models.CASCADE,null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    item = models.CharField(max_length=100, null=True, blank=True)
    costcenter = models.ForeignKey(MasterCostCenter, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    unitprice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True , default=0.00)
    totalprice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    
    objects = models.Manager()

    class Meta:
        db_table = "InlineItem"
        ordering = ['id']


class Attachments(models.Model):
    request = models.ForeignKey(MasterProcurement, related_name='attachments', on_delete=models.CASCADE , null=True, blank=True)
    file = models.FileField(upload_to='procurement/%Y/%m/%d/%H_%M_%S', null=True, blank=True)
    filetype = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "Attachments"
        verbose_name_plural = "Attachments"



class UploadFile(models.Model):
    uploads = models.ImageField(upload_to='procurement/', null=True, blank=True)
    filetype = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "UploadFile"
        verbose_name_plural = "UploadFile"
    








    

