from import_export import resources
from product.models import Color, Size, Brand, Product

class BrandResource(resources.ModelResource):
    class Meta:
        model = Brand

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class ColorResource(resources.ModelResource):
    class Meta:
        model = Color

class SizeResource(resources.ModelResource):
    class Meta:
        model = Size