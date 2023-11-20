from import_export import resources
from trendyol.models import *

class LogRecordsResource(resources.ModelResource):
    class Meta:
        model = LogRecords

class TrendyolOrderResource(resources.ModelResource):
    class Meta:
        model = TrendyolOrders


class TrendyolCommissionResource(resources.ModelResource):
    class Meta:
        model = TrendyolCommission