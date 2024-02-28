from django.shortcuts import get_object_or_404

from adminpage.custom import sendOrderInfoEmail
from adminpage.models import Trendyol, UpdateHistory
from product.models import ApiProduct
from trendyol.api import TrendyolApiClient
from trendyol.models import LogRecords
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
            if p.is_trendyol_discountprice:
                saleprice = p.trendyol_discountprice
            if saleprice > trendyol.firstbarem and saleprice <= 140:
                saleprice = trendyol.firstbarem

            if saleprice > trendyol.secondbarem and saleprice <= 220:
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
            UpdateHistory.objects.create(history_type="Trendyol Stok&Fiyat G端ncelleme")
        except:
            result = 'failed'
        return result


def trendyol_schedule_update_price_stok():
    product_count = ApiProduct.objects.filter(is_publish_trendyol=True).count()
    i = 0
    while i / 1000 <= round(product_count / 1000):
        products = ApiProduct.objects.filter(is_publish_trendyol=True)[i:i + 1000]
        trendyol_update_function(products=products)
        i += 1000