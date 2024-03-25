from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from adminpage.models import UpdateHistory
from categorymodel.models import SubBottomCategory
from ciceksepeti.forms import *
from ciceksepeti.models import *
from django.contrib import messages
from ciceksepeti.services import *
from ciceksepeti.api import *
from django.contrib.auth.decorators import login_required

from product.models import Product, ProductVariant


# Create your views here.
@login_required(login_url="/yonetim/giris-yap/")
def ciceksepeti_hesap_bilgileri(request):
    context = {}
    ciceksepeti = Ciceksepeti.objects.all()

    if ciceksepeti.count() > 0:
        form = CicekSepetiHesapBilgileri(instance=ciceksepeti.last(), data=request.POST or None,
                                         files=request.FILES or None)
        context.update({'form': form})
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'Çiçeksepeti hesap bilgileri başarıyla güncellendi!')
                return redirect("ciceksepeti_hesap_bilgileri")
    else:
        form = CicekSepetiHesapBilgileri(data=request.POST, files=request.FILES)
        context.update({'form': form})
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'Çiçeksepeti hesap bilgileri başarıyla eklendi!')
                return redirect("ciceksepeti_hesap_bilgileri")

    return render(request, 'backend/yonetim/sayfalar/ciceksepeti/hesap_bilgileri.html', context)


def kategorileri_al(request):
    ciceksepeti = Ciceksepeti.objects.all()
    api = CiceksepetiApiClient(api_key=ciceksepeti.last().apikey,
                               supplier_id=ciceksepeti.last().saticiid)
    service = ProductIntegrationService(api)
    response = service.get_categories()
    kategori_list = []

    for seviye1 in response['categories']:
        name = ""
        if seviye1['name'] == 'Hediye':
            for seviye2 in seviye1['subCategories']:
                name = seviye2['name']
                if seviye2['subCategories'] == []:
                    kategori_list.append({'name': name, 'id': seviye2['id']})
                else:
                    for seviye3 in seviye2['subCategories']:
                        name = seviye2['name'] + ">" + seviye3['name']
                        if seviye3['subCategories'] == []:
                            kategori_list.append({'name': name, 'id': seviye3['id']})
                        else:
                            for seviye4 in seviye3['subCategories']:
                                name = seviye2['name'] + ">" + seviye3['name'] + ">" + seviye4['name']
                                if seviye4['subCategories'] == []:
                                    kategori_list.append({'name': name, 'id': seviye4['id']})
                                else:
                                    for seviye5 in seviye4['subCategories']:
                                        name = seviye2['name'] + ">" + seviye3['name'] + ">" + seviye4['name'] + ">" + \
                                               seviye5['name']
                                        if seviye5['subCategories'] == []:
                                            kategori_list.append({'name': name, 'id': seviye5['id']})
                                        else:
                                            for seviye6 in seviye5['subCategories']:
                                                name = seviye2['name'] + ">" + seviye3['name'] + ">" + seviye4[
                                                    'name'] + ">" + seviye5['name'] + ">" + seviye6['name']
                                                if seviye6['subCategories'] == []:
                                                    kategori_list.append({'name': name, 'id': seviye6['id']})
                                                else:
                                                    for seviye7 in seviye6['subCategories']:
                                                        name = seviye2['name'] + ">" + seviye3['name'] + ">" + seviye4[
                                                            'name'] + ">" + seviye5['name'] + ">" + seviye6[
                                                                   'name'] + ">" + seviye7['name']
                                                        if seviye7['subCategories'] == []:
                                                            kategori_list.append({'name': name, 'id': seviye7['id']})
                                                        else:
                                                            for seviye8 in seviye7['subCategories']:
                                                                name = seviye2['name'] + ">" + seviye3['name'] + ">" + \
                                                                       seviye4['name'] + ">" + seviye5['name'] + ">" + \
                                                                       seviye6['name'] + ">" + + seviye7['name'] + ">" + \
                                                                       seviye8['name']
                                                                kategori_list.append(
                                                                    {'name': name, 'id': seviye8['id']})
    t = render_to_string('backend/yonetim/sayfalar/ciceksepeti/kategoriler.html',
                         {'ciceksepeti_kategoriler': kategori_list})
    return JsonResponse({'data': t})


@login_required(login_url="/yonetim/giris-yap/")
def ciceksepeti_kategori_eslestir(request):
    context = {}
    tredyshop_categoriler = SubBottomCategory.objects.all()
    urunler = Product.objects.filter(is_publish=True)
    ciceksepeti = Ciceksepeti.objects.all()

    durum = request.GET.get('durum', 'eslestirilmemis')
    kategori = request.GET.get('kategori')
    model_kodu = request.GET.get('model_kodu')
    baslik = request.GET.get('baslik')
    barkod = request.GET.get('barkod')

    query = f"?durum={durum}&kategori={kategori}&model_kodu={model_kodu}&baslik={baslik}&barkod={barkod}"

    if durum:
        if durum == 'eslestirilmiş':
            urunler = CiceksepetiUrunler.objects.all()
        elif durum == 'eslestirilmemis':
            urunler = ProductVariant.objects.filter(is_publish=True)

    if kategori:
        select_category = SubBottomCategory.objects.get(id=kategori)
        urunler = ProductVariant.objects.filter(product__subbottomcategory_id=kategori).order_by(
            "-create_at")
        context.update({
            'select_category': select_category,
        })

    if barkod:
        barcode = barkod
        urunler = ProductVariant.objects.filter(barcode=barkod).order_by("-create_at")
        context.update({
            'barcode': barcode,
        })

    if baslik:
        title = baslik
        urunler = ProductVariant.objects.filter(title__icontains=baslik).order_by(
            "-create_at")
        context.update({
            'title': title,
        })

    paginator = Paginator(urunler, 50)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context.update({
        'tredyshop_categoriler': tredyshop_categoriler,
        'products': products,
        'kategori': kategori,
        'durum': durum,
    })

    return render(request, 'backend/yonetim/sayfalar/ciceksepeti/kategori_eslestir.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def ciceksepeti_kategori_eslestir_ajax(request):
    product_id = request.GET.get('product_id')
    kategori_id = request.GET.get('kategori_id')

    if CiceksepetiUrunler.objects.filter(urun=ProductVariant.objects.get(id=product_id)).count() < 1:
        CiceksepetiUrunler.objects.create(urun=ProductVariant.objects.get(id=product_id),
                                          ciceksepeti_kategori_id=kategori_id)
    else:
        cickeksepeti_kategori = get_object_or_404(CiceksepetiUrunler, product__id=product_id)
        cickeksepeti_kategori.ciceksepeti_kategori_id = kategori_id
        cickeksepeti_kategori.save()
    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def ciceksepeti_send_api(request, urun, kategori_id):
    ciceksepeti = Ciceksepeti.objects.all()
    api = CiceksepetiApiClient(api_key=ciceksepeti.last().apikey,
                               supplier_id=ciceksepeti.last().saticiid)
    service = ProductIntegrationService(api)

    image_list = []
    if urun.product.image_url1:
        image_list.append(urun.product.image_url1)
    if urun.product.image_url2:
        image_list.append(urun.product.image_url2)
    if urun.product.image_url3:
        image_list.append(urun.product.image_url3)
    if urun.product.image_url4:
        image_list.append(urun.product.image_url4)
    if urun.product.image_url5:
        image_list.append(urun.product.image_url5)

    category_attribute = service.get_category_attributes(kategori_id)

    attribute_list = []

    for attribute in category_attribute['categoryAttributes']:
        if attribute['attributeId'] == 7 and attribute['attributeName'] == "Beden":
            for value in attribute['attributeValues']:
                if urun.size.name == value['name']:
                    attribute_list.append({
                        "id": 7,
                        "ValueId": value['id'],
                        "TextLength": 0
                    })

        if attribute['attributeId'] == 2001498 and attribute['attributeName'] == 'Yaş Grubu':
            for value in attribute['attributeValues']:
                if urun.product.age_group == value['name']:
                    attribute_list.append({
                        "id": 2001498,
                        "ValueId": value['id'],
                        "TextLength": 0
                    })

        if attribute['attributeId'] == 2000310 and attribute['attributeName'] == 'Renk':
            for value in attribute['attributeValues']:
                if urun.color.name == value['name']:
                    attribute_list.append({
                        "id": 2000310,
                        "ValueId": value['id'],
                        "TextLength": 0
                    })

        if attribute['attributeId'] == 2000396 and attribute['attributeName'] == 'Cinsiyet':
            for value in attribute['attributeValues']:
                if urun.product.sextype.name == value['name']:
                    attribute_list.append({
                        "id": 2000396,
                        "ValueId": value['id'],
                        "TextLength": 0
                    })

    items = {
        "products": [
            {
                "productName": str(urun.title),
                "mainProductCode": str(urun.model_code),
                "stockCode": str(urun.stock_code),
                "categoryId": 13349,
                "description": str(urun.product.detail),
                "supplierDescription": "",
                "mediaLink": "",
                "deliveryMessageType": 18,
                "deliveryType": 2,
                "stockQuantity": int(urun.quantity),
                "salesPrice": float(urun.ciceksepeti_price),
                "listPrice": float(urun.ciceksepeti_price),
                "barcode": str(urun.barcode),
                "images": image_list,
                "Attributes": attribute_list
            },
        ]
    }

    response = service.create_products(items=items)
    result = service.get_batch_requests(batch_request_id=response['batchId'])
    return result


@login_required(login_url="/yonetim/giris-yap/")
def ciceksepeti_urun_gonder(request):
    context = {}
    category = SubBottomCategory.objects.all()
    urunler = CiceksepetiUrunler.objects.all()

    urun_durumu = request.GET.get('urun_durumu')
    kategori = request.GET.get('kategori')
    model_kodu = request.GET.get('model_kodu')
    baslik = request.GET.get('baslik')
    barkod = request.GET.get('barkod')

    query = f"?kategori={kategori}&model_kodu={model_kodu}&baslik={baslik}&barkod={barkod}"

    if urun_durumu:
        if urun_durumu == 'tum-urunler':
            urunler = CiceksepetiUrunler.objects.all()
        elif urun_durumu == 'yayinda':
            urunler = CiceksepetiUrunler.objects.filter(yayin_durumu=True)
        elif urun_durumu == 'yayinde-olmayan':
            urunler = CiceksepetiUrunler.objects.filter(yayin_durumu=False)

    if kategori:
        select_category = SubBottomCategory.objects.get(id=kategori)
        urunler = CiceksepetiUrunler.objects.filter(subbottomcategory_id=kategori, yayin_durumu=False).order_by(
            "-create_at")
        context.update({
            'select_category': select_category,
        })

    if barkod:
        barcode = barkod
        urunler = CiceksepetiUrunler.objects.filter(barcode=barkod).order_by("-create_at")
        context.update({
            'barcode': barcode,
        })

    if baslik:
        title = baslik
        urunler = CiceksepetiUrunler.objects.filter(title__icontains=baslik).order_by(
            "-create_at")
        context.update({
            'title': title,
        })

    paginator = Paginator(urunler, 50)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context.update({
        'products': products,
        'query': query,
        'category': category,
    })

    return render(request, 'backend/yonetim/sayfalar/ciceksepeti/urun_islemleri.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def ciceksepeti_urun_gonder_ajax(request):
    product_id = request.GET.get('productID')
    kategori_id = request.GET.get('kategoriID')
    data = "failed"
    urun = get_object_or_404(ProductVariant, id=product_id)
    if urun:
        ciceksepeti_send_api(request, urun=urun, kategori_id=kategori_id)
        urun.is_publish_ciceksepeti = True
        ciceksepeti_urun = get_object_or_404(CiceksepetiUrunler, urun_id=product_id)
        ciceksepeti_urun.yayin_durumu = True
        ciceksepeti_urun.urun.is_publish_ciceksepeti = True
        ciceksepeti_urun.save()
        ciceksepeti_urun.urun.save()
    data = "success"
    return JsonResponse(data=data, safe=False)


def ciceksepetiUpdateData(stock_code, quantity, list_price, sale_price):
    data = {
        "stockCode": str(stock_code),
        "stockQuantity": int(quantity),
        "listPrice": float(list_price),
        "salesPrice": float(sale_price)
    }

    return data


def ciceksepeti_update_function(products):
    items = []
    product_data = None
    ciceksepeti = Ciceksepeti.objects.all()
    result = 'success'

    if products.count() > 0:
        for p in products:
            listprice = p.urun.ciceksepeti_price
            saleprice = p.urun.ciceksepeti_price
            if p.urun.is_ciceksepeti_discountprice:
                saleprice = p.urun.ciceksepeti_discountprice

            if p.urun.quantity > 2:
                items.append(
                    ciceksepetiUpdateData(stock_code=p.urun.stock_code, quantity=p.urun.quantity,
                                          list_price=listprice,
                                          sale_price=saleprice)
                )
            else:
                items.append(
                    ciceksepetiUpdateData(stock_code=p.urun.stock_code, quantity=0, list_price=listprice,
                                          sale_price=saleprice)
                )

            product_data = {
                "items": items
            }
        try:
            api = CiceksepetiApiClient(api_key=ciceksepeti.last().apikey,
                                       supplier_id=ciceksepeti.last().saticiid)
            service = ProductIntegrationService(api)
            response = service.update_stok_price(items=product_data)
            UpdateHistory.objects.create(history_type="Çiceksepeti Stok&Fiyat Güncelleme")
            return response
        except:
            return 'error'


@login_required(login_url="/yonetim/giris-yap/")
def ciceksepeti_stok_fiyat_guncelle(request):
    product_count = CiceksepetiUrunler.objects.filter(yayin_durumu=True).count()
    i = 0
    while i / 200 <= round(product_count / 200):
        products = CiceksepetiUrunler.objects.filter(yayin_durumu=True)[i:i + 200]
        ciceksepeti_update_function(products)
        i += 200
    return redirect('ciceksepeti_urun_gonder')
