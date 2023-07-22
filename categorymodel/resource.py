from import_export import resources
from categorymodel.models import *

class MainCategoryResource(resources.ModelResource):
    class Meta:
        model = MainCategory

class SubCategoryResource(resources.ModelResource):
    class Meta:
        model = SubCategory

class SubBottomCategoryResource(resources.ModelResource):
    class Meta:
        model = SubBottomCategory

