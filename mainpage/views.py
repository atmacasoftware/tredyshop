from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render
from mainpage.models import *
from product.models import Product, Brand, ReviewRating
from orders.models import OrderProduct
from categorymodel.models import *


# Create your views here.

def index(request):
    context = {}
    sliders = Slider.objects.filter(is_publish=True)
    flash_deals = []
    all_product = Product.objects.all()
    aaa = Product.objects.all().order_by("-sell_count")
    new_release = all_product.order_by("-create_at")
    most_seller = all_product.order_by("-sell_count").first()
    most_seller2 = all_product.order_by("-sell_count")[1:2]
    most_seller3 = all_product.order_by("-sell_count")[2:3]
    most_seller4 = all_product.order_by("-sell_count")[3:4]

    reviewrating = ReviewRating.objects.all()
    liked_product = Product.objects.all().filter(reviewrating__rating__gte=4, reviewrating__rating__lte=6)[:3]
    most_count = Product.objects.filter(reviewrating__in=reviewrating).annotate(rating_count=Count('id')).order_by(
        '-rating_count')[:3]
    most_selling = Product.objects.all().order_by("-sell_count")[:3]

    brands = Brand.objects.all()

    for product in all_product:
        if product.is_discountprice == True:
            if 100 - ((product.discountprice * 100) / product.price) >= 0:
                flash_deals.append(product)

    context.update({
        'sliders': sliders,
        'new_release': new_release,
        'flash_deals': flash_deals,
        'most_seller': most_seller,
        'most_seller2': most_seller2,
        'most_seller3': most_seller3,
        'most_seller4': most_seller4,
        'brands': brands,
        'liked_product': liked_product,
        'most_count': most_count,
        'most_selling': most_selling,
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

    products = Product.objects.filter(title__icontains=series)

    if len(products) > 0:
        data = []
        for r in products:
            item = {
                'id': r.id,
                'title': r.title,
                'slug': r.slug,
                'image': r.image.url,
                'get_url': r.get_url(),
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

    context.update({
        'keyword': keyword,
        'categories': categories
    })

    if keyword:
        products = Product.objects.filter(Q(title__icontains=keyword) | Q(category__title__icontains=keyword) | Q(
            subcategory__title__icontains=keyword) | Q(brand__title__icontains=keyword))
        product_count = products.count()

        context.update({
            'products': products,
            'product_count': product_count,
            'brands': brands,
        })

    return render(request, 'frontend/pages/result_search.html', context)


def slider_info(request, slider_slug):
    context = {}
    slider = Slider.objects.get(slug=slider_slug)
    context.update({
        'slider':slider,
    })
    return render(request, 'frontend/pages/slider_info.html', context)


def sss(request):
    context = {}
    faq = SSS.objects.all()
    context.update({
        'faq':faq,
    })
    return render(request, 'frontend/information/faq.html', context)

def delivery_conditional(request):
    context = {}
    contracts = Contracts.objects.all().last()
    context.update({
        'contracts':contracts
    })

    return render(request, 'frontend/information/delivery_conditional.html', context)

def membership_contract(request):
    context = {}
    contracts = Contracts.objects.all().last()
    context.update({
        'contracts':contracts
    })

    return render(request, 'frontend/information/membership_contract.html', context)

def terms_of_use(request):
    context = {}
    contracts = Contracts.objects.all().last()
    context.update({
        'contracts':contracts
    })

    return render(request, 'frontend/information/terms_of_use.html', context)

def security_policy(request):
    context = {}
    contracts = Contracts.objects.all().last()
    context.update({
        'contracts':contracts
    })

    return render(request, 'frontend/information/terms_of_use.html', context)

def kvkk(request):
    context = {}
    contracts = Contracts.objects.all().last()
    context.update({
        'contracts':contracts
    })

    return render(request, 'frontend/information/terms_of_use.html', context)