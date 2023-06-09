from django.contrib import admin
from .models import EmployeeUser
# Register your models here.

class EmployeeUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

admin.site.register(EmployeeUser, EmployeeUserAdmin)


