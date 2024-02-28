from rest_framework import serializers
from product.models import *
from categorymodel.models import *
from adminpage.models import FrontentHeaderCategory, Banner


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source='brand.title')
    category = serializers.CharField(source='category.title')
    subcategory = serializers.CharField(source='subcategory.title')


    class Meta:
        model = ApiProduct
        fields = ['id', 'barcode', 'model_code', 'stock_code', 'dropshipping', 'category', 'subcategory',
                  'subbottomcategory',
                  'brand', 'title', 'description', 'image_url1', 'image_url2', 'image_url3', 'image_url4', 'image_url5',
                  'image_url6', 'image_url7', 'image_url8', 'color', 'size', 'price', 'quantity', 'detail',
                  'discountprice', 'is_discountprice', 'age_group', 'sextype', 'is_publish', 'slug']


class ProductModelGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModelGroup
        fields = ['get_product_title','kapak','get_kapak', 'get_product_slug', 'get_product_price', 'get_product_isdiscount', 'get_product_discountprice', 'third_category']

class SecondCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class ThirdCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubBottomCategory
        fields = '__all__'

class FrontendHeaderCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontentHeaderCategory
        fields = '__all__'

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'