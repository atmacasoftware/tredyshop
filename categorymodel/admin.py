from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from categorymodel.models import *
from categorymodel.resource import *


# Register your models here.

class MainCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'order', 'title', 'category_no', 'is_active']
    list_filter = ['is_active']
    resource_class = MainCategoryResource


class SubCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'maincategory', 'title', 'category_no', 'is_active']
    list_filter = ['is_active']
    resource_class = SubCategoryResource


class SubBottomCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'maincategory', 'subcategory', 'title', 'is_active']
    list_filter = ['is_active']
    resource_class = SubBottomCategoryResource





admin.site.register(MainCategory, MainCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(SubBottomCategory, SubBottomCategoryAdmin)
