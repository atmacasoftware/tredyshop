import admin_thumbnails
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from product.resource import *
from product.models import *


class ProductApiAdmin(ImportExportModelAdmin):
    list_display = ['id', 'barcode', 'title', 'subbottomcategory',
                    'brand', 'price', 'trendyol_price', 'status',
                    'create_at', 'is_publish', 'update_at']
    search_fields = ['title', 'id', 'barcode', 'model_code']
    list_filter = ['status', 'is_discountprice']
    list_per_page = 100


class BrandAdmin(ImportExportModelAdmin):
    list_display = ['id','title', 'is_active']
    list_filter = ['is_active']
    resource_class = BrandResource


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'ip', 'status', 'created_at']


class StockAlarmAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'ip', 'is_active', 'created_at']


class ColorAdmin(ImportExportModelAdmin):
    list_display = ['name', 'code', 'color_tag']
    list_per_page = 1000
    resource_class = ColorResource


class SizeAdmin(ImportExportModelAdmin):
    list_display = ['name', 'code']
    resource_class = SizeResource

class FabricTypeAdmin(ImportExportModelAdmin):
    list_display = ['id','name']
    resource_class = FabricTypeResource

class HeightAdmin(ImportExportModelAdmin):
    list_display = ['id','name']
    resource_class = HeightResource

class PatternAdmin(ImportExportModelAdmin):
    list_display = ['id','name']
    resource_class = PatternResource

class CollerTypeAdmin(ImportExportModelAdmin):
    list_display = ['id','name']
    resource_class = CollerTypeResource

class ArmTypeAdmin(ImportExportModelAdmin):
    list_display = ['id','name']
    resource_class = ArmTypeResource


class WeavingTypeAdmin(ImportExportModelAdmin):
    list_display = ['id','name']
    resource_class = WeavingTypeResource

class MaterialTypeAdmin(ImportExportModelAdmin):
    list_display = ['id','name']
    resource_class = MaterialTypeResource

admin.site.register(Brand, BrandAdmin)
admin.site.register(LikeProduct)
admin.site.register(DisLikeProduct)
admin.site.register(Favorite)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(FabricType, FabricTypeAdmin)
admin.site.register(Height, HeightAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(CollerType, CollerTypeAdmin)
admin.site.register(ArmType, ArmTypeAdmin)
admin.site.register(WeavingType, WeavingTypeAdmin)
admin.site.register(MaterialType, MaterialTypeAdmin)
admin.site.register(StockAlarm, StockAlarmAdmin)
admin.site.register(ApiProduct, ProductApiAdmin)
