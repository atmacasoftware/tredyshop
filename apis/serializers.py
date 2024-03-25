from rest_framework import serializers
from product.models import *
from categorymodel.models import *
from adminpage.models import FrontentHeaderCategory, Banner


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source='brand.title')
    category = serializers.CharField(source='category.title')
    subcategory = serializers.CharField(source='subcategory.title')


    class Meta:
        model = Product
        fields = '__all__'


class ProductModelGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'

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