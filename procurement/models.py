from django.contrib.auth import get_user_model
from django.db import models
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
    CHOICES1 = (('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Cancelled', 'Cancelled'))
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
    Status = models.CharField(max_length=100, choices=CHOICES1, null=True, blank=True, default='Pending')
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
            from approval.models import AppTransaction ,ApproverMatrix
            appmat = ApproverMatrix.objects.filter(request_type=self.RequestType).order_by('sequence')
            for app in appmat:
                if app.sequence == 1:
                    userOrgDept = User.objects.get(id=self.Created_by.id).OrgDepartmentId
                    userOrgDeptHead = OrgDepartmentHead.objects.filter(OrgDepartment_id=userOrgDept).first()
                    userOrgDeptHeadEmail = User.objects.get(username=userOrgDeptHead.Head).email
                    approverEmail = userOrgDeptHeadEmail
                elif app.sequence == 2:
                    approverEmail = 'Jiya.K@yokogawa.com'
                elif app.sequence == 3:
                    approverEmail = 'ganeshchandra.p@yokogawa.com'
                elif app.sequence == 4:
                    approverEmail = 'sajiv.nath@yokogawa.com'
                elif app.sequence == 5:
                    approverEmail = 'Lingarajan.R@Yokogawa.com'
                else:
                    approverEmail = ''
                AppTransaction.objects.create(procurementId=self, sequence=app.sequence, approverEmail=approverEmail, status='Pending', create_by=self.Created_by, update_by=self.Updated_by)

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










    

