from import_export import resources
from mainpage.models import City, County, SSS

class CityResource(resources.ModelResource):
    class Meta:
        model = City

class CountyResource(resources.ModelResource):
    class Meta:
        model = County

class SSSResource(resources.ModelResource):
    class Meta:
        model = SSS