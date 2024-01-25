from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
import requests

from adminpage.models import Notification
from carts.helpers import paytr_taksit_sorgu, taksit_hesaplama
from orders.models import OrderProduct
from product.models import *
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.

def products_detail(request, product_slug):
    context = {}
    query = ''
    product = ApiProduct.objects.get(slug=product_slug)

    image_urls = [
        product.image_url1, product.image_url2, product.image_url3, product.image_url4, product.image_url5,
        product.image_url6, product.image_url7, product.image_url8
    ]

    beden_title = None
    beden_tablosu = None

    if product.subcategory.title == "Üst Giyim":
        if "büyük beden" in product.title:
            beden_tablosu = KadinUstBuyukBedenTablosu.objects.all()
            beden_title = "Kadın Üst Büyük Beden Tablosu"
        else:
            beden_tablosu = KadinUstBedenTablosu.objects.all()
            beden_title = "Kadın Üst Beden Tablosu"

    elif product.subcategory.title == "Alt Giyim":
        if "büyük beden" in product.title:
            beden_tablosu = KadinAltBuyukBedenTablosu.objects.all()
            beden_title = "Kadın Alt Büyük Beden Tablosu"
        else:
            beden_tablosu = KadinAltBedenTablosu.objects.all()
            beden_title = "Kadın Alt Beden Tablosu"

    else:
        beden_tablosu = None

    same_products = ApiProduct.objects.filter(model_code=product.model_code).order_by('-size__name')
    similar_product = ApiProduct.objects.filter(subcategory=product.subcategory).exclude(slug=product.slug).order_by(
        "?")

    product_question = Question.objects.all().filter(product=product)
    product_question_count = Question.objects.all().filter(product=product).count()
    paginator_question = Paginator(product_question, 10)
    page_number_question = request.GET.get('page')
    question_obj = paginator_question.get_page(page_number_question)

    product_reviews = ReviewRating.objects.all().filter(product=product)
    paginator_reviews = Paginator(product_reviews, 10)
    page_number = request.GET.get('page')
    reviews_obj = paginator_reviews.get_page(page_number)

    ip = request.META.get('REMOTE_ADDR')

    if similar_product.count() > 20:
        similar_product = similar_product[:20]

    try:
        if 'addQuestionBtn' in request.POST:
            question = request.POST.get('question')
            ip = request.META.get('REMOTE_ADDR')

            if question != '':
                data = Question.objects.create(user=request.user, product=product, question=question, ip=ip)
                Notification.objects.create(noti_type="5", customer=request.user, question=data, title="Yeni bir ürün sorusu geldi.")
                messages.success(request, 'Sorunuz başarıyla iletilmiştir.')
                return redirect('products_detail', product_slug)

    except:
        messages.warning(request, 'Soru sorabilmeniz için giriş yapmanız gerekmektedir.')
        return redirect('products_detail', product_slug)

    try:
        if request.user.is_authenticated:
               stock_alarm = StockAlarm.objects.get(user=request.user, product=product)
        else:
               stock_alarm = StockAlarm.objects.get(ip=ip, product=product)
    except:
           stock_alarm = None

    favourite_status = 0
    try:
        favourite_product = Favorite.objects.filter(product=product, customer=request.user)
        if favourite_product.count() > 0:
            favourite_status = 1
    except:
        pass

    try:
        orderproduct = None
        if request.user.is_authenticated:
            orderproduct = OrderProduct.objects.filter(user=request.user, product=product).exists()
    except OrderProduct.DoesNotExist:
        orderproduct = None
    try:
        if 'submitComment' in request.POST:
            rating = request.POST.get("rating")
            comment = request.POST.get('comments')
            images = request.FILES.getlist('images')
            ip = request.META.get('REMOTE_ADDR')
            data = ReviewRating.objects.create(user=request.user, rating=rating, product=product, review=comment, ip=ip)
            for image in images:
                ReviewRatingImages.objects.create(review=data, product=product, images=image)
            messages.success(request, 'Değerlendirmeniz için teşekkür ederiz.')
            return redirect('products_detail', product_slug)
    except:
        messages.warning(request, 'Değerlendirme yapabilmeniz için giriş yapmanız gerekmektedir.')
        return redirect('products_detail', product_slug)

    context.update({
        'product': product,
        'image_urls': image_urls,
        'same_products': same_products,
        'similar_product': similar_product,
        'question_obj':question_obj,
        'product_question_count':product_question_count,
        'product_question':product_question,
        'reviews_obj':reviews_obj,
        'beden_tablosu': beden_tablosu,
        'beden_title':beden_title
    })

    return render(request, 'frontend/pages/product_detail.html', context)


def load_more_reviews(request):
    offset = int(request.GET['offset'])
    product_id = request.GET.get('product_id')
    product = ApiProduct.objects.get(id=product_id)
    limit = 10
    reviews = ReviewRating.objects.all().filter(product=product)[offset:limit + offset]
    totalData = ReviewRating.objects.all().filter(product=product).count()
    t = render_to_string('frontend/partials/__load_more_reviews.html', {'data': reviews})
    return JsonResponse({'data': t})


def load_more_question(request):
    offset = int(request.GET['offset'])
    product_id = request.GET.get('product_id')
    product = ApiProduct.objects.get(id=product_id)
    limit = 10
    question = Question.objects.all().filter(product=product)[offset:limit + offset]
    totalData = Question.objects.all().filter(product=product).count()
    t = render_to_string('frontend/partials/__load_more_question.html', {'data': question})
    return JsonResponse({'data': t})


def ajax_favourite(request):
    product_id = request.GET.get('product_id')
    product = ApiProduct.objects.get(id=product_id)
    favourite = Favorite.objects.filter(customer=request.user, product=product)
    data = {}
    if favourite.count() > 0:
        Favorite.objects.get(customer=request.user, product=product).delete()
        data = {'favourite': 'deleted'}
    else:
        Favorite.objects.create(customer=request.user, product=product)
        data = {'favourite': 'added'}
    return JsonResponse({'data': data})


def deleted_favourite(request, product_id):
    product = ApiProduct.objects.get(id=product_id)
    Favorite.objects.get(customer=request.user, product=product).delete()
    data = {'favourite': 'deleted'}
    return JsonResponse({'data': data})


def ajax_stockalarm(request):
    product_id = request.GET.get('product_id')
    product = ApiProduct.objects.get(id=product_id)
    ip = request.META.get('REMOTE_ADDR')
    data = {}
    try:
        if request.user.is_authenticated:
            stockalarm = StockAlarm.objects.create(user=request.user, ip=ip, is_active=True, product=product)
            data = {'notify': 'success'}
        else:
            stockalarm = StockAlarm.objects.create(ip=ip, is_active=True, product=product)
            data = {'notify': 'success'}
    except:
        data = {'notify': 'error'}

    return JsonResponse({'data': data})
