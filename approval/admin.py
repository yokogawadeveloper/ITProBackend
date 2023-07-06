from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ApproverMatrix)
admin.site.register(ApprovalTransaction)



@admin.register(MasterRole)
class MasterRoleAdmin(admin.ModelAdmin):
    list_display = ('roleId', 'rolename', 'isActive')



@admin.register(MasterRoleMapping)
class MasterRoleMappingAdmin(admin.ModelAdmin):
    list_display = ('id','roleId', 'employeeId', 'isActive')


admin.site.register(ModuleMaster)
admin.site.register(ModuleAccess)