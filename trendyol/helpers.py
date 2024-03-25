from django.shortcuts import get_object_or_404

from adminpage.custom import sendOrderInfoEmail
from adminpage.models import Trendyol, UpdateHistory
from product.models import ProductVariant
from trendyol.api import TrendyolApiClient
from trendyol.models import LogRecords, TrendyolProduct, TrendyolAttributes, TrendyolReport, TrendyolReportProduct
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
    product_count = ProductVariant.objects.filter(is_publish_trendyol=True).count()
    i = 0
    while i / 1000 <= round(product_count / 1000):
        products = ProductVariant.objects.filter(is_publish_trendyol=True)[i:i + 1000]
        trendyol_update_function(products=products)
        i += 1000

def trendyolProductData(barcode, title, model_code, brandid, categoryid, quantity, stock_code, desi, description,
                        list_price, sale_price, vatRate, deliveryDuration, cargoid, shipmentid, returningid, images,
                        data_attributes):
    data = {
        "barcode": str(barcode),
        "title": str(title),
        "productMainId": str(model_code),
        "brandId": int(brandid),
        "categoryId": int(categoryid),
        "quantity": int(quantity),
        "stockCode": str(stock_code),
        "dimensionalWeight": int(desi),
        "description": description,
        "currencyType": "TRY",
        "listPrice": float(list_price),
        "salePrice": float(sale_price),
        "vatRate": int(vatRate),
        "deliveryDuration": int(deliveryDuration),
        "cargoCompanyId": int(cargoid),
        "shipmentAddressId": int(shipmentid),
        "returningAddressId": int(returningid),
        "images": images,
        "attributes": data_attributes
    }

    return data

def trendyol_schedule_send_product():
    trendyol_product = TrendyolProduct.objects.filter(is_publish=False, is_ready=True)
    product_data = []
    items = []
    trendyol = Trendyol.objects.all().last()

    t_report = TrendyolReport.objects.create(name="Ürün Gönderme")

    for p in trendyol_product:
        title = p.product.title
        detail = p.product.product.detail
        if detail == '' or detail == None:
            detail = title
        images = []
        attributes = []
        if p.product.product.image_url1:
            images.append({'url': p.product.product.image_url1})
        if p.product.product.image_url2:
            images.append({'url': p.product.product.image_url2})
        if p.product.product.image_url3:
            images.append({'url': p.product.product.image_url3})
        if p.product.product.image_url4:
            images.append({'url': p.product.product.image_url4})
        if p.product.product.image_url5:
            images.append({'url': p.product.product.image_url5})
        if p.product.product.image_url6:
            images.append({'url': p.product.product.image_url6})
        if p.product.product.image_url7:
            images.append({'url': p.product.product.image_url7})
        if p.product.product.image_url8:
            images.append({'url': p.product.product.image_url8})

        for a in TrendyolAttributes.objects.filter(trendyol_product=p):
            if a.name == 'undefined' or a.value == '':
                pass
            else:
                if a.customStatus == True:
                    attributes.append({
                        "attributeId": a.code,
                        "customAttributeValue": a.value})
                else:
                    attributes.append({
                        "attributeId": a.code,
                        "attributeValueId": a.value})
        p.is_publish = True
        p.product.is_publish_trendyol = True
        p.product.save()
        p.save()
        TrendyolReportProduct.objects.create(report=t_report, product=p.product)

        items.append(
            trendyolProductData(barcode=p.product.barcode, title=title, model_code=p.product.model_code,
                                brandid=2071923,
                                categoryid=p.category_id, quantity=p.product.quantity, stock_code=p.product.stock_code,
                                desi=1,
                                list_price=p.product.trendyol_price, sale_price=p.product.trendyol_price, cargoid=10,
                                description=detail, vatRate=10, deliveryDuration=2,
                                shipmentid=trendyol.sevkiyatadresid_1,
                                returningid=trendyol.iadeadresid_1, images=images,
                                data_attributes=attributes))
        product_data = items

    if round(len(product_data) / 1000) <= 1:
        try:
            api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                                    supplier_id=trendyol.saticiid)
            service = ProductIntegrationService(api)
            response = service.create_products(items=product_data)
            log_record = LogRecords.objects.create(log_type="1", batch_id=str(response['batchRequestId']))
            return str(log_record.batch_id)
        except Exception as e:
            return 'Error'
    else:
        i = 0
        while i / 1000 <= round(len(product_data) / 1000):
            try:
                api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                                        supplier_id=trendyol.saticiid)
                service = ProductIntegrationService(api)
                response = service.create_products(items=product_data[i:i + 1000])
                log_record = LogRecords.objects.create(log_type="1", batch_id=str(response['batchRequestId']))
            except Exception as e:
                return "Error"
            i += 1000