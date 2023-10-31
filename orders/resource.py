from import_export import resources
from orders.models import Order, OrderProduct, BankInfo, BINList


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order


class OrderProductResource(resources.ModelResource):
    class Meta:
        model = OrderProduct

class BankInfoResource(resources.ModelResource):
    class Meta:
        model = BankInfo

class BINListResource(resources.ModelResource):
    class Meta:
        model = BINList