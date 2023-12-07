from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from categorymodel.models import *
from trendyol.resource import *

class LogRecordAdmin(ImportExportModelAdmin):
    list_display = ['log_type', 'batch_id']
    search_fields = ('log_type',)
    list_per_page = 100
    resource_class = LogRecordsResource

class TrendyolOrderAdmin(ImportExportModelAdmin):
    list_display = ['order_number', 'packet_number','buyer','sales_amount']
    search_fields = ('order_number', 'packet_number',)
    list_per_page = 100
    resource_class = TrendyolOrderResource


class TrendyolCommissionAdmin(ImportExportModelAdmin):
    list_display = ['kategori_adi', 'komisyon_tutari','update_at']
    search_fields = ('kategori_adi',)
    list_per_page = 100
    resource_class = TrendyolCommissionResource


admin.site.register(LogRecords, LogRecordAdmin)
admin.site.register(TrendyolOrders, TrendyolOrderAdmin)
admin.site.register(TrendyolCommission, TrendyolCommissionAdmin)
admin.site.register(TrendyolMoreProductOrder)

