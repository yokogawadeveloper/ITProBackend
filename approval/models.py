from django.db import models
from django.contrib.auth import get_user_model
from procurement.models import MasterProcurement

User = get_user_model()
# Create your models here.
class ApproverMatrix(models.Model):
    request_type = models.CharField(max_length=100, blank=True, null=True)
    primary_approver = models.CharField(max_length=100, blank=True, null=True)
    secondary_approver = models.CharField(max_length=100, blank=True, null=True)
    sequence = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = "ApproverMatrix"
        verbose_name_plural = "ApproverMatrix"


class ApprovalTransaction(models.Model):
    CHOICES = (('BuHead', 'BuHead'), ('DSINHead', 'DSINHead'),('FinanceHead', 'FinanceHead'),('MD', 'MD'),
    ('DSINMPR', 'DSINMPR'))
    procurementId = models.ForeignKey(MasterProcurement, on_delete=models.CASCADE)
    approvalUserName = models.CharField(max_length=100, blank=True, null=True)
    approverEmail = models.EmailField(max_length=100, blank=True, null=True)
    sequence = models.IntegerField(default=0, blank=True, null=True)
    approverType = models.CharField(max_length=100, blank=True, null=True, choices=CHOICES)
    status = models.CharField(max_length=100, blank=True, null=True, default='Pending')
    remarks = models.CharField(max_length=100, blank=True, null=True)
    approvaldatetime = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "ApprovalTransaction"
        verbose_name_plural = "ApprovalTransaction"
        ordering = ['id']


    
        

