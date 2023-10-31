from import_export import resources
from product.models import *

class BrandResource(resources.ModelResource):
    class Meta:
        model = Brand

class ColorResource(resources.ModelResource):
    class Meta:
        model = Color

class SizeResource(resources.ModelResource):
    class Meta:
        model = Size

class FabricTypeResource(resources.ModelResource):
    class Meta:
        model = FabricType

class HeightResource(resources.ModelResource):
    class Meta:
        model = Height

class PatternResource(resources.ModelResource):
    class Meta:
        model = Pattern


class ArmTypeResource(resources.ModelResource):
    class Meta:
        model = ArmType

class CollerTypeResource(resources.ModelResource):
    class Meta:
        model = CollerType

class WeavingTypeResource(resources.ModelResource):
    class Meta:
        model = WeavingType


class MaterialTypeResource(resources.ModelResource):
    class Meta:
        model = MaterialType


class EnvironmentTypeResource(resources.ModelResource):
    class Meta:
        model = EnvironmentType


class WaistResource(resources.ModelResource):
    class Meta:
        model = Waist


class LegTypeResource(resources.ModelResource):
    class Meta:
        model = LegType


class PocketResource(resources.ModelResource):
    class Meta:
        model = Pocket