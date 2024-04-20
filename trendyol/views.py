from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from adminpage.models import Trendyol, UpdateHistory
from categorymodel.models import SubBottomCategory
from product.models import ProductVariant, Product
from trendyol import models
from django.contrib.auth.decorators import login_required
from trendyol.helpers import trendyolUpdateData, trendyolProductData
from trendyol.api import TrendyolApiClient
from trendyol.forms import TrendyolUpdateForm, TrendyolAddForm
from trendyol.models import TrendyolProduct, TrendyolAttributes, LogRecords, TrendyolReport, TrendyolReportProduct
from trendyol.services import ProductIntegrationService

# Create your views here.

@login_required(login_url="/yonetim/giris-yap/")
def trendyol_hesap_bilgileri(request):
    context = {}
    trendyol = Trendyol.objects.all()
    if trendyol.count() > 0:
        form = TrendyolUpdateForm(instance=trendyol.last(), data=request.POST or None,
                                  files=request.FILES or None)
        context.update({'form': form})
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'Trendyol hesap bilgileri başarıyla güncellendi!')
                return redirect("trendyol_hesap_bilgileri")
    else:
        form = TrendyolAddForm(data=request.POST, files=request.FILES)
        context.update({'form': form})
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'Trendyol hesap bilgileri başarıyla eklendi!')
                return redirect("trendyol_hesap_bilgileri")

    return render(request, 'backend/yonetim/sayfalar/trendyol/hesap_bilgileri.html', context)

@login_required(login_url="/yonetim/giris-yap/")
def trendyol_kategori_eslestir(request):
    context = {}
    trendyol_product = TrendyolProduct.objects.all()
    urunler = ProductVariant.objects.filter(is_publish=True, quantity__gte=10).exclude(trendyolproduct__in=trendyol_product).order_by("-create_at","model_code", "-quantity")

    subbottomcategory = SubBottomCategory.objects.all()
    category = request.GET.get('kategori')
    durum = request.GET.get('durum')
    kaynak = request.GET.get('kaynak')
    yayin = request.GET.get('yayin')

    if category:
        select_category = int(category)
        context.update({'select_category': select_category})
        if durum == "eslestirilmis":
            urunler = trendyol_product.filter(product__product__subbottomcategory_id=category)
        else:
            urunler = urunler.filter(product__subbottomcategory_id=category)

    if durum:
        if durum == "eslestirilmis":
            urunler = trendyol_product

    if kaynak:
        if kaynak != "None" or kaynak != None:
            if durum == "eslestirilmis":
                urunler = trendyol_product.filter(product__product__dropshipping=kaynak)
            else:
                urunler = urunler.filter(product__dropshipping=kaynak)

    if yayin:
        if yayin != "None" or yayin != None:
            if durum == "eslestirilmis":
                urunler = trendyol_product.filter(product__is_publish_trendyol=yayin)
            else:
                urunler = urunler.filter(is_publish_trendyol=yayin)

    query = f"?kategori={category}&durum={durum}&kaynak={kaynak}&yayin={yayin}"

    paginator = Paginator(urunler, 10)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context.update({
        'products': products,
        'subbottomcategory': subbottomcategory,
        'durum': durum,
        'kaynak':kaynak,
        'yayin':yayin,
        'query':query,
    })
    return render(request, 'backend/yonetim/sayfalar/trendyol/kategori_eslestir.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_kategori_al(request):
    trendyol = Trendyol.objects.all().last()
    api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                            supplier_id=trendyol.saticiid)
    service = ProductIntegrationService(api)
    response = service.get_categories()
    kategori_list = []

    for c in response['categories']:
        for c1 in c['subCategories']:
            name = c1['name']
            if c1['subCategories'] == []:
                kategori_list.append({'id': c1['id'], 'name': name})
            else:
                for c2 in c1['subCategories']:
                    name = c1['name'] + " > " + c2['name']
                    if c2['subCategories'] == []:
                        kategori_list.append({'id': c2['id'], 'name': name})
                    else:
                        for c3 in c2['subCategories']:
                            name = c1['name'] + " > " + c2['name'] + " > " + c3['name']
                            if c3['subCategories'] == []:
                                kategori_list.append({'id': c3['id'], 'name': name})
                            else:
                                for c4 in c3['subCategories']:
                                    name = c1['name'] + " > " + c2['name'] + " > " + c3['name'] + " > " + c4['name']
                                    if c4['subCategories'] == []:
                                        kategori_list.append({'id': c4['id'], 'name': name})
                                    else:
                                        for c5 in c4['subCategories']:
                                            name = c1['name'] + " > " + c2['name'] + " > " + c3['name'] + " > " + c4[
                                                'name'] + " > " + c5['name']
                                            kategori_list.append({'id': c5['id'], 'name': name})

    t = render_to_string('backend/yonetim/sayfalar/trendyol/kategoriler.html',
                         {'kategori_list': kategori_list})
    return JsonResponse({'data': t})


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_ozellikleri_getir(request):
    category_id = request.GET.get('category_id')
    product_id = request.GET.get('product_id')
    category_name = request.GET.get('category_name')

    try:
        product = ProductVariant.objects.get(id=product_id)
        trendyol_product = TrendyolProduct.objects.get(product=product)
    except:
        trendyol_product = None

    trendyol = Trendyol.objects.all().last()
    api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                            supplier_id=trendyol.saticiid)
    service = ProductIntegrationService(api)
    response = service.get_category_attributes(category_id=category_id)
    ozellik_list = []
    for attribute in response['categoryAttributes']:
        ozellik_list.append(
            {'product_id': product_id, 'allowCustom': attribute['allowCustom'],
             'id': attribute['attribute']['id'], 'name': attribute['attribute']['name'],
             'required': attribute['required'], 'values': attribute['attributeValues']})
    t = render_to_string('backend/yonetim/sayfalar/trendyol/ozellikler.html',
                         {'ozellik_list': ozellik_list, 'product_id': product_id, 'category_id': category_id,
                          'category_name': category_name, 'trendyol_product': trendyol_product})
    return JsonResponse({'data': t})


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_ozellik_kaydet(request):
    veriler = request.GET.getlist('attributes[]')
    product_id = request.GET.get('product_id')
    category_name = request.GET.get('category_name')
    category_id = request.GET.get('category_id')
    product = get_object_or_404(ProductVariant, id=product_id)

    if TrendyolProduct.objects.filter(product_id=product_id).count() < 1:
        trendyol_product = TrendyolProduct.objects.create(product=product, category_id=category_id,
                                                          category=category_name.replace("&gt;", ">").replace("&amp;","&"), is_ready=True)
        for v in veriler:
            if v.replace('"', '').split('/*/')[1] != '' or v.replace('"', '').split('/*/') != None:
                TrendyolAttributes.objects.create(trendyol_product=trendyol_product,
                                                  name=v.replace('"', '').split('/*/')[0],
                                                  value=v.replace('"', '').split('/*/')[1],
                                                  code=v.replace('"', '').split('/*/')[2],
                                                  customStatus=v.replace('"', '').split('/*/')[3])

    else:
        trendyol_product = TrendyolProduct.objects.get(product=product)
        trendyol_product.category_id = category_id
        trendyol_product.category_name = category_name
        for atr in TrendyolAttributes.objects.filter(trendyol_product=trendyol_product):
            atr.delete()
        for v in veriler:
            if v.replace('"', '').split('/*/')[1] != '' or v.replace('"', '').split('/*/') != None:
                TrendyolAttributes.objects.create(trendyol_product=trendyol_product,
                                                  name=v.replace('"', '').split('/*/')[0],
                                                  value=v.replace('"', '').split('/*/')[1],
                                                  code=v.replace('"', '').split('/*/')[2],
                                                  customStatus=v.replace('"', '').split('/*/')[3])

    data = 'success'
    return JsonResponse(data=data, safe=False)


def trendyol_urun_gonder(request):
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

        sevkiyat = trendyol.sevkiyatadresid_2
        iade = trendyol.iadeadresid_2

        if p.product.product.dropshipping == "Modaymış":
            sevkiyat = trendyol.sevkiyatadresid_1
            iade = trendyol.iadeadresid_1

        elif p.product.product.dropshipping == "Leyna":
            sevkiyat = trendyol.sevkiyatadresid_4
            iade = trendyol.iadeadresid_2

        elif p.product.product.dropshipping == "Bella Notte":
            sevkiyat = trendyol.sevkiyatadresid_3
            iade = trendyol.iadeadresid_2

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
            trendyolProductData(barcode=p.product.barcode, title=title, model_code=p.product.model_code, brandid=2071923,
                                categoryid=p.category_id, quantity=p.product.quantity, stock_code=p.product.stock_code,
                                desi=1,
                                list_price=p.product.trendyol_price, sale_price=p.product.trendyol_price, cargoid=10,
                                description=detail, vatRate=10, deliveryDuration=2,
                                shipmentid=sevkiyat,
                                returningid=iade, images=images,
                                data_attributes=attributes))

        product_data = items

    if round(len(product_data) / 1000) <= 1:
        try:
            api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                                    supplier_id=trendyol.saticiid)
            service = ProductIntegrationService(api)
            response = service.create_products(items=product_data)
            log_record = LogRecords.objects.create(log_type="1", batch_id=str(response['batchRequestId']))
            return redirect('trendyol_engtegrasyon_islemleri')
        except Exception as e:
            return redirect('trendyol_engtegrasyon_islemleri')
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
        return redirect('trendyol_engtegrasyon_islemleri')

def trendyol_engtegrasyon_islemleri(request):
    context = {}
    reports = TrendyolReport.objects.all().order_by('-created_at')[:10]
    logs = list()
    for l1 in LogRecords.objects.filter(log_type=1)[:5]:
        logs.append(l1)
    for l2 in LogRecords.objects.filter(log_type=2)[:5]:
        logs.append(l2)
    for l3 in LogRecords.objects.filter(log_type=3)[:5]:
        logs.append(l3)
    context.update({'reports': reports, 'logs':logs,})
    return render(request, 'backend/yonetim/sayfalar/trendyol/entegrasyon_islemleri.html', context)

@login_required(login_url="/yonetim/giris-yap/")
def trendyol_update_function(request, products):
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
            UpdateHistory.objects.create(history_type="Trendyol Stok&Fiyat Güncelleme")
        except:
            result = 'failed'
        return result

@login_required(login_url="/yonetim/giris-yap/")
def trendyol_stok_fiyat_guncelle(request):
    context = {}
    log_records = LogRecords.objects.filter(log_type="2")
    if log_records.count() > 20:
        log_records = log_records[:20]
    context.update({
        'log_records': log_records
    })

    total_product = ProductVariant.objects.all().filter(is_publish_trendyol=True).count()
    messages.success(request, f"Toplam Ürün Sayısı: {total_product}")
    trendyol = Trendyol.objects.all().last()

    product_count = ProductVariant.objects.filter(is_publish_trendyol=True).count()
    i = 0
    while i / 1000 <= round(product_count / 1000):
        products = ProductVariant.objects.filter(is_publish_trendyol=True)[i:i + 1000]
        trendyol_update_function(request, products=products)
        i += 1000
    return redirect('trendyol_engtegrasyon_islemleri')