from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MasterProcurement)
# admin.site.register(MoreAttachments)


@admin.register(InlineItem)
class InlineItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'procurement']
    list_filter = ['procurement']
    search_fields = ['procurement']
    # list_per_page = 20
    ordering = ['id']


@admin.register(MoreAttachments)
class MoreAttachmentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'procurement']
    list_filter = ['procurement']
    search_fields = ['procurement']
    # list_per_page = 20
    ordering = ['id']



