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
    CHOICES = (('BuHead', 'BuHead'), ('DSINHead', 'DSINHead'), ('FinanceHead', 'FinanceHead'), ('MD', 'MD'),
               ('DSINMPR', 'DSINMPR'))
    TYPE = (('Approved', 'Approved'), ('Modification', 'Modification'), ('Reject', 'Reject'))
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


class MasterRole(models.Model):
    roleId = models.AutoField(primary_key=True)
    rolename = models.CharField(max_length=100, null=True, blank=True)
    isActive = models.BooleanField(default=True, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = "MasterRole"
        verbose_name_plural = "MasterRole"


class MasterRoleMapping(models.Model):
    roleId = models.ForeignKey(MasterRole, null=True, blank=True, on_delete=models.CASCADE)
    employeeId = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, null=True, blank=True)
    isActive = models.BooleanField(default=True, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = "MasterRoleMapping"
        verbose_name_plural = "MasterRoleMapping"


class ModuleMaster(models.Model):
    moduleId = models.AutoField(primary_key=True, unique=True)
    module_name = models.CharField(max_length=100, null=True)
    module_slug = models.SlugField(max_length=100, null=True)
    root = models.CharField(max_length=100, null=True)
    m_color = models.CharField(max_length=100, null=True)
    m_icon_name = models.CharField(max_length=100, null=True)
    m_link = models.CharField(max_length=100, null=True)
    menu_flag = models.BooleanField(default=True)
    sort_no = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = "ModuleMaster"
        verbose_name_plural = "ModuleMaster"


class ModuleAccess(models.Model):
    moduleAccessId = models.AutoField(primary_key=True, unique=True)
    moduleId = models.ForeignKey(ModuleMaster, null=True, blank=True, on_delete=models.CASCADE)
    is_approver = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_dsin = models.BooleanField(default=False)
    is_requester = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)


    objects = models.Manager()

    class Meta:
        db_table = "ModuleAccess"
        verbose_name_plural = "ModuleAccess"
        