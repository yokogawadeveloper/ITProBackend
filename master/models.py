from django.db import models
from django.contrib.auth import get_user_model

# User = get_user_model()

# Create your models here.
class OrgDepartment(models.Model):
    Name = models.CharField(max_length=100, unique=True)
    Head = models.CharField(max_length=100, null=True, blank=True)
    BUWallet = models.CharField(max_length=100, null=True, blank=True)
    RRProcessName = models.CharField(max_length=100, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        db_table = "OrgDepartment"
        verbose_name_plural = "OrgDepartment"


class OrgDepartmentHead(models.Model):
    OrgDepartment = models.ForeignKey(OrgDepartment, on_delete=models.CASCADE,related_name='OrgDepartmentHead')
    Head = models.CharField(max_length=100, null=True, blank=True)
    Designation = models.CharField(max_length=100, null=True, blank=True)
    OrgOffice = models.IntegerField(null=True, blank=True)

    objects = models.Manager()

    class Meta:
        db_table = "OrgDepartmentHead"
        verbose_name_plural = "OrgDepartmentHead"


class MasterCategory(models.Model):
    CategoryId = models.AutoField(primary_key=True)
    ItemCategory = models.CharField(max_length=100, unique=True)
    BoolInUse = models.BooleanField(default=True, null=True, blank=True)
    IsActive = models.BooleanField(default=True, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        db_table = "MasterCategory"
        verbose_name_plural = "MasterCategory"

    
class MasterItem(models.Model):
    ItemId = models.AutoField(primary_key=True)
    ItemName = models.CharField(max_length=100,null=True, blank=True)
    ItemCategoryId = models.ForeignKey(MasterCategory, on_delete=models.CASCADE, null=True, blank=True)
    UnitPrice = models.FloatField(null=True, blank=True)
    BoolInUse = models.BooleanField(default=True, null=True, blank=True)
    IsActive = models.BooleanField(default=True, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        db_table = "MasterItem"
        verbose_name_plural = "MasterItem"


class MasterDepartment(models.Model):
    DepartmentName = models.CharField(max_length=100, unique=True)
    DepartmentHead = models.CharField(max_length=100,null=True, blank=True)
    DepartmentAdministrator = models.CharField(max_length=100,null=True, blank=True)
    DepartmentSubAdministrator = models.CharField(max_length=100,null=True, blank=True)
    BUCode = models.CharField(max_length=100,null=True, blank=True)
    BoolInUse = models.BooleanField(default=True, null=True, blank=True)
    IsActive = models.BooleanField(default=True, null=True, blank=True)


    objects = models.Manager()

    class Meta:
        db_table = "MasterDepartment"
        verbose_name_plural = "MasterDepartment"

    
class MasterCostCenter(models.Model):
    CostCenter = models.CharField(max_length=100, unique=True)
    BUSA = models.CharField(max_length=100, null=True, blank=True)
    IsExisting = models.BooleanField(default=0, null=True, blank=True)
    IsActive = models.BooleanField(default=True, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        db_table = "MasterCostCenter"
        verbose_name_plural = "MasterCostCenter"

