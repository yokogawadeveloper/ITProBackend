from django.contrib import admin
from .models import *
# Register your models here.

class EmployeeUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')



admin.site.register(EmployeeUser, EmployeeUserAdmin)


@admin.register(MasterRole)
class MasterRoleAdmin(admin.ModelAdmin):
    list_display = ('roleId', 'rolename', 'isActive')



@admin.register(MasterRoleMapping)
class MasterRoleMappingAdmin(admin.ModelAdmin):
    list_display = ('id','roleId', 'employeeId', 'isActive')




