from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from accounting.resource import *


# Register your models here.

class ExpensesIncurredAdmin(ImportExportModelAdmin):
    list_display = ['name','company','price','status','created_at']
    resource_class = ExpensesIncurredResource

admin.site.register(ExpensesIncurred, ExpensesIncurredAdmin)