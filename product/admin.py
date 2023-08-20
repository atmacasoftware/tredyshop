import admin_thumbnails
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from product.resource import *
from product.models import *


# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1


class ProductDescriptionInline(admin.TabularInline):
    model = DescriptionList
    extra = 1


class ProductSpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1


class ProductKeywordInline(admin.TabularInline):
    model = ProductKeywords
    extra = 1


class ReviewImageInline(admin.TabularInline):
    model = ReviewRatingImages
    extra = 1


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'sku', 'color', 'size', 'price', 'trendyol_price', 'hepsiburada_price',
                    'pttavm_price', 'is_discountprice', 'discountprice', 'quantity']


class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True


@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'title', 'image_thumbnail']


class ProductAdmin(ImportExportModelAdmin):
    list_display = ['id', 'xml_id', 'stock_code', 'barcode', 'title', 'category', 'subcategory', 'subbottomcategory',
                    'brand', 'price', 'trendyol_price', 'hepsiburada_price', 'pttavm_price', 'amount', 'status',
                    'create_at']

    list_filter = ['status']
    inlines = [ProductImageInline, ProductVariantsInline, ProductDescriptionInline, ProductSpecificationInline,
               ProductKeywordInline]
    list_per_page = 5000
    search_fields = ['title', 'id', 'xml_id', 'stock_code', 'barcode']
    resource_class = ProductResource


class BrandAdmin(ImportExportModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['is_active']
    resource_class = BrandResource


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    inlines = [ReviewImageInline]


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


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(LikeProduct)
admin.site.register(DisLikeProduct)
admin.site.register(Favorite)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(StockAlarm, StockAlarmAdmin)
admin.site.register(Variants, VariantsAdmin)
