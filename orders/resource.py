from import_export import resources
from orders.models import Order, OrderProduct


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order


class OrderProductResource(resources.ModelResource):
    class Meta:
        model = OrderProduct