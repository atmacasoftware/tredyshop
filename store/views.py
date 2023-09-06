import decimal

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.db.models import Q, Min, Max
from categorymodel.models import *
from product.models import *


# Create your views here.

def store_page(request, categroy_slug=None, subcategory_slug=None, subbottomcategory_slug=None, brands_slug=None):
    context = {}

    brands = Brand.objects.all().filter(brands__category__slug=categroy_slug)
    products = None
    descriptions = DescriptionList.objects.all()
    category_type = None

    minMaxPrice = None

    if categroy_slug != None and subcategory_slug == None and brands_slug == None:
        category_s = MainCategory.objects.get(slug=categroy_slug)
        products = Product.objects.filter(category__slug=categroy_slug)[:15]
        category_type = "main"
        minMaxPrice = products.aggregate(
            Min('price'),
            Max('price'))
        context.update({'category_s': category_s, 'products': products})
    elif categroy_slug != None and subcategory_slug != None and subbottomcategory_slug == None and brands_slug == None:
        category_s = MainCategory.objects.get(slug=categroy_slug)
        subcategory_s = SubCategory.objects.get(slug=subcategory_slug)
        products = Product.objects.filter(subcategory__slug=subcategory_slug).distinct()[:15]
        product_count = Product.objects.filter(subcategory__slug=subcategory_slug).count()
        minMaxPrice = Product.objects.filter(subcategory__slug=subcategory_slug).distinct().aggregate(
            Min('price'),
            Max('price'))
        colors = Variants.objects.filter(product__subcategory__slug=subcategory_slug,
                                         color_id__isnull=False).distinct().values(
            'color__name', 'color__id', 'color__code')
        sizes = Variants.objects.filter(product__subcategory__slug=subcategory_slug,
                                        size_id__isnull=False).distinct().values(
            'size__name', 'size__id', 'size__code')
        category_type = "sub"
        context.update(
            {'category_s': category_s, 'subcategory_s': subcategory_s, 'products': products, 'colors': colors,
             'sizes': sizes, 'product_count': product_count})
    elif categroy_slug != None and subcategory_slug != None and subbottomcategory_slug != None and brands_slug == None:
        category_s = MainCategory.objects.get(slug=categroy_slug)
        subcategory_s = SubCategory.objects.get(slug=subcategory_slug)
        subbottomcategory_s = SubBottomCategory.objects.get(slug=subbottomcategory_slug)
        colors = Variants.objects.filter(product__subbottomcategory__slug=subbottomcategory_slug,
                                         color_id__isnull=False).distinct().values(
            'color__name', 'color__id', 'color__code')
        sizes = Variants.objects.filter(product__subbottomcategory__slug=subbottomcategory_slug,
                                        size_id__isnull=False).distinct().values(
            'size__name', 'size__id', 'size__code')
        category_type = "sub"
        products = Product.objects.filter(subbottomcategory__slug=subbottomcategory_slug).distinct()[:15]
        minMaxPrice = Product.objects.filter(subbottomcategory__slug=subbottomcategory_slug).distinct().aggregate(
            Min('price'),
            Max('price'))
        context.update(
            {'category_s': category_s, 'subcategory_s': subcategory_s, 'subbottomcategory_s': subbottomcategory_s,
             'products': products, 'colors': colors,
             'sizes': sizes})
    elif categroy_slug == None and subcategory_slug == None and brands_slug != None:
        brands_s = Brand.objects.get(slug=brands_slug)
        products = Product.objects.filter(brand__slug=brands_slug)[:15]
        context.update({'brands_s': brands_s, 'products': products})

    context.update({'categroy_slug': categroy_slug, 'subcategory_slug': subcategory_slug,
                    'subbottomcategory_slug': subbottomcategory_slug, 'brands_slug': brands_slug,
                    'brands': brands, 'descriptions': descriptions, 'category_type': category_type,
                    'minMaxPrice': minMaxPrice})

    return render(request, 'frontend/pages/store.html', context)


def product_list(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    colors = request.GET.getlist('color[]')
    sizes = request.GET.getlist('sizes[]')

    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']

    minPrice = decimal.Decimal(minPrice.replace(',', '.'))
    maxPrice = decimal.Decimal(maxPrice.replace(',', '.'))

    arrangement = request.GET['arrangement']


    order_type = '?'

    if arrangement == '1':
        order_type = '?'
    elif arrangement == '2':
        order_type = '-sell_count'
    elif arrangement == '3':
        order_type = 'price'
    elif arrangement == '4':
        order_type = '-price'
    elif arrangement == '5':
        order_type = '-create_at'
    elif arrangement == '5':
        order_type = 'create_at'

    data = []
    category = request.GET['category']
    subcategory = request.GET['subcategory']
    subbottomcategory = request.GET['subbottomcategory']
    brands = request.GET['brands']

    if category != 'None' and subcategory == 'None' and subbottomcategory == 'None' and brands == 'None':
        data = Product.objects.filter(category__slug=category, price__gte=minPrice,
                                      price__lte=maxPrice).order_by(order_type)[offset:offset + limit]
        if len(colors) and colors != '' and colors != [] and colors != ['']:
            data = Product.objects.filter(variants__color_id__in=colors, price__gte=minPrice,
                                          price__lte=maxPrice).order_by(order_type)[offset:offset + limit]
        if len(sizes) and sizes != '' and sizes != [] and sizes != ['']:
            data = Product.objects.filter(variants__size_id__in=sizes, price__gte=minPrice,
                                          price__lte=maxPrice).order_by(order_type)[offset:offset + limit]
    elif category != 'None' and subcategory != 'None' and subbottomcategory == 'None' and brands == 'None':
        data = Product.objects.filter(subcategory__slug=subcategory, price__gte=minPrice,
                                      price__lte=maxPrice).order_by(order_type)[offset:offset + limit]
        if len(colors) and colors != '' and colors != [] and colors != ['']:
            data = Product.objects.filter(variants__color_id__in=colors, price__gte=minPrice,
                                          price__lte=maxPrice).order_by(order_type)[
                   offset:offset + limit]
        if len(sizes) and sizes != '' and sizes != [] and sizes != ['']:
            data = Product.objects.filter(variants__size_id__in=sizes, price__gte=minPrice,
                                          price__lte=maxPrice).order_by(order_type)[
                   offset:offset + limit]
    elif category != 'None' and subcategory != 'None' and subbottomcategory != 'None' and brands == 'None':
        data = Product.objects.filter(subbottomcategory__slug=subbottomcategory, price__gte=minPrice,
                                      price__lte=maxPrice).order_by(order_type)[offset:offset + limit]
        if len(colors) and colors != '' and colors != [] and colors != ['']:
            data = Product.objects.filter(variants__color_id__in=colors, price__gte=minPrice,
                                          price__lte=maxPrice).order_by(order_type)[
                   offset:offset + limit]
        if len(sizes) and sizes != '' and sizes != [] and sizes != ['']:
            data = Product.objects.filter(variants__size_id__in=sizes, price__gte=minPrice,
                                          price__lte=maxPrice).order_by(order_type)[
                   offset:offset + limit]

    elif category == 'None' and subcategory == 'None' and subbottomcategory == 'None' and brands != 'None':
        data = Product.objects.filter(brand__slug=brands, price__gte=minPrice,
                                      price__lte=maxPrice).order_by(order_type)[offset:offset + limit]
        if len(colors) and colors != '' and colors != [] and colors != ['']:
            data = Product.objects.filter(variants__color_id__in=colors, price__gte=minPrice,
                                          price__lte=maxPrice).order_by(order_type)[
                   offset:offset + limit]
        if len(sizes) and sizes != '' and sizes != [] and sizes != ['']:
            data = Product.objects.filter(variants__size_id__in=sizes, price__gte=minPrice,
                                          price__lte=maxPrice).order_by(order_type)[
                   offset:offset + limit]

    t = render_to_string('frontend/partials/ajax/product-list.html', {'data': data})
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
    sizes = request.GET.getlist('sizes[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']

    minPrice = decimal.Decimal(minPrice.replace(',', '.'))
    maxPrice = decimal.Decimal(maxPrice.replace(',', '.'))

    arrangement = request.GET.getlist('arrangement[]')
    arrangement = listToString(arrangement)

    order_type = '?'

    if arrangement == '1':
        order_type = '?'
    elif arrangement == '2':
        order_type = '-sell_count'
    elif arrangement == '3':
        order_type = 'price'
    elif arrangement == '4':
        order_type = '-price'
    elif arrangement == '5':
        order_type = '-create_at'
    elif arrangement == '5':
        order_type = 'create_at'

    products = None
    if subcategoryslug != None and subottomcategoryslug == None and brandsslug == None:
        subcategory = SubCategory.objects.get(slug=subcategoryslug)
        products = Product.objects.filter(subcategory=subcategory, price__gte=minPrice,
                                          price__lte=maxPrice).distinct().order_by(order_type)[:15]
        if len(colors) > 0:
            products = Product.objects.filter(variants__color_id__in=colors, price__gte=minPrice,
                                              price__lte=maxPrice).distinct().order_by(order_type)[:15]
        if len(sizes) > 0:
            products = Product.objects.filter(variants__size_id__in=sizes, price__gte=minPrice,
                                              price__lte=maxPrice).distinct().order_by(order_type)[:15]
    elif subcategoryslug != None and subottomcategoryslug != None and brandsslug == None:
        bottomcategory = SubBottomCategory.objects.get(slug=subottomcategoryslug)
        products = Product.objects.filter(subbottomcategory=bottomcategory, price__gte=minPrice,
                                          price__lte=maxPrice).distinct().order_by(order_type)[:15]
        if len(colors) > 0:
            products = Product.objects.filter(subbottomcategory=bottomcategory,
                                              variants__color_id__in=colors, price__gte=minPrice,
                                              price__lte=maxPrice).distinct().order_by(order_type)[:15]
        if len(sizes) > 0:
            products = Product.objects.filter(subbottomcategory=bottomcategory, variants__size_id__in=sizes,
                                              price__gte=minPrice,
                                              price__lte=maxPrice).distinct().order_by(order_type)[
                       :15]
    elif subcategoryslug == None and subottomcategoryslug == None and brandsslug != None:
        brand = Brand.objects.get(slug=brandsslug)
        products = Product.objects.filter(brand=brand, price__gte=minPrice,
                                          price__lte=maxPrice).distinct()[:15]
        if len(colors) > 0:
            products = Product.objects.filter(brand=brand, variants__color_id__in=colors, price__gte=minPrice,
                                              price__lte=maxPrice).distinct().order_by(order_type)[:15]
        if len(sizes) > 0:
            products = Product.objects.filter(brand=brand, variants__size_id__in=sizes, price__gte=minPrice,
                                              price__lte=maxPrice).distinct().order_by(order_type)[:15]

    t = render_to_string('frontend/partials/ajax/product-list.html', {'data': products})
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

    return render(request, 'frontend/pages/new_product.html', context)


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

    return render(request, 'frontend/pages/most_sell_product.html', context)


def under_50_price(request):
    context = {}

    products = Product.objects.filter(price__gte=0, price__lte=50)

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

    return render(request, 'frontend/pages/under_50_price.html', context)


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

    return render(request, 'frontend/pages/most_discount_price.html', context)
