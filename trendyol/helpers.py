from adminpage.models import Trendyol, UpdateHistory
from product.models import ApiProduct
from trendyol.api import TrendyolApiClient
from trendyol.models import LogRecords, TrendyolOrders
from trendyol.services import ProductIntegrationService, OrderIntegrationService
from datetime import datetime, timezone
from math import *

def trendyolUpdateData(barcode, quantity, list_price, sale_price):
    data = {
        "barcode": str(barcode),
        "quantity": int(quantity),
        "listPrice": float(list_price),
        "salePrice": float(sale_price)
    }

    return data


def trendyol_update_function(products):
    items = []
    product_data = []
    trendyol = Trendyol.objects.all().last()
    result = 'success'

    if products.count() > 0:
        for p in products:
            listprice = p.trendyol_price
            saleprice = p.trendyol_price
            if saleprice > trendyol.firstbarem and saleprice <= 102:
                saleprice = trendyol.firstbarem

            if saleprice > trendyol.secondbarem and saleprice <= 170:
                saleprice = trendyol.secondbarem

            if p.quantity > 2:
                items.append(
                    trendyolUpdateData(barcode=p.barcode, quantity=p.quantity, list_price=listprice,
                                       sale_price=saleprice)
                )
            else:
                items.append(
                    trendyolUpdateData(barcode=p.barcode, quantity=0, list_price=listprice,
                                       sale_price=saleprice)
                )

            product_data = items
        try:
            api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                                    supplier_id=trendyol.saticiid)
            service = ProductIntegrationService(api)
            response = service.update_price_and_stock(items=product_data)
            log_record = LogRecords.objects.create(log_type="2", batch_id=response['batchRequestId'])
            UpdateHistory.objects.create(history_type="Trendyol Stok&Fiyat Güncelleme")
        except:
            result = 'failed'
        return result


def trendyol_schedule_update_price_stok():
    total_product = ApiProduct.objects.all().filter(is_publish_trendyol=True).count()
    result = ceil(total_product / 999)
    i = 0

    while i < result:
        if i == 0:
            j = 0
            products = ApiProduct.objects.filter(is_publish_trendyol=True)[j:999]
            trendyol_update_function(products=products)
        else:
            j = i * 1000
            products = ApiProduct.objects.filter(is_publish_trendyol=True)[j - 1:j + 999]
            trendyol_update_function(products=products)
        i = i + 1

def get_cron_trendyol_orders():
    context = {}
    trendyol = Trendyol.objects.all().last()
    trendyol_orders = TrendyolOrders.objects.all()
    filter_params = None
    quantity = 0
    title = ''
    barcode = ''
    color = '-'
    size = '-'
    unitPrice = 0.0
    salesAmount = 0.0
    discount = 0.0
    sku = ''

    api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                            supplier_id=trendyol.saticiid)
    service = OrderIntegrationService(api)
    response = service.get_shipment_packages(filter_params=filter_params)
    status = None
    for r in response['content']:
        customerName = r['customerFirstName'] + ' ' + r['customerLastName']
        orderNumber = r['orderNumber']
        packetNumber = r['id']
        orderDate = r['orderDate']
        datetime_obj_with_tz = datetime.utcfromtimestamp(orderDate / 1000)

        if TrendyolOrders.objects.filter(packet_number__contains=str(packetNumber)).count() > 0:
            order = TrendyolOrders.objects.get(packet_number=str(packetNumber))
            if len(r['lines']) == 1:
                for l in r['lines']:
                    orderStatus = l['orderLineItemStatusName']
                    if orderStatus == 'UnDeliveredAndReturned':
                        status = "İade Edildi"
                    elif orderStatus == 'Picking':
                        status = "Hazırlanıyor"
                    elif orderStatus == "Deliverd":
                        status = "Tamamlandı"
                    elif orderStatus == "Cancelled":
                        status = "İptal Edildi"
                    elif orderStatus == "Created":
                        status = "Yeni"
                    elif orderStatus == "Shipped":
                        status = "Taşıma Durumunda"
                    else:
                        status = "Taşıma Durumunda"
                order.status = status
                order.save()
        else:
            if len(r['lines']) == 1:
                for l in r['lines']:
                    quantity = l['quantity']
                    size = l['productSize']
                    sku = l['merchantSku']
                    title = l['productName']
                    barcode = l['barcode']
                    kdv = l['vatBaseAmount']
                    orderStatus = l['orderLineItemStatusName']
                    if orderStatus == 'UnDeliveredAndReturned':
                        status = "İade Edildi"
                    elif orderStatus == 'Picking':
                        status = "Hazırlanıyor"
                    elif orderStatus == "Deliverd":
                        status = "Tamamlandı"
                    elif orderStatus == "Cancelled":
                        status = "İptal Edildi"
                    elif orderStatus == "Created":
                        status = "Yeni"
                    elif orderStatus == "Shipped":
                        status = "Taşıma Durumunda"
                    else:
                        status = "Taşıma Durumunda"
                    discount = l['discount']
                    unitPrice = l['price']
                    salesAmount = l['amount']
                    TrendyolOrders.objects.create(order_number=orderNumber, packet_number=packetNumber,
                                                  buyer=customerName, quantity=quantity, title=title,
                                                  barcode=barcode, color=color, size=size, stock_code=sku,
                                                  unit_price=unitPrice, sales_amount=salesAmount,
                                                  discount_amount=discount, status=status,
                                                  order_date=datetime_obj_with_tz)