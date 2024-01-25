import json

from django.db.models import Q, Count, Min, Max
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
import decimal
import requests
from adminpage.models import *
from customer.models import Subscription
from mainpage.models import *
from product.models import Brand, ReviewRating, ApiProduct, Pattern, EnvironmentType, ProductModelGroup
from categorymodel.models import *
from store.views import listToString


# Create your views here.

def index(request):
    context = {}
    flash_deals = []
    new_release = []

    banners = Banner.objects.all().order_by('order')

    context.update({
        'banners':banners,
    })
    return render(request, 'frontend/pages/mainpage.html', context)


def ajax_search(request):
    res = None
    series = request.GET.get('series', '')

    if len(series) > 3:
        ip = request.META.get('REMOTE_ADDR')
        is_exists = MostSearchingKeyword.objects.filter(keyword=series)
        if is_exists.count() > 0:
            keyword = MostSearchingKeyword.objects.get(keyword=series)
            keyword.count += 1
            keyword.save()
        else:
            MostSearchingKeyword.objects.create(keyword=series, ip=ip)

    products = ProductModelGroup.objects.filter(product__title__icontains=series, product__is_publish=True)[:15]

    if len(products) > 0:
        data = []
        for r in products:
            if r.kapak:
                item = {
                    'id': r.product.id,
                    'title': r.product.title,
                    'slug': r.product.slug,
                    'image': str(r.kapak.url),
                    'get_url': r.product.get_url(),
                }
                data.append(item)
            else:
                item = {
                    'id': r.product.id,
                    'title': r.product.title,
                    'slug': r.product.slug,
                    'image': r.product.image_url1,
                    'get_url': r.product.get_url(),
                }
                data.append(item)
        res = data
    else:
        res = "no-data"
    return JsonResponse({'data': res})


def search(request):
    context = {}
    keyword = request.GET['q']

    categories = MainCategory.objects.all()
    brands = Brand.objects.all()

    category_type = "search"

    minMaxPrice = ApiProduct.objects.filter().aggregate(
        Min('discountprice'),
        Max('discountprice'))

    context.update({
        'keyword': keyword,
        'categories': categories,
        'category_type': category_type
    })

    if keyword:
        products = ProductModelGroup.objects.filter(Q(product__title__icontains=keyword) | Q(product__category__title__icontains=keyword) | Q(
            product__subcategory__title__icontains=keyword) | Q(product__subbottomcategory__title__icontains=keyword) | Q(product__brand__title__icontains=keyword), product__is_publish=True)

        minMaxPrice = products.aggregate(
            Min('product__price'),
            Max('product__price'))

        product_count = products.count()

        context.update({
            'products': products,
            'product_count': product_count,
            'brands': brands,
            'minMaxPrice': minMaxPrice,
        })

    return render(request, 'frontend/pages/store.html', context)


def search_product_filter(request):
    keyword = request.GET['keyword']
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

    data = []

    if keyword:
        data = ProductModelGroup.objects.filter(Q(product__title__icontains=keyword) | Q(product__category__title__icontains=keyword) | Q(
            product__subcategory__title__icontains=keyword) | Q(product__brand__title__icontains=keyword), product__price__gte=minPrice,
                                      product__price__lte=maxPrice, product__is_publish=True).order_by(order_type)

    t = render_to_string('frontend/partials/ajax/product-list.html', {'data': data})
    return JsonResponse({'data': t})


def sss(request):
    context = {}
    faq = SSS.objects.all()
    context.update({
        'faq': faq,
    })
    return render(request, 'frontend/information/faq.html', context)


def delivery_conditional(request):
    context = {}
    contracts = Contracts.objects.all().last()
    context.update({
        'contracts': contracts
    })

    return render(request, 'frontend/information/delivery_conditional.html', context)


def membership_contract(request):
    context = {}
    contracts = Contracts.objects.all().last()
    context.update({
        'contracts': contracts
    })

    return render(request, 'frontend/information/membership_contract.html', context)


def terms_of_use(request):
    context = {}
    contracts = Contracts.objects.all().last()
    context.update({
        'contracts': contracts
    })

    return render(request, 'frontend/information/terms_of_use.html', context)


def security_policy(request):
    context = {}
    contracts = Contracts.objects.all().last()
    context.update({
        'contracts': contracts
    })

    return render(request, 'frontend/information/security_policy.html', context)


def kvkk(request):
    context = {}
    contracts = Contracts.objects.all().last()
    context.update({
        'contracts': contracts
    })

    return render(request, 'frontend/information/kvkk.html', context)


def cookies(request):
    context = {}
    contracts = Contracts.objects.all().last()
    cookie = Cookies.objects.filter(is_active=True)
    context.update({
        'contracts': contracts,
        'cookie': cookie
    })

    return render(request, 'frontend/information/cookies.html', context)


def subscription(request):
    if 'subscriptionBtn' in request.POST:
        email = request.POST.get('email')
        ip = request.META.get('REMOTE_ADDR')
        if email != '':
            if Subscription.objects.filter(email=email).exists():
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                Subscription.objects.create(email=email, ip=ip)
            return redirect(request.META.get('HTTP_REFERER'))


def aboutus(request):
    context = {}
    about = Hakkimizda.objects.all().last()
    context.update({'about':about})

    return render(request, 'frontend/pages/aboutus.html', context)

def error_404_view(request, exception):
    return render(request, 'frontend/partials/404.html', status=404)


def error_500_view(request):
    return render(request, 'frontend/partials/500.html', status=500)
