from io import BytesIO
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
import xlwt
from datetime import timedelta, datetime, date
import requests
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.template.loader import get_template, render_to_string
from django.utils.http import urlsafe_base64_encode
from xhtml2pdf import pisa
from django.contrib.auth.tokens import default_token_generator
from adminpage.models import Notification, Izinler, ProductSellStatistic, Trendyol
from categorymodel.models import SubBottomCategory
from ecommerce import settings
from ecommerce.settings import EMAIL_HOST_USER
from product.models import ApiProduct
from user_accounts.models import User
from django.utils.html import strip_tags
from trendyol.api import TrendyolApiClient
from trendyol.models import LogRecords, TrendyolMoreProductOrder
from trendyol.services import ProductIntegrationService, OrderIntegrationService


def exportExcel(filename, sheetname, columns, rows):
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = f'attachment; filename={filename}-' + str(datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(f'{sheetname}')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = columns
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = rows
    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response


def exportPdf(template_name, context_dict={}):
    template = get_template(template_name)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def notReadNotification():
    notify = Notification.objects.filter(is_read=False).count()
    return notify


def readNotification():
    notify = Notification.objects.filter(is_read=False)
    return notify


def createNotification(type, title, detail):
    notify = Notification.objects.create(noti_type=type, title=title, detail=detail)
    notify.save()
    response = 'Create Notify'
    return response


def izinSor(user_id):
    user = User.objects.get(id=user_id)
    izin = Izinler.objects.filter(user=user).last()
    return izin


def sendAccountVerificationEmail(request, first_name, last_name, email, otp):
    try:

        my_subject = "Lütfen hesabınızı doğrulayınız."
        my_recipient = email

        current_site = get_current_site(request)

        html_message = render_to_string("backend/email/account_verification_email.html", {
            'first_name': first_name,
            'last_name':last_name,
            'domain': current_site,
            'otp':otp
        })

        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject=my_subject,
            body=plain_message,
            from_email=EMAIL_HOST_USER,
            to=[my_recipient]
        )

        message.attach_alternative(html_message, "text/html")
        message.send()

        msg = 'success'
        return msg
    except:
        msg = 'failed'
        return msg


def sendOrderInfoEmail(platform, email, order):
    try:
        my_subject = "Yeni bir sipariş var!"
        my_recipient = email

        if platform == "Trendyol":
            html_message = render_to_string("backend/email/order.html", {
                'siparis_no':order.order_number,
                'quantity': order.quantity,
                'title': order.title,
                'unit_price': order.unit_price,
                'sales_amount': order.sales_amount,
                'order_date': order.order_date,
                'siparis_id': order.id,
            })
            plain_message = strip_tags(html_message)

            message = EmailMultiAlternatives(
                subject=my_subject,
                body=plain_message,
                from_email=EMAIL_HOST_USER,
                to=[my_recipient]
            )

            message.attach_alternative(html_message, "text/html")
            message.send()
        elif platform == "TredyShop":
            html_message = render_to_string("backend/email/order.html", {
                'siparis_no':order.order_number,
                'sales_amount': order.order_total,
                'order_date': order.created_at
            })
            plain_message = strip_tags(html_message)

            message = EmailMultiAlternatives(
                subject=my_subject,
                body=plain_message,
                from_email=EMAIL_HOST_USER,
                to=[my_recipient]
            )

            message.attach_alternative(html_message, "text/html")
            message.send()
        msg = 'success'
        return msg
    except:
        msg = 'failed'
        return msg


def customerTredyShopCreateOrder(request, email, address, order_list, order, total, grand_total):
    my_subject = "Yeni bir sipariş var!"
    my_recipient = email

    if order.delivery_price == 0:
        delivery_price = "Ücretsiz"
    else:
        delivery_price = order.delivery_price

    vade_farki = order.order_total - order.order_amount

    html_message = render_to_string("backend/email/customer_order.html", {
        'siparis_no': order.order_number,
        'order_list': order_list,
        'sales_amount': order.order_total,
        'order_date': order.created_at,
        'address': address,
        'order_list_count': len(order_list),
        'total': total,
        'grand_total': grand_total,
        'delivery_price': delivery_price,
        'vade_farki': vade_farki,
    })
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject=my_subject,
        body=plain_message,
        from_email=EMAIL_HOST_USER,
        to=[my_recipient]
    )

    message.attach_alternative(html_message, "text/html")
    message.send()

    msg = 'success'
    return msg


def customerTredyShopDeliveryOrder(request, email, address, order_list, order, total, grand_total):
    my_subject = "Siparişin Kargolandı"
    my_recipient = email

    if order.delivery_price == 0:
        delivery_price = "Ücretsiz"
    else:
        delivery_price = order.delivery_price

    vade_farki = order.order_total - order.order_amount

    html_message = render_to_string("backend/email/cargo_notification.html", {
        'siparis_no': order.order_number,
        'order_list': order_list,
        'sales_amount': order.order_total,
        'order_date': order.created_at,
        'address': address,
        'order_list_count': len(order_list),
        'total': total,
        'grand_total': grand_total,
        'delivery_price': delivery_price,
        'vade_farki': vade_farki,
    })
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject=my_subject,
        body=plain_message,
        from_email=EMAIL_HOST_USER,
        to=[my_recipient]
    )

    message.attach_alternative(html_message, "text/html")
    message.send()

    msg = 'success'
    return msg

def customerTredyShopExtraditionRequestOrder(request, email, order_number):
    my_subject = "İade talebiniz alındı."
    my_recipient = email

    html_message = render_to_string("backend/email/customer_extradition_request.html", {
        'siparis_no': order_number,
    })
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject=my_subject,
        body=plain_message,
        from_email=EMAIL_HOST_USER,
        to=[my_recipient]
    )

    message.attach_alternative(html_message, "text/html")
    message.send()

    msg = 'success'
    return msg

def sendExtraditionRequestInfoEmail(request, email, order_number, siparis_tarihi, iade_tarihi, urun_id):
    try:
        my_subject = "Yeni bir iade talebin var!"
        my_recipient = email

        html_message = render_to_string("backend/email/extradition_request.html", {
            'siparis_no': order_number,
            'order_date': siparis_tarihi,
            'iade_tarihi': iade_tarihi,
            'urun_id': urun_id,
        })
        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject=my_subject,
            body=plain_message,
            from_email=EMAIL_HOST_USER,
            to=[my_recipient]
        )

        message.attach_alternative(html_message, "text/html")
        message.send()

        msg = 'success'
        return msg

    except:
        msg = 'failed'
        return msg


def productStatistic(barcode, title, quantity, satis, harcama=None):
    if ProductSellStatistic.objects.filter(barcode=barcode).count() > 0:
        statistic = get_object_or_404(ProductSellStatistic, barcode=barcode)
        statistic.sell_count += quantity
        statistic.satis += satis
        statistic.save()
    else:
        ProductSellStatistic.objects.create(barcode=barcode, name=title, sell_count=quantity,
                                            satis=satis, maliyet=harcama)

############################  TRENDYOL URUN GONDERME ###############################

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


def trendyolUpdateProductData(barcode, title, model_code, brandid, categoryid, stock_code, description, vatRate,
                              deliveryDuration, cargoid, shipmentid, returningid, images,
                              data_attributes):
    data = {
        "barcode": str(barcode),
        "title": str(title),
        "productMainId": str(model_code),
        "brandId": int(brandid),
        "categoryId": int(categoryid),
        "stockCode": str(stock_code),
        "description": description,
        "currencyType": "TRY",
        "vatRate": int(vatRate),
        "deliveryDuration": int(deliveryDuration),
        "images": images,
        "attributes": data_attributes,
        "cargoCompanyId": int(cargoid),
        "shipmentAddressId": int(shipmentid),
        "returningAddressId": int(returningid),
    }

    return data


def trendyolUpdateData(barcode, quantity, list_price, sale_price):
    data = {
        "barcode": str(barcode),
        "quantity": int(quantity),
        "listPrice": float(list_price),
        "salePrice": float(sale_price)
    }

    return data


def trendyolDeleteData(products):
    data = []

    for p in products:
        data.append(
            {
                "barcode": str(p.barcode)
            }
        )

    return data


def callingProduct(category, title):
    products = ApiProduct.objects.filter(subbottomcategory=category, title__icontains=title, is_publish=True,
                                         is_publish_trendyol=False)

    return products


def updateCallingProduct(category, title):
    products = ApiProduct.objects.filter(subbottomcategory=category, title__icontains=title, is_publish=True,
                                         is_publish_trendyol=True)
    return products


def trendyolAttributes(trendyol_category):
    attributes_url = f"https://api.trendyol.com/sapigw/product-categories/{trendyol_category}/attributes"
    product_attributes = requests.request("GET", attributes_url)
    product_attributes = product_attributes.json()
    return product_attributes


def trendyolCategory(category_title):
    categories = requests.get("https://api.trendyol.com/sapigw/product-categories")

    trendyol_category = None

    for c in categories.json()['categories']:
        for c1 in c['subCategories']:
            if c1['subCategories'] != []:
                for c2 in c1['subCategories']:
                    if c2['subCategories'] != []:
                        for c3 in c2['subCategories']:
                            if c3['subCategories'] != []:
                                for c4 in c3['subCategories']:
                                    if c4['subCategories'] != []:
                                        for c5 in c4['subCategories']:
                                            if category_title.lower() == str(c5['name']).lower():
                                                trendyol_category = c5['id']
                                    else:
                                        if category_title.lower() == str(c4['name']).lower():
                                            trendyol_category = c4['id']
                            else:
                                if category_title.lower() == str(c3['name']).lower():
                                    trendyol_category = c3['id']
                    else:
                        if category_title.lower() == str(c2['name']).lower():
                            trendyol_category = c2['id']
            else:
                if category_title.lower() == str(c1['name']).lower():
                    trendyol_category = c1['id']

    return trendyol_category

def sendTrendyol(category_title, title, category_no, shipmentId, returningid, vatRate, cargoid):
    product_data = []
    items = []
    data_attributes = []

    attributes = []
    trendyol = Trendyol.objects.all().last()
    trendyol_category = trendyolCategory(category_title)
    product_attributes = trendyolAttributes(trendyol_category)

    ##Calling Product
    products = callingProduct(category=SubBottomCategory.objects.get(category_no=category_no), title=title)

    if trendyol_category:
        for a in product_attributes['categoryAttributes']:
            attributes.append(a)

        for p in products:
            title = p.title
            detail = p.detail
            if detail == '' or detail == None:
                detail = title
            images = []
            if p.image_url1:
                images.append({'url': p.image_url1})
            if p.image_url2:
                images.append({'url': p.image_url2})
            if p.image_url3:
                images.append({'url': p.image_url3})
            if p.image_url4:
                images.append({'url': p.image_url4})
            if p.image_url5:
                images.append({'url': p.image_url5})
            if p.image_url6:
                images.append({'url': p.image_url6})
            if p.image_url7:
                images.append({'url': p.image_url7})
            if p.image_url8:
                images.append({'url': p.image_url8})

            for a in attributes:
                if category_title == "Omuz Çantası" or category_title == "Babet" or category_title == "Bot & Bootie" or category_title == "Bot" or category_title == "Çizme" or category_title == "Ev Botu" or category_title == "Ev Terliği" or category_title == "Panduf" or category_title == "Atlet" or category_title == "Büstiyer" or category_title == "Bluz" or category_title == "Body" or category_title == "Kazak" or category_title == "Hırka" or category_title == "Süveter" or category_title == "Tunik" or category_title == "Ceket" or category_title == "Mont" or category_title == "Kaban" or category_title == "Yelek" or category_title == "Gömlek" or category_title == "Kimono&Kaftan" or category_title == "Panço" or category_title == "Sweatshirt" or category_title == "T-Shirt" or category_title == "Yağmurluk&Rüzgarlık" or category_title == "Etek" or category_title == "Pantolon" or category_title == "Jeans" or category_title == "Şort & Bermuda" or category_title == "Tayt" or category_title == "Eşofman Altı" or category_title == "Eşofman Takımı" or category_title == "Pijama Altı" or category_title == "Pijama Takımı" or category_title == "Abiye & Mezuniyet Elbisesi" or category_title == "Elbise" or category_title == "Salopet" or category_title == "Tulum" or category_title == "Fantezi Babydoll" or category_title == "Fantezi Gecelik" or category_title == "Fantezi İç Çamaşır Takımları" or category_title == "Fantezi Kostüm" or category_title == "Fantezi Külot" or category_title == "Fantezi Sütyen" or category_title == "Gecelik" or category_title == "Jartiyer" or category_title == "Külot" or category_title == "Sütyen" or category_title == "Bijuteri Kolye" or category_title == "Bijuteri Bileklik" or category_title == "Bijuteri Küpe":
                    if a['attribute']['name'] == 'Yaş Grubu':
                        if p.age_group:
                            for s in a['attributeValues']:
                                if p.age_group == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Cinsiyet':
                        if p.sextype:
                            for s in a['attributeValues']:
                                if p.sextype.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                if category_title == "Atlet" or category_title == "Büstiyer" or category_title == "Bluz" or category_title == "Body" or category_title == "Kazak" or category_title == "Hırka" or category_title == "Süveter" or category_title == "Tunik" or category_title == "Ceket" or category_title == "Mont" or category_title == "Kaban" or category_title == "Yelek" or category_title == "Gömlek" or category_title == "Kimono&Kaftan" or category_title == "Panço" or category_title == "Sweatshirt" or category_title == "T-Shirt" or category_title == "Yağmurluk&Rüzgarlık":
                    if a['attribute']['name'] == 'Beden':
                        if p.size:
                            for s in a['attributeValues']:
                                if p.size.name.lower() == s['name'].lower():
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == "Kumaş Tipi":
                        if p.fabrictype:
                            for s in a['attributeValues']:
                                if p.fabrictype.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Boy':
                        if p.height:
                            for s in a['attributeValues']:
                                if p.height.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Kalıp':
                        if p.pattern:
                            for s in a['attributeValues']:
                                if p.pattern.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Ortam':
                        if p.environment:
                            for s in a['attributeValues']:
                                if p.environment.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                if category_title == "Etek":
                    if a['attribute']['name'] == 'Beden':
                        if p.size:
                            for s in a['attributeValues']:
                                if p.size.name.lower() == s['name'].lower():
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == "Kumaş Tipi":
                        if p.fabrictype:
                            for s in a['attributeValues']:
                                if p.fabrictype.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Boy':
                        if p.height:
                            for s in a['attributeValues']:
                                if p.height.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                if category_title == "Pantolon" or category_title == "Jeans" or category_title == "Şort & Bermuda" or category_title == "Tayt" or category_title == "Eşofman Altı" or category_title == "Pijama Altı" or category_title == "Salopet" or category_title == "Tulum":
                    if a['attribute']['name'] == 'Beden':
                        if p.size:
                            for s in a['attributeValues']:
                                if p.size.name.lower() == s['name'].lower():
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == "Kumaş Tipi":
                        if p.fabrictype:
                            for s in a['attributeValues']:
                                if p.fabrictype.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Bel':
                        if p.waist:
                            for s in a['attributeValues']:
                                if p.waist.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Boy':
                        if p.height:
                            for s in a['attributeValues']:
                                if p.height.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Paça Tipi':
                        if p.legtype:
                            for s in a['attributeValues']:
                                if p.legtype.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Materyal':
                        if p.material:
                            for s in a['attributeValues']:
                                if p.material.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                if category_title == "Eşofman Takımı" or category_title == "Pijama Takımı" or category_title == "Abiye & Mezuniyet Elbisesi" or category_title == "Elbise" or category_title == "Salopet" or category_title == "Tulum":
                    if a['attribute']['name'] == 'Beden':
                        if p.size:
                            for s in a['attributeValues']:
                                if p.size.name.lower() == s['name'].lower():
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == "Kumaş Tipi":
                        if p.fabrictype:
                            for s in a['attributeValues']:
                                if p.fabrictype.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Boy':
                        if p.height:
                            for s in a['attributeValues']:
                                if p.height.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Kalıp':
                        if p.pattern:
                            for s in a['attributeValues']:
                                if p.pattern.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )

                if category_title == "Fantezi Babydoll" or category_title == "Fantezi Gecelik" or category_title == "Fantezi İç Çamaşır Takımları" or category_title == "Fantezi Külot" or category_title == "Fantezi Sütyen" or category_title == "Gecelik" or category_title == "Jartiyer" or category_title == "Külot" or category_title == "Sütyen":
                    if a['attribute']['name'] == 'Beden':
                        if p.size:
                            for s in a['attributeValues']:
                                if p.size.name.lower() == s['name'].lower():
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == "Kumaş Tipi":
                        if p.fabrictype:
                            for s in a['attributeValues']:
                                if p.fabrictype.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )

                    if a['attribute']['name'] == 'Kalıp':
                        if p.pattern:
                            for s in a['attributeValues']:
                                if p.pattern.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                if category_title == "Fantezi Kostüm":
                    if a['attribute']['name'] == 'Beden':
                        if p.size:
                            for s in a['attributeValues']:
                                if p.size.name.lower() == s['name'].lower():
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                if category_title == "Bijuteri Kolye" or category_title == "Bijuteri Bileklik" or category_title == "Bijuteri Küpe":
                    if a['attribute']['name'] == 'Beden':
                        if p.size:
                            for s in a['attributeValues']:
                                if p.size.name.lower() == s['name'].lower():
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Tema / Stil':
                        if p.bijuteri_theme:
                            for s in a['attributeValues']:
                                if p.bijuteri_theme.name.lower() == s['name'].lower():
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                if category_title == "Babet" or category_title == "Bot & Bootie" or category_title == "Çizme" or category_title == "Ev Botu" or category_title == "Ev Terliği" or category_title == "Panduf":
                    if a['attribute']['name'] == 'Beden':
                        if p.size:
                            for s in a['attributeValues']:
                                if p.size.name.lower() == s['name'].lower():
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Topuk Tipi':
                        if p.heeltype:
                            for s in a['attributeValues']:
                                if p.heeltype.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Topuk Boyu':
                        if p.heelsize:
                            for s in a['attributeValues']:
                                if p.heelsize.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                if category_title == "Ekran Koruyucu Film":
                    if a['attribute']['name'] == 'Garanti Süresi':
                        if p.warranty:
                            for s in a['attributeValues']:
                                if p.warranty == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                if category_title == "Tablet Kılıfı":
                    if a['attribute']['name'] == 'Uyku Modu':
                        if p.sleepmode.name:
                            for s in a['attributeValues']:
                                if p.sleepmode.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Kılıf Tipi':
                        if p.casetype.name:
                            for s in a['attributeValues']:
                                if p.casetype.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Uyumlu Marka':
                        if p.compatible:
                            for s in a['attributeValues']:
                                if p.compatible == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Uyumlu Model':
                        if p.tabletmodel.name:
                            for s in a['attributeValues']:
                                if p.tabletmodel.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
            if category_title == "Kapak & Kılıf" or category_title == "Bluz" or category_title == "Body" or category_title == "Kazak" or category_title == "Hırka" or category_title == "Süveter" or category_title == "Tunik" or category_title == "Ceket" or category_title == "Mont" or category_title == "Kaban" or category_title == "Yelek" or category_title == "Tablet Kılıfı" or category_title == "Omuz Çantası" or category_title == "Babet" or category_title == "Bot & Bootie" or category_title == "Çizme" or category_title == "Ev Botu" or category_title == "Ev Terliği" or category_title == "Panduf" or category_title == "Atlet" or category_title == "Büstiyer" or category_title == "Gömlek" or category_title == "Kimono&Kaftan" or category_title == "Panço" or category_title == "Sweatshirt" or category_title == "T-Shirt" or category_title == "Yağmurluk&Rüzgarlık" or category_title == "Etek" or category_title == "Pantolon" or category_title == "Jeans" or category_title == "Şort & Bermuda" or category_title == "Tayt" or category_title == "Eşofman Altı" or category_title == "Eşofman Takımı" or category_title == "Pijama Altı" or category_title == "Pijama Takımı" or category_title == "Abiye & Mezuniyet Elbisesi" or category_title == "Elbise" or category_title == "Salopet" or category_title == "Tulum" or category_title == "Fantezi Babydoll" or category_title == "Fantezi Gecelik" or category_title == "Fantezi İç Çamaşır Takımları" or category_title == "Fantezi Kostüm" or category_title == "Fantezi Külot" or category_title == "Fantezi Sütyen" or category_title == "Jartiyer" or category_title == "Külot" or category_title == "Sütyen" or category_title == "Gecelik" or category_title == "Bijuteri Kolye" or category_title == "Bijuteri Bileklik" or category_title == "Bijuteri Küpe":
                if p.color is not None:
                    data_attributes.append(
                        {
                            "attributeId": 47,
                            "customAttributeValue": str(p.color.name).upper()
                        }
                    )

            items.append(
                trendyolProductData(barcode=p.barcode, title=title, model_code=p.stock_code, brandid=2071923,
                                    categoryid=trendyol_category, quantity=p.quantity, stock_code=p.stock_code,
                                    desi=1,
                                    list_price=p.trendyol_price, sale_price=p.trendyol_price, cargoid=cargoid,
                                    description=detail, vatRate=vatRate, deliveryDuration=2,
                                    shipmentid=shipmentId,
                                    returningid=returningid, images=images,
                                    data_attributes=data_attributes))

            product_data = items
            data_attributes = []
            p.trendyol_category_id = int(trendyol_category)
            p.save()
    if round(len(product_data) / 1000) <= 1:
        try:
            api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                                    supplier_id=trendyol.saticiid)
            service = ProductIntegrationService(api)
            response = service.create_products(items=product_data)
            log_record = LogRecords.objects.create(log_type="1", batch_id=str(response['batchRequestId']))
            return str(log_record.batch_id)
        except Exception as e:
            return "Error"
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
        return "Success"