from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from master.models import *
import datetime


User = get_user_model()

# Create your models here.
class MasterUpload(models.Model):
    File = models.FileField(upload_to='procurement/%Y/%m/%d/%H_%M_%S', null=True, blank=True)
    FileType = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "MasterUpload"
        verbose_name_plural = "MasterUpload"
    

class MasterProcurement(models.Model):
    CHOICES2 = (('New', 'New'), ('Rental', 'Rental'))
    RequestNumber = models.CharField(max_length=100, null=True, blank=True)
    RequestType = models.CharField(max_length=100, null=True, blank=True)
    Name = models.CharField(max_length=100, null=True, blank=True)
    DepartmentId = models.ForeignKey(MasterDepartment, on_delete=models.CASCADE, null=True, blank=True)
    IsExpenditure = models.BooleanField(default=False, null=True, blank=True)
    TotalBudget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    UtilizedBudget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Remarks = models.TextField(null=True, blank=True)
    PurchaseDate = models.DateField(null=True, blank=True,default=datetime.date.today)
    Age = models.IntegerField(default=0, null=True, blank=True)
    Status = models.CharField(max_length=100, null=True, blank=True, default='Pending')
    DeviceType = models.CharField(max_length=100, choices=CHOICES2, null=True, blank=True)
    Attachment = models.ForeignKey(MasterUpload, on_delete=models.CASCADE, null=True, blank=True)
    Created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    Updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    Created_at = models.DateTimeField(auto_now_add=True, null=True)
    Updated_at = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        created = not self.pk
        if created and not self.RequestNumber and self.RequestType:
            cureentYear = str(datetime.datetime.now().year)
            self.RequestNumber = ''.join([word[0] for word in self.RequestType.split()]) + cureentYear[:] + str(MasterProcurement.objects.filter(RequestType=self.RequestType).count() + 1).zfill(4)
        super().save(*args, **kwargs)
        if created:
            from approval.models import ApprovalTransaction ,ApproverMatrix
            appmat = ApproverMatrix.objects.filter(request_type=self.RequestType).order_by('sequence')
            for app in appmat:
                if app.sequence == 1:
                    userOrgDept = User.objects.get(id=self.Created_by.id).OrgDepartmentId
                    userOrgDeptHead = OrgDepartmentHead.objects.filter(OrgDepartment_id=userOrgDept).first()
                    userOrgDeptHeadEmail = User.objects.get(username=userOrgDeptHead.Head).email
                    approverEmail = userOrgDeptHeadEmail
                    userId = User.objects.get(username=userOrgDeptHead.Head)
                    #create approval transaction
                    ApprovalTransaction.objects.create(
                    procurementId=self,
                    approverEmail=approverEmail,
                    approvalUserName=userId.username,
                    sequence=app.sequence,
                    approverType='BuHead',
                    status='Pending',
                                )

                elif app.sequence == 2:
                    email = 'Jiya.K@yokogawa.com'
                    user = User.objects.get(email = email)
                    is_dsinhead = True
                    #create approval transaction
                    ApprovalTransaction.objects.create(
                    procurementId=self,
                    approvalUserName=user.username,
                    approverEmail=email,
                    sequence=app.sequence,
                    approverType='DSINHead',
                    status='Pending',
                                )

                elif app.sequence == 3:
                    email = 'ganeshchandra.p@yokogawa.com'
                    user = User.objects.get(email = email)
                    is_financehead = True
                    #create approval transaction
                    ApprovalTransaction.objects.create(
                    procurementId=self,
                    approvalUserName=user.username,
                    approverEmail=email,
                    sequence=app.sequence,
                    approverType='FinanceHead',
                    status='Pending',
                                )

                elif app.sequence == 4:
                    email = 'sajiv.nath@yokogawa.com'
                    user = User.objects.get(email = email)
                    is_md = True
                    #create approval transaction
                    ApprovalTransaction.objects.create(
                    procurementId=self,
                    approvalUserName=user.username,
                    approverEmail=email,
                    sequence=app.sequence,
                    approverType='MD',
                    status='Pending',
                                )
                elif app.sequence == 5:
                    email = 'Naveen.R@yokogawa.com' 
                    user = User.objects.get(email = email)
                    is_dsinmprhead = True

                    ApprovalTransaction.objects.create(
                    procurementId=self,
                    approvalUserName=user.username,
                    approverEmail=email,
                    sequence=app.sequence,
                    approverType='DSINMPR',
                    status='Pending',
                                )
                
    class Meta:
        db_table = "MasterProcurement"
        ordering = ['id']


class InlineItem(models.Model):
    procurement = models.ForeignKey(MasterProcurement, related_name='inlineitem', on_delete=models.CASCADE)
    category = models.CharField(max_length=100, null=True, blank=True)
    item = models.CharField(max_length=100, null=True, blank=True)
    costcenter = models.ForeignKey(MasterCostCenter, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    unitprice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True , default=0.00)
    totalprice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    attachment = models.ForeignKey(MasterUpload, on_delete=models.CASCADE, null=True, blank=True)
    
    objects = models.Manager()

    class Meta:
        db_table = "InlineItem"
        ordering = ['id']










    

