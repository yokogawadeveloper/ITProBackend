from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from master.models import OrgDepartment


# Create your models here.
class EmployeeUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Username must be set as EmployeeNo')

        if not email:
            raise ValueError('email must be set')

        if not password:
            password = 'Yokogawa@12345'

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(username, email, password, **extra_fields)


class EmployeeUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)  # It is EmployeeNo
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    OrgDepartmentId = models.ForeignKey(OrgDepartment, on_delete=models.CASCADE, null=True, blank=True)
    # other fields
    GlobalEmpNo = models.CharField(max_length=100, null=True, blank=True)
    YGSAccountCode = models.CharField(max_length=100, null=True, blank=True)
    DomainId = models.CharField(max_length=100, null=True, blank=True)
    YGSCostCenter = models.CharField(max_length=100, null=True, blank=True)
    CostCenter = models.CharField(max_length=100, null=True, blank=True)
    Sex = models.CharField(max_length=100, null=True, blank=True)
    DOB = models.DateTimeField(null=True, blank=True)
    BoolContract = models.BooleanField(default=False)
    DOJ = models.DateField(null=True, blank=True)
    DepartmentId = models.IntegerField(null=True, blank=True)
    GroupId = models.IntegerField(null=True, blank=True)
    DeptCode = models.CharField(max_length=100, null=True, blank=True)
    Grade = models.CharField(max_length=100, null=True, blank=True)
    Designation = models.CharField(max_length=100, null=True, blank=True)
    FunctionalRoleId = models.IntegerField(null=True, blank=True, default=0)
    OldEmail = models.EmailField(max_length=100, null=True, blank=True)
    HODEmpNo = models.CharField(max_length=100, null=True, blank=True)
    BoolHOD = models.BooleanField(default=False, null=True, blank=True)
    MobileNo = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = EmployeeUserManager()

    class Meta:
        db_table = 'EmployeeUser'
        managed = True
        verbose_name = 'EmployeeUser'
        ordering = ['id']


class MasterRole(models.Model):
    roleId = models.AutoField(primary_key=True)
    rolename = models.CharField(max_length=100, null=True, blank=True)
    isActive = models.BooleanField(default=True, null=True, blank=True)
    created_by = models.ForeignKey(EmployeeUser, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(EmployeeUser, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = "MasterRole"
        verbose_name_plural = "MasterRole"


class MasterRoleMapping(models.Model):
    roleId = models.ForeignKey(MasterRole, null=True, blank=True, on_delete=models.CASCADE)
    employeeId = models.ForeignKey(EmployeeUser, null=True, blank=True, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True, null=True, blank=True)
    created_by = models.ForeignKey(EmployeeUser, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(EmployeeUser, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = "MasterRoleMapping"
        verbose_name_plural = "MasterRoleMapping"