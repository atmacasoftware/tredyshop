from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from categorymodel.models import *
from trendyol.resource import *


class TrendyolFirstCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'parentId','is_subcategory']
    search_fields = ('id', 'name', 'parentId',)
    resource_class = TrendyolFirstCategoryResource


class TrendyolSecondCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'parentId', 'is_subcategory']
    search_fields = ('id', 'name', 'parentId',)
    list_per_page = 5000
    resource_class = TrendyolSecondCategoryResource


class TrendyolThirdCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'parentId', 'is_subcategory']
    search_fields = ('id', 'name', 'parentId',)
    list_per_page = 5000
    resource_class = TrendyolThirdCategoryResource


class TrendyolFourCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'parentId', 'is_subcategory']
    search_fields = ('id', 'name', 'parentId',)
    list_per_page = 5000
    resource_class = TrendyolFourCategoryResource


class TrendyolFiveCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'parentId', 'is_subcategory']
    search_fields = ('id', 'name', 'parentId',)
    list_per_page = 5000
    resource_class = TrendyolFiveCategoryResource


class TrendyolSixCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'parentId', 'is_subcategory']
    search_fields = ('id', 'name', 'parentId',)
    list_per_page = 5000
    resource_class = TrendyolSixCategoryResource


class TrendyolBrandAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name']
    search_fields = ('id', 'name',)
    list_per_page = 5000
    resource_class = TrendyolBrandResource


class TrendyolOrderAdmin(ImportExportModelAdmin):
    list_display = ['order_number', 'packet_number','buyer','sales_amount']
    search_fields = ('order_number', 'packet_number',)
    list_per_page = 1000
    resource_class = TrendyolOrderResource

admin.site.register(TrendyolFirstCategory, TrendyolFirstCategoryAdmin)
admin.site.register(TrendyolSecondCategory, TrendyolSecondCategoryAdmin)
admin.site.register(TrendyolThirdCategory, TrendyolThirdCategoryAdmin)
admin.site.register(TrendyolFourCategory, TrendyolFourCategoryAdmin)
admin.site.register(TrendyolFiveCategory, TrendyolFiveCategoryAdmin)
admin.site.register(TrendyolSixCategory, TrendyolSixCategoryAdmin)
admin.site.register(TrendyolBrand, TrendyolBrandAdmin)
admin.site.register(LogRecords)
admin.site.register(TrendyolOrders, TrendyolOrderAdmin)

