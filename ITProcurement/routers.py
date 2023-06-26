from rest_framework import routers
from master.views import *
from procurement.views import *
from approval.views import *



router = routers.DefaultRouter()

#-------------------------------------Master-------------------------------------#
router.register(r'mastercategory', MasterCategoryViewSet, basename='mastercategory')
router.register(r'masteritem', MasterItemViewSet, basename='masteritem')
router.register(r'masterdepartment', MasterDepartmentViewSet, basename='masterdepartment')
router.register(r'mastercostcenter', MasterCostCenterViewSet, basename='mastercostcenter')

#-------------------------------------Procurement-------------------------------------#
router.register(r'masterprocurement', MasterProcurementViewSet, basename='masterprocurement')
# router.register(r'masterprocurementitem', MasterProcurementDetailViewSet, basename='masterprocurementitem')

#-------------------------------------Approval-------------------------------------#
router.register(r'uploadfile', UploadFileViewSet, basename='uploadfile')