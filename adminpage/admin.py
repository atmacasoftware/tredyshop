from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from adminpage.resource import *
from adminpage.models import *


# Register your models here.


class TrendyolAdmin(ImportExportModelAdmin):
    list_display = ['id']
    resource_class = TrendyolResource

class IssuedInvoicesAdmin(ImportExportModelAdmin):
    list_display = ['id']
    resource_class = IssuedInvoicesResource


class InvoicesReceivedAdmin(ImportExportModelAdmin):
    list_display = ['id']
    resource_class = InvoicesReceived


class HakkimizdaAdmin(ImportExportModelAdmin):
    list_display = ['id']
    resource_class = Hakkimizda

admin.site.register(Trendyol, TrendyolAdmin)
admin.site.register(IssuedInvoices, IssuedInvoicesAdmin)
admin.site.register(InvoicesReceived, InvoicesReceivedAdmin)
admin.site.register(Hakkimizda, InvoicesReceivedAdmin)

