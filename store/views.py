import decimal

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.db.models import Q, Min, Max

from adminpage.models import BannerOne, BannerTwo
from categorymodel.models import *
from product.models import *


# Create your views here.

def store_page(request, categroy_slug=None, subcategory_slug=None, subbottomcategory_slug=None, brands_slug=None):
    context = {}

    brands = Brand.objects.all()
    products = None
    category_type = None
    minMaxPrice = None

    if categroy_slug != None and subcategory_slug == None and brands_slug == None:
        category_s = MainCategory.objects.get(slug=categroy_slug)
        products = ApiProduct.objects.filter(category__slug=categroy_slug, dropshipping="Modaymış",
                                             quantity__gte=1).distinct()[:15]
        category_type = "main"
        minMaxPrice = products.aggregate(
            Min('price'),
            Max('price'))
        context.update({'category_s': category_s, 'products': products})
    elif categroy_slug != None and subcategory_slug != None and subbottomcategory_slug == None and brands_slug == None:
        category_s = MainCategory.objects.get(slug=categroy_slug)
        subcategory_s = SubCategory.objects.get(slug=subcategory_slug)
        products = ApiProduct.objects.filter(subcategory__slug=subcategory_slug,
                                             dropshipping="Modaymış", quantity__gte=1).distinct()[:15]
        product_count = ApiProduct.objects.filter(subcategory__slug=subcategory_slug, dropshipping="Modaymış").count()
        minMaxPrice = ApiProduct.objects.filter(subcategory__slug=subcategory_slug,
                                                dropshipping="Modaymış").distinct().aggregate(
            Min('price'),
            Max('price'))
        colors = ApiProduct.objects.filter(subcategory__slug=subcategory_slug,
                                           color_id__isnull=False, quantity__gte=1).distinct().values(
            'color__name', 'color__id', 'color__code')
        sizes = ApiProduct.objects.filter(subcategory__slug=subcategory_slug,
                                          size_id__isnull=False, quantity__gte=1).distinct().values(
            'size__name', 'size__id', 'size__code')
        category_type = "sub"
        context.update(
            {'category_s': category_s, 'subcategory_s': subcategory_s, 'products': products, 'colors': colors,
             'sizes': sizes, 'product_count': product_count})
    elif categroy_slug != None and subcategory_slug != None and subbottomcategory_slug != None and brands_slug == None:
        category_s = MainCategory.objects.get(slug=categroy_slug)
        subcategory_s = SubCategory.objects.get(slug=subcategory_slug)
        subbottomcategory_s = SubBottomCategory.objects.get(slug=subbottomcategory_slug)
        colors = ApiProduct.objects.filter(subbottomcategory__slug=subbottomcategory_slug,
                                           color_id__isnull=False, quantity__gte=1).distinct().values(
            'color__name', 'color__id', 'color__code')
        sizes = ApiProduct.objects.filter(subbottomcategory__slug=subbottomcategory_slug,
                                          size_id__isnull=False, quantity__gte=1).distinct().values(
            'size__name', 'size__id', 'size__code')
        category_type = "sub"
        products = ApiProduct.objects.filter(subbottomcategory__slug=subbottomcategory_slug,
                                             dropshipping="Modaymış", quantity__gte=1).distinct()[:15]
        minMaxPrice = ApiProduct.objects.filter(subbottomcategory__slug=subbottomcategory_slug,
                                                dropshipping="Modaymış").distinct().aggregate(
            Min('price'),
            Max('price'))
        context.update(
            {'category_s': category_s, 'subcategory_s': subcategory_s, 'subbottomcategory_s': subbottomcategory_s,
             'products': products, 'colors': colors,
             'sizes': sizes})
    elif categroy_slug == None and subcategory_slug == None and brands_slug != None:
        brands_s = Brand.objects.get(slug=brands_slug)
        products = ApiProduct.objects.filter(brand__slug=brands_slug, dropshipping="Modaymış", quantity__gte=1)[:15]
        context.update({'brands_s': brands_s, 'products': products})

    context.update({'categroy_slug': categroy_slug, 'subcategory_slug': subcategory_slug,
                    'subbottomcategory_slug': subbottomcategory_slug, 'brands_slug': brands_slug,
                    'brands': brands, 'category_type': category_type,
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
        data = ApiProduct.objects.filter(category__slug=category, dropshipping="Modaymış", price__gte=minPrice,
                                         price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
               offset:offset + limit]
        if len(colors) and colors != '' and colors != [] and colors != ['']:
            data = ApiProduct.objects.filter(color_id__in=colors, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
        if len(sizes) and sizes != '' and sizes != [] and sizes != ['']:
            data = ApiProduct.objects.filter(size_id__in=sizes, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
    elif category != 'None' and subcategory != 'None' and subbottomcategory == 'None' and brands == 'None':
        data = ApiProduct.objects.filter(subcategory__slug=subcategory, dropshipping="Modaymış", price__gte=minPrice,
                                         price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
               offset:offset + limit]
        if len(colors) and colors != '' and colors != [] and colors != ['']:
            data = ApiProduct.objects.filter(color_id__in=colors, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
        if len(sizes) and sizes != '' and sizes != [] and sizes != ['']:
            data = ApiProduct.objects.filter(size_id__in=sizes, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
    elif category != 'None' and subcategory != 'None' and subbottomcategory != 'None' and brands == 'None':
        data = ApiProduct.objects.filter(subbottomcategory__slug=subbottomcategory, dropshipping="Modaymış",
                                         price__gte=minPrice,
                                         price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
               offset:offset + limit]
        if len(colors) and colors != '' and colors != [] and colors != ['']:
            data = ApiProduct.objects.filter(color_id__in=colors, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
        if len(sizes) and sizes != '' and sizes != [] and sizes != ['']:
            data = ApiProduct.objects.filter(size_id__in=sizes, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]

    elif category == 'None' and subcategory == 'None' and subbottomcategory == 'None' and brands != 'None':
        data = ApiProduct.objects.filter(brand__slug=brands, dropshipping="Modaymış", price__gte=minPrice,
                                         price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
               offset:offset + limit]
        if len(colors) and colors != '' and colors != [] and colors != ['']:
            data = ApiProduct.objects.filter(color_id__in=colors, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
                   offset:offset + limit]
        if len(sizes) and sizes != '' and sizes != [] and sizes != ['']:
            data = ApiProduct.objects.filter(size_id__in=sizes, price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).order_by(order_type)[
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
        products = ApiProduct.objects.filter(subcategory=subcategory, dropshipping="Modaymış", price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[:15]
        if len(colors) > 0:
            products = ApiProduct.objects.filter(color_id__in=colors, price__gte=minPrice,
                                                 price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[:15]
        if len(sizes) > 0:
            products = ApiProduct.objects.filter(size_id__in=sizes, price__gte=minPrice,
                                                 price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[:15]
    elif subcategoryslug != None and subottomcategoryslug != None and brandsslug == None:
        bottomcategory = SubBottomCategory.objects.get(slug=subottomcategoryslug)
        products = ApiProduct.objects.filter(subbottomcategory=bottomcategory, dropshipping="Modaymış",
                                             price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[:15]
        if len(colors) > 0:
            products = ApiProduct.objects.filter(subbottomcategory=bottomcategory,
                                                 color_id__in=colors, price__gte=minPrice,
                                                 price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[:15]
        if len(sizes) > 0:
            products = ApiProduct.objects.filter(subbottomcategory=bottomcategory, size_id__in=sizes,
                                                 price__gte=minPrice,
                                                 price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[
                       :15]
    elif subcategoryslug == None and subottomcategoryslug == None and brandsslug != None:
        brand = Brand.objects.get(slug=brandsslug)
        products = ApiProduct.objects.filter(brand=brand, dropshipping="Modaymış", price__gte=minPrice,
                                             price__lte=maxPrice, quantity__gte=1).distinct()[:15]
        if len(colors) > 0:
            products = ApiProduct.objects.filter(brand=brand, color_id__in=colors, price__gte=minPrice,
                                                 price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[:15]
        if len(sizes) > 0:
            products = ApiProduct.objects.filter(brand=brand, size_id__in=sizes, price__gte=minPrice,
                                                 price__lte=maxPrice, quantity__gte=1).distinct().order_by(order_type)[:15]

    t = render_to_string('frontend/partials/ajax/product-list.html', {'data': products})
    return JsonResponse({'data': t})


def new_product(request):
    context = {}

    products = ApiProduct.objects.all().filter(dropshipping="Modaymış").order_by("-create_at")

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

    products = ApiProduct.objects.all().filter(dropshipping="Modaymış").order_by("-sell_count")

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


def banner_one(request):
    context = {}
    banner_one = BannerOne.objects.all().last()
    products = []
    product_count = None
    if banner_one.banner_type == 'Belirli Tutar Altı':
        products = ApiProduct.objects.filter(price__gte=banner_one.banner_minprice,
                                             price__lte=banner_one.banner_maxprice, dropshipping="Modaymış")
        product_count = products.count()
    elif banner_one.banner_type == 'İndirimli Ürünler':
        allproducts = ApiProduct.objects.all().filter(dropshipping="Modaymış")

        for p in allproducts:
            if p.is_discountprice == True:
                if 100 - ((p.discountprice * 100) / p.price) > banner_one.banner_discountrate:
                    products.append(p)
        product_count = len(products)

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

    context.update({'products': products, 'page_obj': page_obj, 'page_range': page_range, 'banner_one': banner_one,
                    'product_count': product_count})

    return render(request, 'frontend/pages/banner_one.html', context)


def banner_two(request):
    context = {}
    banner_two = BannerTwo.objects.all().last()
    products = []
    product_count = None
    if banner_two.banner_type == 'Belirli Tutar Altı':
        products = ApiProduct.objects.filter(price__gte=banner_two.banner_minprice,
                                             price__lte=banner_two.banner_maxprice, dropshipping="Modaymış")
        product_count = products.count()

    elif banner_two.banner_type == 'İndirimli Ürünler':
        allproducts = ApiProduct.objects.all().filter(dropshipping="Modaymış")

        for p in allproducts:
            if p.is_discountprice == True:
                if 100 - ((p.discountprice * 100) / p.price) > banner_two.banner_discountrate:
                    products.append(p)

        product_count = len(products)

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

    context.update({'products': products, 'page_obj': page_obj, 'page_range': page_range, 'banner_two': banner_two,
                    'product_count': product_count})

    return render(request, 'frontend/pages/banner_two.html', context)


def most_discount_product(request):
    context = {}

    product = []
    allproducts = ApiProduct.objects.all().filter(dropshipping="Modaymış")

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
