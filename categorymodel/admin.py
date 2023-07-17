from django.contrib import admin
from categorymodel.models import *


# Register your models here.

class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['is_active']


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['maincategory', 'title', 'is_active']
    list_filter = ['is_active']


admin.site.register(MainCategory, MainCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
