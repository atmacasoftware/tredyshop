from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from categorymodel.models import *
from product.models import *


# Create your views here.

def store_page(request, categroy_slug=None, subcategory_slug=None, subbottomcategory_slug=None, brands_slug=None):
    context = {}

    brands = Brand.objects.all().filter(brands__category__slug=categroy_slug)
    products = None
    descriptions = DescriptionList.objects.all()

    if categroy_slug != None and subcategory_slug == None and brands_slug == None:
        category_s = MainCategory.objects.get(slug=categroy_slug)
        products = Product.objects.filter(category__slug=categroy_slug)
        context.update({'category_s': category_s, 'products': products})
    elif categroy_slug != None and subcategory_slug != None and brands_slug == None:
        category_s = MainCategory.objects.get(slug=categroy_slug)
        subcategory_s = SubCategory.objects.get(slug=subcategory_slug)
        products = Product.objects.filter(subcategory__slug=subcategory_slug).distinct()
        context.update({'category_s': category_s, 'subcategory_s': subcategory_s, 'products': products})
    elif categroy_slug != None and subcategory_slug != None and subbottomcategory_slug != None and brands_slug == None:
        category_s = MainCategory.objects.get(slug=categroy_slug)
        subcategory_s = SubCategory.objects.get(slug=subcategory_slug)
        subbottomcategory_s = SubBottomCategory.objects.get(slug=subbottomcategory_slug)
        products = Product.objects.filter(subbottomcategory__slug=subbottomcategory_slug).distinct()
        context.update(
            {'category_s': category_s, 'subcategory_s': subcategory_s, 'subbottomcategory_s': subbottomcategory_s,
             'products': products})
    elif categroy_slug == None and subcategory_slug == None and brands_slug != None:
        brands_s = Brand.objects.get(slug=brands_slug)
        products = Product.objects.filter(brand__slug=brands_slug)
        context.update({'brands_s': brands_s, 'products': products})

    context.update({'categroy_slug': categroy_slug, 'subcategory_slug': subcategory_slug, 'brands_slug': brands_slug,
                    'brands': brands, 'descriptions': descriptions})

    return render(request, 'frontend/pages/store.html', context)


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
        if 100 - ((p.discountprice * 100)/p.price) > 30:
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