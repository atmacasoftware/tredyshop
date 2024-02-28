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
    list_per_page = 5000


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


class EnvironmentTypeAdmin(ImportExportModelAdmin):
    list_display = ['id','name']
    resource_class = EnvironmentTypeResource

class WaistAdmin(ImportExportModelAdmin):
    list_display = ['id','name']
    resource_class = WaistResource

class LegTypeAdmin(ImportExportModelAdmin):
    list_display = ['id','name']
    resource_class = LegTypeResource

class PocketAdmin(ImportExportModelAdmin):
    list_display = ['id','name']
    resource_class = PocketResource

class HeelTypeAdmin(ImportExportModelAdmin):
    list_display = ['id','name']
    resource_class = HeelTypeResource

class HeelSizeAdmin(ImportExportModelAdmin):
    list_display = ['id','name']
    resource_class = HeelSizeResource

class SexAdmin(ImportExportModelAdmin):
    list_display = ['id','name']
    resource_class = SexResource

class KadinUstBedenAdmin(ImportExportModelAdmin):
    list_display = ['beden_adi','boyun','gogus','bel']
    resource_class = KadinUstBedenResource

class KadinUstBuyukAdmin(ImportExportModelAdmin):
    list_display = ['beden_adi','boyun','gogus','bel']
    resource_class = KadinUstBuyukBedenResource

class KadinAltBedenAdmin(ImportExportModelAdmin):
    list_display = ['beden_adi','basen','bel']
    resource_class = KadinAltBedenResource

class KadinAltBuyukBedenAdmin(ImportExportModelAdmin):
    list_display = ['beden_adi','basen','bel']
    resource_class = KadinAltBuyukBedenResource

class KadinJeanBedenAdmin(ImportExportModelAdmin):
    list_display = ['beden_adi','basen','bel']
    resource_class = KadinJeanBedenResource

class ProductGroupAdmin(ImportExportModelAdmin):
    list_display = ['model_code','product']
    search_fields = ['model_code']
    list_per_page = 1000
    resource_class = ProductGroupResource

class TabletModelAdmin(ImportExportModelAdmin):
    list_display = ['name']
    resource_class = TabletModelResource

class TableCaseTypeAdmin(ImportExportModelAdmin):
    list_display = ['name']
    resource_class = TableCaseTypeResource

class SleepModeAdmin(ImportExportModelAdmin):
    list_display = ['name']
    resource_class = SleepModeResource

class BagPatternAdmin(ImportExportModelAdmin):
    list_display = ['name']
    resource_class = BagPatternResource

class BijuteriThemeAdmin(ImportExportModelAdmin):
    list_display = ['name']
    resource_class = BijuteriThemeResource


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
admin.site.register(EnvironmentType, EnvironmentTypeAdmin)
admin.site.register(Waist, WaistAdmin)
admin.site.register(LegType, LegTypeAdmin)
admin.site.register(Pocket, PocketAdmin)
admin.site.register(HeelType, HeelTypeAdmin)
admin.site.register(HeelSize, HeelSizeAdmin)
admin.site.register(Sex, SexAdmin)
admin.site.register(KadinUstBedenTablosu, KadinUstBedenAdmin)
admin.site.register(KadinUstBuyukBedenTablosu, KadinUstBuyukAdmin)
admin.site.register(KadinAltBedenTablosu, KadinAltBedenAdmin)
admin.site.register(KadinAltBuyukBedenTablosu, KadinAltBuyukBedenAdmin)
admin.site.register(KadinJeanBedenTablosu, KadinJeanBedenAdmin)
admin.site.register(ProductKapak)
admin.site.register(ProductModelGroup, ProductGroupAdmin)
admin.site.register(TabletModel, TabletModelAdmin)
admin.site.register(TableCaseType, TableCaseTypeAdmin)
admin.site.register(SleepMode, SleepModeAdmin)
admin.site.register(BagPattern, BagPatternAdmin)
admin.site.register(BijuteriTheme, BijuteriThemeAdmin)
