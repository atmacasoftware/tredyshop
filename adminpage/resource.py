from import_export import resources
from adminpage.models import *

class TrendyolResource(resources.ModelResource):
    class Meta:
        model = Trendyol


class IssuedInvoicesResource(resources.ModelResource):
    class Meta:
        model = IssuedInvoices


class InvoicesReceivedResource(resources.ModelResource):
    class Meta:
        model = InvoicesReceived

class HakkimizdaResource(resources.ModelResource):
    class Meta:
        model = Hakkimizda

class HarcamalarResource(resources.ModelResource):
    class Meta:
        model = Harcamalar