from import_export import resources
from mainpage.models import City, County, SSS, Contracts, Cookies

class CityResource(resources.ModelResource):
    class Meta:
        model = City

class CountyResource(resources.ModelResource):
    class Meta:
        model = County

class SSSResource(resources.ModelResource):
    class Meta:
        model = SSS

class ContractsResource(resources.ModelResource):
    class Meta:
        model = Contracts

class CookiesResource(resources.ModelResource):
    class Meta:
        model = Cookies