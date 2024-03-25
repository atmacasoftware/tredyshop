from django.shortcuts import get_object_or_404
from user_accounts.models import User
from adminpage.custom import productStatistic, sendOrderInfoEmail
from adminpage.models import Trendyol, Notification
from product.models import ProductVariant
from trendyol.api import TrendyolApiClient
from trendyol.models import TrendyolOrders, TrendyolMoreProductOrder, TrendyolCommission
from trendyol.services import OrderIntegrationService
from datetime import datetime

def get_trendyol_orders():
    trendyol = Trendyol.objects.all().last()
    trendyol_orders = TrendyolOrders.objects.all()
    filter_params = None
    color = '-'
    komisyon_tutari = 0

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
                order.shippment_city = r['shipmentAddress']['city']
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
                        order.commission_price = 0.0
                        order.delivery_price = 0.0
                        order.service_price = 3.59
                    elif orderStatus == "Created" or orderStatus == "ReadyToShip":
                        status = "Yeni"
                    elif orderStatus == "Shipped":
                        status = "Kargolandı"
                    else:
                        status = "Kargolandı"

                order.status = status
                order.save()
            elif len(r['lines']) > 1:
                order.shippment_city = r['shipmentAddress']['city']
                for l in r['lines']:
                    for product in TrendyolMoreProductOrder.objects.filter(order_number=orderNumber,
                                                                           packet_number=packetNumber):
                        orderStatus = l['orderLineItemStatusName']
                        if orderStatus == 'UnDeliveredAndReturned':
                            status = "İade Edildi"
                        elif orderStatus == 'Picking':
                            status = "Hazırlanıyor"
                        elif orderStatus == "Deliverd":
                            status = "Tamamlandı"
                        elif orderStatus == "Cancelled":
                            status = "İptal Edildi"
                            order.commission_price = 0.0
                            order.delivery_price = 0.0
                            order.service_price = 3.59
                        elif orderStatus == "Created" or orderStatus == "ReadyToShip":
                            status = "Yeni"
                        elif orderStatus == "Shipped":
                            status = "Kargolandı"
                        else:
                            status = "Kargolandı"
                        product.status = status
                        product.save()
                order.save()
        else:
            if len(r['lines']) == 1:
                for l in r['lines']:
                    quantity = l['quantity']
                    size = l['productSize']
                    sku = l['merchantSku']
                    title = l['productName']
                    barcode = l['barcode']
                    try:
                        seller_product = get_object_or_404(ProductVariant, barcode=str(l['barcode']))
                        if seller_product.product.subcategory == "Üst Giyim":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Üst Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.product.subcategory == "Alt Giyim":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Alt Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.product.subcategory == "Dış Giyim":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Dış Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.product.subcategory == "İç Giyim":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="İç Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.product.subcategory == "Ayakkabı":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Ayakkabı").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.product.subcategory == "Aksesuar":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Çanta").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        else:
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Alt Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                    except:
                        komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Alt Giyim").komisyon_tutari
                        komisyon_tutari = l['amount'] * komisyon_orani / 100

                    orderStatus = l['orderLineItemStatusName']
                    if orderStatus == 'UnDeliveredAndReturned':
                        status = "İade Edildi"
                    elif orderStatus == 'Picking':
                        status = "Hazırlanıyor"
                    elif orderStatus == "Deliverd":
                        status = "Tamamlandı"
                    elif orderStatus == "Cancelled":
                        status = "İptal Edildi"
                    elif orderStatus == "Created" or orderStatus == "ReadyToShip":
                        status = "Yeni"
                    elif orderStatus == "Shipped":
                        status = "Kargolandı"
                    else:
                        status = "Kargolandı"
                    discount = l['discount']
                    unitPrice = l['amount']
                    salesAmount = l['price']
                    try:
                        color = l['productColor']
                    except:
                        color = None
                    data = TrendyolOrders.objects.create(order_number=orderNumber, packet_number=packetNumber,
                                                         buyer=customerName, quantity=quantity, title=title,
                                                         barcode=barcode, color=color, size=size,
                                                         stock_code=sku,
                                                         unit_price=unitPrice, sales_amount=salesAmount,
                                                         discount_amount=discount, status=status,
                                                         shippment_city=r['shipmentAddress']['city'],
                                                         order_date=datetime_obj_with_tz,
                                                         commission_price=komisyon_tutari,
                                                         service_price=trendyol.hizmet_bedeli)

                    productStatistic(barcode=barcode, title=title, quantity=quantity,
                                     satis=salesAmount)
                    for user in User.objects.filter(is_superuser=True):
                        Notification.objects.create(noti_type="4", title="Yeni Trendyol siparişi alındı.", trendyol_orders=data, user=user)
                    sendOrderInfoEmail(platform="Trendyol", email="atmacaahmet5261@hotmail.com", order=data)
            elif len(r['lines']) > 1:
                for l in r['lines']:
                    quantity = l['quantity']
                    size = l['productSize']
                    sku = l['merchantSku']
                    title = l['productName']
                    barcode = l['barcode']
                    try:
                        seller_product = get_object_or_404(ProductVariant, barcode=str(l['barcode']))
                        if seller_product.product.subcategory == "Üst Giyim":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Üst Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.product.subcategory == "Alt Giyim":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Alt Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.product.subcategory == "Dış Giyim":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Dış Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.product.subcategory == "İç Giyim":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="İç Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.product.subcategory == "Ayakkabı":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Ayakkabı").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.product.subcategory == "Aksesuar":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Çanta").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        else:
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Alt Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                    except:
                        komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Alt Giyim").komisyon_tutari
                        komisyon_tutari = l['amount'] * komisyon_orani / 100

                    orderStatus = l['orderLineItemStatusName']
                    if orderStatus == 'UnDeliveredAndReturned':
                        status = "İade Edildi"
                    elif orderStatus == 'Picking':
                        status = "Hazırlanıyor"
                    elif orderStatus == "Deliverd":
                        status = "Tamamlandı"
                    elif orderStatus == "Cancelled":
                        status = "İptal Edildi"
                    elif orderStatus == "Created" or orderStatus == "ReadyToShip":
                        status = "Yeni"
                    elif orderStatus == "Shipped":
                        status = "Kargolandı"
                    else:
                        status = "Kargolandı"
                    discount = l['discount']
                    unitPrice = l['amount']
                    salesAmount = l['price']
                    try:
                        color = l['productColor']
                    except:
                        color = None
                    TrendyolMoreProductOrder.objects.create(order_number=orderNumber, barcode=barcode, title=title,
                                                            packet_number=packetNumber, color=color,
                                                            quantity=quantity, size=size, stock_code=sku,
                                                            unit_price=unitPrice, sales_amount=salesAmount,
                                                            discount_amount=discount, status=status)
                    productStatistic(barcode=barcode, title=title, quantity=quantity,
                                     satis=salesAmount)
                birim_fiyat = 0
                satis_fiyat = 0
                indirim = 0
                miktar = 0
                for product in TrendyolMoreProductOrder.objects.filter(order_number=orderNumber,
                                                                       packet_number=packetNumber):
                    birim_fiyat += product.unit_price
                    satis_fiyat += product.sales_amount
                    indirim += product.discount_amount
                    miktar += product.quantity

                data = TrendyolOrders.objects.create(order_number=orderNumber, packet_number=packetNumber,
                                                     buyer=customerName, quantity=miktar, title="Birden Fazla Ürün",
                                                     barcode="Birden Fazla Barkod", color="Birden Fazla Ürün",
                                                     size="Birden Fazla Ürün", stock_code="Birden Fazla STK",
                                                     unit_price=birim_fiyat, sales_amount=satis_fiyat,
                                                     discount_amount=indirim, status="Birden Fazla",
                                                     shippment_city=r['shipmentAddress']['city'],
                                                     order_date=datetime_obj_with_tz, commission_price=komisyon_tutari,
                                                     service_price=trendyol.hizmet_bedeli)
                for user in User.objects.filter(is_superuser=True):
                        Notification.objects.create(noti_type="4", title="Yeni Trendyol siparişi alındı.", trendyol_orders=data, user=user)
                sendOrderInfoEmail(platform="Trendyol", email="atmacaahmet5261@hotmail.com", order=data)
