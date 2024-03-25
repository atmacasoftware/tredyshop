import decimal

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.db.models import Q, Min, Max

from adminpage.models import Banner
from categorymodel.models import *
from product.models import *


# Create your views here.

def katalog(request, categroy_slug, subcategory_slug):
    context = {}
    tum_kategoriler = SubCategory.objects.filter(maincategory_id=1)

    secili_kategori = get_object_or_404(SubCategory, slug=subcategory_slug)
    alt_kategorileri = SubBottomCategory.objects.filter(subcategory=secili_kategori)
    diger_kategorileri = SubCategory.objects.filter(maincategory_id=1).exclude(id=secili_kategori.id)

    product_list = []

    for kategori in alt_kategorileri:
        data = {
            'kategori_id': kategori.id,
            'kategori_adi': kategori.title,
            'product_count': Product.objects.filter(subbottomcategory_id=kategori.id).count(),
            'products': Product.objects.filter(subbottomcategory_id=kategori.id)[:8]
        }

        if data['product_count'] > 0:
            product_list.append(data)

    context.update({
        'tum_kategoriler': tum_kategoriler,
        'secili_kategori':secili_kategori,
        'alt_kategorileri':alt_kategorileri,
        'diger_kategorileri':diger_kategorileri,
        'product_list':product_list,
    })
    return render(request, 'frontend/v_2_0/sayfalar/store/katalog.html', context)

def store_page(request, categroy_slug=None, subcategory_slug=None, subbottomcategory_slug=None, brands_slug=None):
    context = {}

    brands = Brand.objects.all()
    products = None
    category_type = None
    minMaxPrice = None

    if categroy_slug != None and subcategory_slug != None and subbottomcategory_slug != None and brands_slug == None:
        category_s = MainCategory.objects.get(slug=categroy_slug)
        subcategory_s = SubCategory.objects.get(slug=subcategory_slug)
        subbottomcategory_s = SubBottomCategory.objects.get(slug=subbottomcategory_slug)
        colors = ProductVariant.objects.filter(product__subbottomcategory__slug=subbottomcategory_slug,
                                           color_id__isnull=False, quantity__gte=1).distinct().values(
            'color__name', 'color__id', 'color__code')
        sizes = ProductVariant.objects.filter(product__subbottomcategory__slug=subbottomcategory_slug,
                                          size_id__isnull=False, quantity__gte=1).distinct().values(
            'size__name', 'size__id', 'size__code')
        fabrictype = Product.objects.filter(subbottomcategory__slug=subbottomcategory_slug,
                                          fabrictype_id__isnull=False, quantity__gte=1).distinct().values(
            'fabrictype__name', 'fabrictype__id')
        category_type = "sub"
        products = Product.objects.filter(subbottomcategory__slug=subbottomcategory_slug, quantity__gte=1).distinct()[:16]

        product_count = Product.objects.filter(subbottomcategory__slug=subbottomcategory_slug,
                                                    quantity__gte=1).distinct().count()
        minMaxPrice = Product.objects.filter(subbottomcategory__slug=subbottomcategory_slug).distinct().aggregate(
            Min('price'),
            Max('price'))
        context.update(
            {'category_s': category_s, 'subcategory_s': subcategory_s, 'subbottomcategory_s': subbottomcategory_s,
             'products': products, 'colors': colors, 'product_count':product_count,
             'sizes': sizes, 'fabrictype':fabrictype})
    elif categroy_slug == None and subcategory_slug == None and brands_slug != None:
        brands_s = Brand.objects.get(slug=brands_slug)
        products = Product.objects.filter(brand__slug=brands_slug, quantity__gte=1)[:15]
        context.update({'brands_s': brands_s, 'products': products})

    context.update({'categroy_slug': categroy_slug, 'subcategory_slug': subcategory_slug,
                    'subbottomcategory_slug': subbottomcategory_slug, 'brands_slug': brands_slug,
                    'brands': brands, 'category_type': category_type,
                    'minMaxPrice': minMaxPrice})

    return render(request, 'frontend/v_2_0/sayfalar/store/katalog_filter.html', context)


def product_list(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    colors = request.GET.getlist('color[]')
    sizes = request.GET.getlist('sizes[]')
    fabrictype = request.GET.getlist('fabrictype[]')
    agegroup = request.GET.getlist('agegroup[]')
    discount = request.GET.getlist('discount[]')

    is_discount = False
    if len(discount) > 0:
        is_discount = True

    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']

    minPrice = decimal.Decimal(minPrice.replace(',', '.'))
    maxPrice = decimal.Decimal(maxPrice.replace(',', '.'))

    arrangement = request.GET['arrangement']

    order_type = '?'

    if arrangement == '1':
        order_type = '?'
    elif arrangement == '2':
        order_type = '-product__sell_count'
    elif arrangement == '3':
        order_type = 'product__price'
    elif arrangement == '4':
        order_type = '-product__price'
    elif arrangement == '5':
        order_type = '-product__create_at'
    elif arrangement == '5':
        order_type = 'product__create_at'

    data = []
    category = request.GET['category']
    subcategory = request.GET['subcategory']
    subbottomcategory = request.GET['subbottomcategory']
    brands = request.GET['brands']

    if category != 'None' and subcategory == 'None' and subbottomcategory == 'None' and brands == 'None':
        data = Product.objects.filter(category__slug=category, price__gte=minPrice,
                                         price__lte=maxPrice, quantity__gte=1, is_discountprice=is_discount).order_by(order_type)[
               offset:offset + limit]
        if len(colors) and colors != '' and colors != [] and colors != ['']:
            data = Product.objects.filter(category__slug=category, productvariant__color_id__in=colors, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
        if len(sizes) and sizes != '' and sizes != [] and sizes != ['']:
            data = Product.objects.filter(category__slug=category, productvariant__size_id__in=sizes, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
        if len(fabrictype) and fabrictype != '' and fabrictype != [] and fabrictype != ['']:
            data = Product.objects.filter(category__slug=category, fabrictype_id__in=fabrictype, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
        if len(agegroup) and agegroup != '' and agegroup != [] and agegroup != ['']:
            data = Product.objects.filter(category__slug=category, age_group=agegroup, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
    elif category != 'None' and subcategory != 'None' and subbottomcategory == 'None' and brands == 'None':

        data = Product.objects.filter(subcategory__slug=subcategory, price__gte=minPrice,
                                         price__lte=maxPrice, quantity__gte=1, is_discountprice=is_discount).order_by(order_type)[
               offset:offset + limit]
        if len(colors) and colors != '' and colors != [] and colors != ['']:
            data = Product.objects.filter(subcategory__slug=subcategory, productvariant__color_id__in=colors, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
        if len(sizes) and sizes != '' and sizes != [] and sizes != ['']:
            data = Product.objects.filter(subcategory__slug=subcategory, productvariant__size_id__in=sizes, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
        if len(fabrictype) and fabrictype != '' and fabrictype != [] and fabrictype != ['']:
            data = Product.objects.filter(subcategory__slug=subcategory, fabrictype_id__in=fabrictype, price__gte=minPrice,
                                             price__lte=maxPrice, _quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
        if len(agegroup) and agegroup != '' and agegroup != [] and agegroup != ['']:
            data = Product.objects.filter(_subcategory__slug=subcategory, age_group=agegroup, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
    elif category != 'None' and subcategory != 'None' and subbottomcategory != 'None' and brands == 'None':
        data = Product.objects.filter(subbottomcategory__slug=subbottomcategory,
                                         price__gte=minPrice,
                                         price__lte=maxPrice, quantity__gte=1, is_discountprice=is_discount).order_by(order_type)[
               offset:offset + limit]
        if len(colors) and colors != '' and colors != [] and colors != ['']:
            data = Product.objects.filter(subbottomcategory__slug=subbottomcategory, productvariant__color_id__in=colors, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
        if len(sizes) and sizes != '' and sizes != [] and sizes != ['']:
            data = Product.objects.filter(subbottomcategory__slug=subbottomcategory, productvariant__size_id__in=sizes, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
        if len(fabrictype) and fabrictype != '' and fabrictype != [] and fabrictype != ['']:
            data = Product.objects.filter(subbottomcategory__slug=subbottomcategory, fabrictype_id__in=fabrictype, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
        if len(agegroup) and agegroup != '' and agegroup != [] and agegroup != ['']:
            data = Product.objects.filter(subbottomcategory__slug=subbottomcategory, age_group=agegroup, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
    elif category == 'None' and subcategory == 'None' and subbottomcategory == 'None' and brands != 'None':
        data = Product.objects.filter(brand__slug=brands, price__gte=minPrice,
                                         price__lte=maxPrice,quantity__gte=1, is_discountprice=is_discount).order_by(order_type)[
               offset:offset + limit]
        if len(colors) and colors != '' and colors != [] and colors != ['']:
            data = Product.objects.filter(brand__slug=brands, productvariant__color_id__in=colors, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
        if len(sizes) and sizes != '' and sizes != [] and sizes != ['']:
            data = Product.objects.filter(brand__slug=brands, productvariant__size_id__in=sizes, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
        if len(fabrictype) and fabrictype != '' and fabrictype != [] and fabrictype != ['']:
            data = Product.objects.filter(brand__slug=brands, fabrictype_id__in=fabrictype, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
        if len(agegroup) and agegroup != '' and agegroup != [] and agegroup != ['']:
            data = Product.objects.filter(brand__slug=brands, age_group=agegroup, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
    t = render_to_string('frontend/v_2_0/sayfalar/store/__product_list.html', {'data': data})
    return JsonResponse({'data': t})


def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

    # return string
    return str1


def filter_data(request, categroy_slug=None, subcategoryslug=None, subottomcategoryslug=None, brandsslug=None):
    colors = request.GET.getlist('color[]')
    sizes = request.GET.getlist('size[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    fabrictype = request.GET.getlist('fabrictype[]')
    agegroup = request.GET.getlist('agegroup[]')
    discount = request.GET.getlist('discount[]')

    is_discount = False
    if len(discount) > 0:
        is_discount = True


    minPrice = decimal.Decimal(minPrice.replace(',', '.'))
    maxPrice = decimal.Decimal(maxPrice.replace(',', '.'))

    arrangement = request.GET.getlist('arrangement[]')
    arrangement = listToString(arrangement)

    order_type = '?'

    if arrangement == '1':
        order_type = '?'
    elif arrangement == '2':
        order_type = '-product__reviewrating__rating'
    elif arrangement == '3':
        order_type = 'product__reviewrating__rating'
    elif arrangement == '4':
        order_type = '-product__price'
    elif arrangement == '5':
        order_type = 'product__price'
    elif arrangement == '6':
        order_type = '-product__create_at'

    products = None
    if subcategoryslug != None and subottomcategoryslug == None and brandsslug == None:
        subcategory = SubCategory.objects.get(slug=subcategoryslug)
        products = Product.objects.filter(subcategory=subcategory,price__gte=minPrice,
                                             price__lte=maxPrice,quantity__gte=1, is_discountprice=is_discount).distinct().order_by(order_type)[:16]
        if len(colors) > 0:
            products = Product.objects.filter(subcategory=subcategory, productvariant__color_id__in=colors, price__gte=minPrice,
                                                 price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[:16]
        if len(sizes) > 0:
            products = Product.objects.filter(subcategory=subcategory,productvariant__size_id__in=sizes, price__gte=minPrice,
                                                 price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[:16]
        if len(fabrictype) > 0:
            products = Product.objects.filter(subcategory=subcategory,fabrictype_id__in=fabrictype, price__gte=minPrice,
                                                 price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[:16]
        if len(agegroup) > 0:
            products = Product.objects.filter(subcategory=subcategory, age_group=agegroup, price__gte=minPrice,
                                                 price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[:16]
    elif subcategoryslug != None and subottomcategoryslug != None and brandsslug == None:
        bottomcategory = SubBottomCategory.objects.get(slug=subottomcategoryslug)
        products = Product.objects.filter(subbottomcategory=bottomcategory,
                                             price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1, is_discountprice=is_discount).distinct().order_by(order_type)[:16]
        if len(colors) > 0:
            products = Product.objects.filter(subbottomcategory=bottomcategory,
                                                 productvariant__color_id__in=colors, price__gte=minPrice,
                                                 price__lte=maxPrice,quantity__gte=1).distinct().order_by(order_type)[:16]
        if len(sizes) > 0:
            products = Product.objects.filter(subbottomcategory=bottomcategory, productvariant__size_id__in=sizes,
                                                 price__gte=minPrice,
                                                 price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[
                       :16]

        if len(fabrictype) > 0:
            products = Product.objects.filter(subbottomcategory=bottomcategory, fabrictype_id__in=fabrictype,
                                                 price__gte=minPrice,
                                                 price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[
                       :16]
        if len(agegroup) > 0:
            products = Product.objects.filter(subbottomcategory=bottomcategory, age_group=agegroup,
                                                 price__gte=minPrice,
                                                 price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[
                       :16]
    elif subcategoryslug == None and subottomcategoryslug == None and brandsslug != None:
        brand = Brand.objects.get(slug=brandsslug)
        products = Product.objects.filter(brand=brand, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1, is_discountprice=is_discount).distinct()[:15]
        if len(colors) > 0:
            products = Product.objects.filter(brand=brand, productvariant__color_id__in=colors, price__gte=minPrice,
                                                 price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[:16]
        if len(sizes) > 0:
            products = Product.objects.filter(brand=brand, productvarian__size_id__in=sizes, price__gte=minPrice,
                                                 price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[:16]
        if len(fabrictype) > 0:
            products = Product.objects.filter(brand=brand, fabrictype_id__in=fabrictype, price__gte=minPrice,
                                                 price__lte=maxPrice,quantity__gte=1).distinct().order_by(order_type)[:16]
        if len(agegroup) > 0:
            products = Product.objects.filter(brand=brand, age_group=agegroup, price__gte=minPrice,
                                                 price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[:16]

    t = render_to_string('frontend/v_2_0/sayfalar/store/__product_list.html', {'data': products})
    return JsonResponse({'data': t})


def new_product(request):
    context = {}

    products = Product.objects.all().order_by("-create_at")

    page_number = 20

    page = request.GET.get('page', 1)
    paginator = Paginator(products, page_number)
    page_range = paginator.get_elided_page_range(page)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context.update({'products': products, 'page_obj': page_obj, 'page_range': page_range})

    return render(request, 'frontend/v_1_0/pages/new_product.html', context)


def most_sell_product(request):
    context = {}

    products = Product.objects.all().order_by("-sell_count")

    page_number = 20

    page = request.GET.get('page', 1)
    paginator = Paginator(products, page_number)
    page_range = paginator.get_elided_page_range(page)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context.update({'products': products, 'page_obj': page_obj, 'page_range': page_range})

    return render(request, 'frontend/v_1_0/pages/most_sell_product.html', context)


def most_discount_product(request):
    context = {}

    product = []
    allproducts = Product.objects.all()

    for p in allproducts:
        if p.is_discountprice == True:
            if 100 - ((p.discountprice * 100) / p.price) > 30:
                product.append(p)

    page_number = 20

    page = request.GET.get('page', 1)
    paginator = Paginator(product, page_number)
    page_range = paginator.get_elided_page_range(page)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context.update({'products': product, 'page_obj': page_obj, 'page_range': page_range})

    return render(request, 'frontend/v_1_0/pages/most_discount_price.html', context)


