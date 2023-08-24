import json

from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from adminpage.custom import exportExcel, exportPdf
from adminpage.forms import *
from categorymodel.models import SubCategory, SubBottomCategory, MainCategory
from ecommerce import settings
from product.models import Product, Variants, Images
from product.read_xml import modaymissaveXML2db, updateModaymisSaveXML2db, updateTahtakaleSaveXML2db, \
    tahtakaleSaveXML2db
# Create your views here.
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
import requests
from user_accounts.models import User


def admin_login(request):
    try:
        if request.user.is_authenticated:
            messages.success(request, 'Giriş yapıldı')
            return redirect('mainpage')
        if 'loginBtn' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            remember = request.POST.get('remember_me')
            user_obj = User.objects.filter(email=email)
            if not user_obj.exists():
                messages.error(request, 'Bu kullanıcı mevcut değil.')
                return redirect('admin_login')
            user_obj = authenticate(email=email, password=password)
            if user_obj is not None:
                if User.objects.get(email=email, is_superuser=True):
                    auth_login(request, user_obj)
                    if not remember:
                        request.session.set_expiry(18000)
                    messages.success(request,
                                     f'Hoşgeldin {request.user.get_full_name()}.')
                    return redirect('admin_mainpage')
    except Exception as e:
        return redirect('admin_login')

    return render(request, 'backend/adminpage/pages/login.html')


@login_required(login_url="/yonetim/giris-yap/")
def user_info(request):
    if 'updateBtn' in request.POST:
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')

        try:
            user = get_object_or_404(User, id=request.user.id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.mobile = mobile
            user.save()
            messages.success(request,
                             'Hesap bilgileriniz başarıyla güncellenmiştir.')
            return redirect('user_info')
        except:
            messages.warning(request,
                             'Bir hata meydana geldi!')
            return redirect('user_info')
    return render(request, 'backend/adminpage/pages/user_info.html')


@login_required(login_url="/yonetim/giris-yap/")
def change_password(request):
    if 'changePasswordBtn' in request.POST:
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        re_password = request.POST.get('re_password')

        if new_password == re_password:
            flag = check_password(current_password, request.user.password)
            if flag:
                haspass = make_password(new_password)
                request.user.password = haspass
                request.user.save()
                messages.success(request, 'Şifreniz başarıyla değiştirildi.')
                return redirect('admin_change_password')
        else:
            messages.warning(request, 'Yeni şifre ve şifre tekrar aynı olmalıdır.')
            return redirect('admin_change_password')
    return render(request, 'backend/adminpage/pages/change_password.html')


@login_required(login_url="/yonetim/giris-yap/")
def mainpage(request):
    return render(request, 'backend/adminpage/pages/mainpage.html')


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye1(request):
    context = {}
    category = MainCategory.objects.all()
    subcategory = SubCategory.objects.all()
    form = MainCategoryForm(data=request.POST or None, files=request.FILES or None)
    context.update({
        'category': category,
        'form': form,
        'subcategory': subcategory
    })

    if 'addBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori eklendi.')
            return redirect("kategoriler_seviye1")

    return render(request, 'backend/adminpage/pages/kategoriler_seviye1.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye1_guncelle(request, id):
    context = {}
    category = MainCategory.objects.get(id=id)
    form = MainCategoryForm(instance=category, data=request.POST or None, files=request.FILES or None)
    context.update({
        'category': category,
        'form': form,
    })

    if 'updateBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori güncellendi.')
            return redirect("kategoriler_seviye1_guncelle", id)

    return render(request, 'backend/adminpage/pages/kategoriler_seviye1_guncelle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye1_sil(request, id):
    context = {}
    category = MainCategory.objects.get(id=id)
    category_title = category.title
    category.delete()
    messages.success(request, f'{category_title} ve ona bağlı alt kategorilerde silindi.')
    return redirect("kategoriler_seviye1")


def kategoriler_seviye1_export_excel(request):
    columns = ['ID', 'Başlık', 'Sırası',
               'Kategori Numarası', 'Oluşturulma Tarihi']

    rows = MainCategory.objects.all().values_list('id', 'title', 'order', 'category_no', 'created_at')
    return exportExcel('Kategoriler', 'Kategoriler', columns=columns, rows=rows)


def kategoriler_seviye1_export_pdf(request):
    columns = ["ID", "Başlık", "Kategori Sırası", "Kategori Numarası", "Oluşturulma Tarihi"]
    rows = []
    row = MainCategory.objects.all().values_list('id', 'title', 'order', 'category_no', 'created_at')
    for r in row:
        rows.append(r)

    dict = {
        'columns': columns,
        'rows': rows
    }

    pdf = exportPdf(f"{str(settings.BASE_DIR)}" + "/templates/backend/adminpage/partials/table_pdf.html", dict)
    response = HttpResponse(pdf, content_type='application/pdf')
    content = f'attachment; filename=Kategoriler' + '.pdf'
    response['Content-Disposition'] = content

    return response


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye1_hepsini_sil(request):
    context = {}
    category = MainCategory.objects.all().delete()
    messages.success(request, 'Tüm ana kategoriler ve bağlı olan alt kategorilerde silindi.')
    return redirect("kategoriler_seviye1")


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_secilileri_sil(request):
    categoy1_id = request.GET.getlist('seviye1-category[]')

    MainCategory.objects.filter(id__in=categoy1_id).delete()
    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye2(request, slug):
    context = {}
    maincategory = MainCategory.objects.get(slug=slug)
    subcategory = SubCategory.objects.filter(maincategory__slug=slug)
    subbottomcategory = SubBottomCategory.objects.all()
    form = SubCategoryForm(data=request.POST or None, files=request.FILES or None)
    context.update({
        'maincategory': maincategory,
        'subcategory': subcategory,
        'form': form,
        'subbottomcategory': subbottomcategory
    })

    if 'addBtn' in request.POST:
        if form.is_valid():
            data = form.save(commit=False)
            data.maincategory = maincategory
            data.save()
            messages.success(request, 'Kategori başarıyla eklendi.')
            return redirect("kategoriler_seviye2")

    return render(request, 'backend/adminpage/pages/kategoriler_seviye2.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye2_guncelle(request, id):
    context = {}
    category = SubCategory.objects.get(id=id)
    form = SubCategoryForm(instance=category, data=request.POST or None, files=request.FILES or None)
    context.update({
        'category': category,
        'form': form,
    })

    if 'updateBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori güncellendi.')
            return redirect("kategoriler_seviye2_guncelle", id)

    return render(request, 'backend/adminpage/pages/kategoriler_seviye2_guncelle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye2_sil(request, id):
    context = {}
    category = SubCategory.objects.get(id=id)
    category_title = category.title
    category.delete()
    messages.success(request, f'{category_title} ve ona bağlı alt kategorilerde silindi.')
    return redirect("kategoriler_seviye2")


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye2_hepsini_sil(request, slug):
    context = {}
    category = SubCategory.objects.filter(maincategory__slug=slug).delete()
    messages.success(request, 'Tüm ana kategoriler ve bağlı olan alt kategorilerde silindi.')
    return redirect("kategoriler_seviye2")


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye2_tum_sil(request):
    context = {}
    category = SubCategory.objects.all().delete()
    messages.success(request, 'Tüm alt kategoriler silindi.')
    return redirect("kategoriler_seviye2")


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler2_secilileri_sil(request):
    categoy_id = request.GET.getlist('seviye2-category[]')
    SubCategory.objects.filter(id__in=categoy_id).delete()
    data = 'success'
    return JsonResponse(data=data, safe=False)


def kategoriler_seviye2_export_excel(request, slug):
    columns = ['ID', 'Üst Kategorisi', 'Başlık',
               'Kategori Numarası', 'Oluşturulma Tarihi']

    seviye1_category = MainCategory.objects.get(slug=slug)
    rows = SubCategory.objects.filter(maincategory=seviye1_category).values_list('id', 'maincategory__title', 'title',
                                                                                 'category_no', 'created_at')
    return exportExcel(f'{slug}-alt-kategorileri', 'Kategoriler', columns=columns, rows=rows)


def kategoriler_seviye2_hepsi_export_excel(request):
    columns = ['ID', 'Üst Kategorisi', 'Başlık',
               'Kategori Numarası', 'Oluşturulma Tarihi']

    rows = SubCategory.objects.all().values_list('id', 'maincategory__title', 'title', 'category_no', 'created_at')
    return exportExcel('tüm-alt-kategorileri', 'Kategoriler', columns=columns, rows=rows)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye3(request, main_slug, sub_slug):
    context = {}
    maincategory = MainCategory.objects.get(slug=main_slug)
    subcategory = SubCategory.objects.get(slug=sub_slug)
    subbottomcategory = SubBottomCategory.objects.filter(subcategory__slug=sub_slug)
    form = SubBottomCategoryForm(data=request.POST or None, files=request.FILES or None)
    context.update({
        'maincategory': maincategory,
        'subcategory': subcategory,
        'form': form,
        'subbottomcategory': subbottomcategory
    })

    if 'addBtn' in request.POST:
        if form.is_valid():
            data = form.save(commit=False)
            data.maincategory = maincategory
            data.subcategory = subcategory
            data.save()
            messages.success(request, 'Kategori başarıyla eklendi.')
            return redirect("kategoriler_seviye3", main_slug, sub_slug)

    return render(request, 'backend/adminpage/pages/kategoriler_seviye3.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye3_guncelle(request, main_slug, sub_slug, id):
    context = {}
    category = SubCategory.objects.get(id=id)
    form = SubBottomCategoryForm(instance=category, data=request.POST or None, files=request.FILES or None)
    context.update({
        'category': category,
        'form': form,
    })

    if 'updateBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori güncellendi.')
            return redirect("kategoriler_seviye3_guncelle", main_slug, sub_slug, id)

    return render(request, 'backend/adminpage/pages/kategoriler_seviye3_guncelle.html', context)

def kategoriler_seviye3_export_excel(request, slug):
    columns = ['ID', 'En Üst Kategorisi', 'Üst Kategorisi', 'Başlık', 'Oluşturulma Tarihi']

    seviye2_category = SubCategory.objects.get(slug=slug)
    rows = SubBottomCategory.objects.filter(subcategory=seviye2_category).values_list('id', 'maincategory__title',
                                                                                      'subcategory__title', 'title',
                                                                                      'created_at')
    return exportExcel(f'{slug}-alt-kategorileri', 'Kategoriler', columns=columns, rows=rows)


def kategoriler_seviye3_hepsi_export_excel(request):
    columns = ['ID', 'En Üst Kategorisi', 'Üst Kategorisi', 'Başlık', 'Oluşturulma Tarihi']

    rows = SubBottomCategory.objects.all().values_list('id', 'maincategory__title', 'subcategory__title', 'title',
                                                       'created_at')
    return exportExcel('tüm-alt-kategorileri', 'Kategoriler', columns=columns, rows=rows)

@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye3_sil(request, main_slug, sub_slug, id):
    context = {}
    category = SubBottomCategory.objects.get(id=id)
    category.delete()
    messages.success(request, 'Kategori silindi.')
    return redirect("kategoriler_seviye3", main_slug, sub_slug)

@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye3_hepsini_sil(request, main_slug, sub_slug):
    context = {}
    category = SubBottomCategory.objects.filter(subcategory__slug=sub_slug).delete()
    messages.success(request, 'Kategori silindi.')
    return redirect("kategoriler_seviye3", main_slug, sub_slug)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye3_tum_sil(request, main_slug, sub_slug):
    context = {}
    category = SubBottomCategory.objects.all().delete()
    messages.success(request, 'Tüm alt kategoriler silindi.')
    return redirect("kategoriler_seviye3", main_slug, sub_slug)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler3_secilileri_sil(request):
    categoy_id = request.GET.getlist('seviye3-category[]')
    SubBottomCategory.objects.filter(id__in=categoy_id).delete()
    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def products(request):
    return render(request, 'backend/adminpage/pages/products.html')


@login_required(login_url="/yonetim/giris-yap/")
def tahtakale_product(request):
    return render(request, "backend/adminpage/pages/tahtakale.html")


@login_required(login_url="/yonetim/giris-yap/")
def tahtakale_product_load(request):
    try:
        tahtakaleSaveXML2db()
        messages.success(request, 'Veriler yüklendi!')
        return redirect("tahtakale_product")
    except:
        return redirect("tahtakale_product")


@login_required(login_url="/yonetim/giris-yap/")
def tahtakale_product_update(request):
    try:
        updateTahtakaleSaveXML2db()
        messages.success(request, 'Veriler güncelledi!')
        return redirect("tahtakale_product")
    except:
        return redirect("tahtakale_product")


@login_required(login_url="/yonetim/giris-yap/")
def haydigiy_product(request):
    return render(request, "backend/adminpage/pages/haydigiy.html")


@login_required(login_url="/yonetim/giris-yap/")
def haydigiy_product_load(request):
    try:
        modaymissaveXML2db()()
        messages.success(request, 'Veriler yüklendi!')
        return redirect("haydigiy_product")
    except Exception as e:
        return redirect("haydigiy_product")


@login_required(login_url="/yonetim/giris-yap/")
def haydigiy_product_update(request):
    try:
        tahtakaleSaveXML2db()
        messages.success(request, 'Veriler güncelledi!')
        return redirect("haydigiy_product")
    except:
        return redirect("haydigiy_product")


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_hesap_bilgileri_ekle(request):
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
                return redirect("trendyol_hesap_bilgileri_ekle")
    else:
        form = TrendyolAddForm(data=request.POST, files=request.FILES)
        context.update({'form': form})
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'Trendyol hesap bilgileri başarıyla eklendi!')
                return redirect("trendyol_hesap_bilgileri_ekle")

    return render(request, 'backend/adminpage/pages/trendyol/trendyol.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_add_product(request):
    return render(request, 'backend/adminpage/pages/trendyol/urun_girisi.html')


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_add_product_giyim(request):
    return render(request, 'backend/adminpage/pages/trendyol/urun_girisi_giyim.html')


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_add_product_giyim_category1(request, category_no):
    context = {}
    subcategory = SubCategory.objects.get(category_no=category_no)
    categories = SubBottomCategory.objects.filter(subcategory__category_no=category_no)
    context.update({'categories': categories, 'subcategory': subcategory})
    return render(request, 'backend/adminpage/pages/trendyol/urun_girisi_giyim_category1.html', context)


def productSendTrendyol(request, product_data):
    trendyol = Trendyol.objects.all().last()
    api_key = trendyol.apikey
    trendyol_api_url = f"https://api.trendyol.com/sapigw/suppliers/{trendyol.saticiid}/v2/products"
    headers = {
        "Authorization": "Basic " + trendyol.token,
        "User-Agent": f"{trendyol.saticiid} - SelfIntegration",
        "Content-Type": "application/json",
    }
    response = requests.request('POST', trendyol_api_url, headers=headers,
                                data=json.dumps(product_data).encode('utf-8'))

    return response


def trendyolProductData(barcode, title, model_code, brandid, categoryid, quantity, stock_code, desi, description,
                        list_price, sale_price, vatRate, cargoid, shipmentid, returningid, delivery_duration, images,
                        data_attributes):
    data = {
        "barcode": str(barcode),
        "title": str(title),
        "productMainId": str(model_code),
        "brandId": int(brandid),
        "categoryId": int(categoryid),
        "quantity": int(quantity),
        "stockCode": str(stock_code),
        "dimensionalWeight": desi,
        "description": description,
        "currencyType": "TRY",
        "listPrice": float(list_price),
        "salePrice": float(sale_price),
        "vatRate": int(vatRate),
        "cargoCompanyId": int(cargoid),
        "shipmentAddressId": int(shipmentid),
        "returningAddressId": int(returningid),
        "deliveryDuration": int(delivery_duration),
        "images": images,
        "attributes": data_attributes
    }

    return data


def callingProduct(category, title):
    products = Product.objects.filter(subbottomcategory=category, title__icontains=title)
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


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_add_product_giyim_send_trendyol(request, id):
    context = {}
    trendyol = Trendyol.objects.all().last()
    category = SubBottomCategory.objects.get(id=id)
    context.update({'category': category})
    product_data = {}
    items = []
    data_attributes = []
    deneme = callingProduct(category, 'ceket')
    trendyol_category = None

    attributes = []

    if 'sendTrendyol' in request.POST:
        category_title = request.POST.get('category_title')
        product_title = request.POST.get('product_title')

        trendyol_category = trendyolCategory(category_title)

        ##Attributes
        product_attributes = trendyolAttributes(trendyol_category)

        ##Calling Product
        products = callingProduct(category, product_title)

        for a in product_attributes['categoryAttributes']:
            attributes.append(a)

        for p in products:
            product_variants = Variants.objects.filter(product=p)
            if product_variants.count() > 0:
                product_images = Images.objects.filter(product=p)
                images = []
                for i in product_images:
                    images.append(
                        {'url': i.image_url}
                    )

                for v in product_variants:
                    attribute_id = None
                    beden = None
                    for a in attributes:
                        if a['attribute']['name'] == 'Beden':
                            attribute_id = a['attribute']['id']
                            for s in a['attributeValues']:
                                if v.size.name == s['name']:
                                    beden = s['id']

                    if beden != None:
                        if v.color is not None:
                            data_attributes = [
                                {
                                    "attributeId": 338,
                                    "attributeValueId": beden
                                },
                                {
                                    "attributeId": 343,
                                    "attributeValueId": 4295
                                },
                                {
                                    "attributeId": 346,
                                    "attributeValueId": 4293
                                },
                                {
                                    "attributeId": 47,
                                    "customAttributeValue": str(v.color.name)
                                },
                            ]
                        else:
                            data_attributes = [
                                {
                                    "attributeId": 338,
                                    "attributeValueId": beden
                                },
                                {
                                    "attributeId": 343,
                                    "attributeValueId": 4295
                                },
                                {
                                    "attributeId": 346,
                                    "attributeValueId": 4293
                                },

                            ]
                    if beden == None:
                        if v.color is not None:
                            data_attributes = [
                                {
                                    "attributeId": 343,
                                    "attributeValueId": 4295
                                },
                                {
                                    "attributeId": 346,
                                    "attributeValueId": 4293
                                },
                                {
                                    "attributeId": 47,
                                    "customAttributeValue": str(v.color.name)
                                },
                            ]
                        else:
                            data_attributes = [
                                {
                                    "attributeId": 343,
                                    "attributeValueId": 4295
                                },
                                {
                                    "attributeId": 346,
                                    "attributeValueId": 4293
                                },
                            ]
                    items.append(
                        trendyolProductData(barcode=v.gtin, title=v.title, model_code=p.stock_code, brandid=996771,
                                            categoryid=trendyol_category, quantity=v.quantity, stock_code=v.sku, desi=1,
                                            list_price=p.trendyol_price, sale_price=p.trendyol_price, cargoid=10,
                                            description=p.detail, vatRate=10, shipmentid=trendyol.sevkiyatadresid_1,
                                            returningid=trendyol.iadeadresid_2, delivery_duration=4, images=images,
                                            data_attributes=data_attributes))

        product_data = items
        response = productSendTrendyol(request, product_data)
        if response.status_code == 200:
            messages.success(request, "Ürünler başarıyla Trendyola aktarılmıştır.")
        else:
            messages.error(request, f'Error Code:{response.status_code} - {response.json()}')
        return redirect('trendyol_add_product_giyim_send_trendyol', id)
    return render(request, 'backend/adminpage/pages/trendyol/urun_girisi_giyim_send_trendyol.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_update_price_stok(request):
    if 'updateBtn' in request.POST:
        products = Product.objects.filter(is_publish_trendyol=True)

        trendyol = Trendyol.objects.all().last()
        api_key = trendyol.apikey
        trendyol_api_url = f"https://api.trendyol.com/sapigw/suppliers/{trendyol.saticiid}/products/price-and-inventory"
        headers = {
            "Authorization": "Basic " + api_key,
            "Content-Type": "application/json",
        }

        if products.count() > 0:
            for p in products:
                variants = Variants.objects.filter(product=p)
                for v in variants:
                    data = {
                        "items": [
                            {
                                "barcode": v.gtin,
                                "quantity": v.quantity,
                                "salePrice": float(p.trendyol_price),
                                "listPrice": float(p.trendyol_price)
                            }
                        ]
                    }
                    response = requests.put(trendyol_api_url, headers=headers, json=data)
            return redirect('trendyol_update_price_stok')
        return redirect('trendyol_update_price_stok')
    return render(request, 'backend/adminpage/pages/trendyol/stok_fiyat_guncelleme.html')


@login_required(login_url="/yonetim/giris-yap/")
def kesilen_fatura_ekle(request):
    context = {}
    form = IssuedInvoicesAddForm(data=request.POST, files=request.FILES)
    context.update({'form': form})
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Fatura başarıyla eklendi!')
            return redirect("kesilen_fatura_ekle")
    return render(request, 'backend/adminpage/pages/kesilen_fatura_ekle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kesilen_faturalar(request):
    context = {}
    faturalar = IssuedInvoices.objects.all()
    context.update({
        'faturalar': faturalar
    })
    return render(request, 'backend/adminpage/pages/kesilen_faturalar.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def update_kesilen_fatura(request, id):
    context = {}
    fatura = IssuedInvoices.objects.get(id=id)
    form = IssuedInvoicesUpdateForm(instance=fatura, data=request.POST or None,
                                    files=request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Fatura başarıyla güncellendi!')
            return redirect("update_kesilen_fatura", id)

    context.update({
        'fatura': fatura,
        'form': form
    })
    return render(request, 'backend/adminpage/pages/kesilen_fatura_guncelle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def delete_kesilen_fatura(request, id):
    fatura = IssuedInvoices.objects.get(id=id)
    fatura.delete()
    messages.success(request, 'Fatura başarıyla silindi!')
    return redirect('kesilen_faturalar')


def kesilen_faturalar_export_excel(request):
    columns = ['Ad/Soyad/Ünvan', 'Vergi Numarası', 'Vergi Dairesi', 'Yıl', 'Ay', 'KDV Hariç Tutar (TL)',
               'KDV Oranı', 'Fatura Düzenlenme Tarihi']

    rows = IssuedInvoices.objects.all().values_list('name', 'tax_number', 'tax_administration', 'year', 'month',
                                                    'price', 'tax_rate', 'edited_date')

    return exportExcel('kesilen-faturalar', 'Ödemeler', columns=columns, rows=rows)


@login_required(login_url="/yonetim/giris-yap/")
def alinan_fatura_ekle(request):
    context = {}
    form = InvoicesReceivedAddForm(data=request.POST, files=request.FILES)
    context.update({'form': form})
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Fatura başarıyla eklendi!')
            return redirect("alinan_fatura_ekle")
    return render(request, 'backend/adminpage/pages/alinan_fatura_ekle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def alinan_faturalar(request):
    context = {}
    faturalar = InvoicesReceived.objects.all()
    context.update({
        'faturalar': faturalar
    })
    return render(request, 'backend/adminpage/pages/alinan_faturalar.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def update_alinan_fatura(request, id):
    context = {}
    fatura = InvoicesReceived.objects.get(id=id)
    form = InvoicesReceivedUpdateForm(instance=fatura, data=request.POST or None,
                                      files=request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Fatura başarıyla güncellendi!')
            return redirect("update_alinan_fatura", id)

    context.update({
        'fatura': fatura,
        'form': form
    })
    return render(request, 'backend/adminpage/pages/alinan_fatura_guncelle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def delete_alinan_fatura(request, id):
    fatura = InvoicesReceived.objects.get(id=id)
    fatura.delete()
    messages.success(request, 'Fatura başarıyla silindi!')
    return redirect('alinan_faturalar')


def alinan_faturalar_export_excel(request):
    columns = ['Yıl', 'Ay', 'KDV Hariç Tutar (TL)',
               'KDV Oranı', 'Oluşturulma Tarihi']

    rows = InvoicesReceived.objects.all().values_list('year', 'month', 'price', 'tax_rate', 'created_at')
    return exportExcel('alinan-faturalar', 'Ödemeler', columns=columns, rows=rows)
