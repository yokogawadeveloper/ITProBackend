from django.urls import path
from .backups import *


urlpatterns = [
    path('export_user/', ExportEmployeeAPIView.as_view()),
    path('export_orgdepartment/', ExportOrgDepartmentAPIView.as_view()),
    path('export_orgdepartmenthead/', ExportOrgDepartmentHeadAPIView.as_view()),
    path('export_department/', ExportMasterDepartmentAPIView.as_view()),
    path('export_costcenter/', ExportMasterCostCenterAPIView.as_view()),
    path('export_category/', ExportMasterCategoryAPIView.as_view()),
    path('export_item/', ExportMasterItemAPIView.as_view()),

    path('import_user/', ImportUserBulkData.as_view()),
    path('import_orgdepartment/', ImportOrgDepartmentBulkData.as_view()),
    path('import_orgdepartmenthead/', ImportOrgDepartmentHeadBulkData.as_view()),
    path('import_department/', ImportDepartmentBulkData.as_view()),
    path('import_costcenter/', ImportCostCenterBulkData.as_view()),
    path('import_category/', ImportMasterCategory.as_view()),
    path('import_item/', ImportMasterItem.as_view()),
]


