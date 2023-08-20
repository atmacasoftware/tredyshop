from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from orders.models import *
from orders.resource import *


# Register your models here.

class OrderAdmin(ImportExportModelAdmin):
    list_display = ['order_number', 'cardholder', 'status', 'paymenttype', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered', 'paymenttype']
    search_fields = ['order_number', 'cardholder', 'paymenttype']
    resource_class = OrderResource


class OrderProductAdmin(ImportExportModelAdmin):
    list_display = ['order', 'user', 'product', 'variation', 'color', 'size', 'quantity', 'product_price', 'ordered',
                    'created_at']
    list_filter = ['ordered']
    resource_class = OrderProductResource


class BankInfoAdmin(ImportExportModelAdmin):
    list_display = ['name', 'branch', 'iban', 'account_no', 'account_holder', 'created_at', 'updated_at']
    list_filter = ['name']
    search_fields = ('name', 'iban', 'account_no',)
    resource_class = BankInfoResource


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(BankInfo, BankInfoAdmin)
