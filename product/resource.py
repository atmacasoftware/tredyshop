from import_export import resources
from product.models import Color, Size

class ColorResource(resources.ModelResource):
    class Meta:
        model = Color

class SizeResource(resources.ModelResource):
    class Meta:
        model = Size