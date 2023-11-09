from import_export import resources
from trendyol.models import *

class TrendyolFirstCategoryResource(resources.ModelResource):
    class Meta:
        model = TrendyolFirstCategory

class TrendyolSecondCategoryResource(resources.ModelResource):
    class Meta:
        model = TrendyolSecondCategory

class TrendyolThirdCategoryResource(resources.ModelResource):
    class Meta:
        model = TrendyolThirdCategory

class TrendyolFourCategoryResource(resources.ModelResource):
    class Meta:
        model = TrendyolFourCategory


class TrendyolFiveCategoryResource(resources.ModelResource):
    class Meta:
        model = TrendyolFiveCategory

class TrendyolSixCategoryResource(resources.ModelResource):
    class Meta:
        model = TrendyolSixCategory


class TrendyolBrandResource(resources.ModelResource):
    class Meta:
        model = TrendyolBrand

class TrendyolOrderResource(resources.ModelResource):
    class Meta:
        model = TrendyolOrders
