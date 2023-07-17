from django.contrib import admin
from mainpage.models import *
from import_export.admin import ImportExportModelAdmin
from mainpage.resource import CityResource, CountyResource, SSSResource, ContractsResource, CookiesResource


# Register your models here.

class CityAdmin(ImportExportModelAdmin):
    list_display = ['title', 'code', 'slug']
    resource_class = CityResource


class CountyAdmin(ImportExportModelAdmin):
    list_display = ['city', 'title', 'slug']
    resource_class = CountyResource

class SliderAdmin(admin.ModelAdmin):
    list_display = ['title','image_tag','is_publish', 'created_at', 'updated_at']
    readonly_fields = ('image_tag',)

class MostSearchAdmin(admin.ModelAdmin):
    list_display = ['keyword','count', 'created_at', 'updated_at']
    list_filter = ['count']

class SSSAdmin(ImportExportModelAdmin):
    list_display = ['question','answer', 'created_at']
    list_filter = ['question']
    resource_class = SSSResource


class ContractsAdmin(ImportExportModelAdmin):
    list_display = ['created_at', 'updated_at']
    resource_class = ContractsResource

admin.site.register(Setting)
admin.site.register(City, CityAdmin)
admin.site.register(County, CountyAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(MostSearchingKeyword, MostSearchAdmin)
admin.site.register(SSS, SSSAdmin)
admin.site.register(Contracts, ContractsAdmin)
