from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MasterDepartment)
admin.site.register(MasterCategory)
admin.site.register(MasterItem)
admin.site.register(MasterCostCenter)

