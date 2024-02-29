from datetime import datetime, timezone, timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
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
    similar_product = ApiProduct.objects.filter(subbottomcategory=product.subbottomcategory).exclude(slug=product.slug).order_by(
        "?")[:6]

    product_question_count = Question.objects.all().filter(product=product).count()

    product_reviews = ReviewRating.objects.all().filter(product=product)[:10]

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

    now = datetime.now()
    tahmini_teslimat = now
    if now.weekday() == 5 or (now.weekday() == 4 and now.hour >= 23):
        tahmini_teslimat = tahmini_teslimat + timedelta(days=4)
    elif now.weekday() == 6 or (now.weekday() == 0 and now.hour <= 1):
        tahmini_teslimat = tahmini_teslimat + timedelta(days=3)
    else:
        tahmini_teslimat = tahmini_teslimat + timedelta(days=2)
        if tahmini_teslimat.weekday() == 5 or (tahmini_teslimat.weekday() == 4 and tahmini_teslimat.hour <= 23):
            tahmini_teslimat = tahmini_teslimat + timedelta(days=2)
        elif tahmini_teslimat.weekday() == 6 or (tahmini_teslimat.weekday() == 0 and tahmini_teslimat.hour <= 1):
            tahmini_teslimat = tahmini_teslimat + timedelta(days=1)


    context.update({
        'product': product,
        'image_urls': image_urls,
        'same_products': same_products,
        'similar_product': similar_product,
        'product_question_count':product_question_count,
        'product_reviews':product_reviews,
        'beden_tablosu': beden_tablosu,
        'beden_title':beden_title,
        'tahmini_teslimat':tahmini_teslimat,
        'favourite_status':favourite_status,
    })

    return render(request, 'frontend/v_2_0/sayfalar/urun/detay.html', context)


def degerlendirme_sayfasi(request, slug):
    context = {}
    product = get_object_or_404(ApiProduct, slug=slug)

    reviews = ReviewRating.objects.filter(product=product).order_by("created_at")
    reviews_count = ReviewRating.objects.filter(product=product).count()

    p = Paginator(reviews, 10)
    page = request.GET.get('page')
    product_reviews = p.get_page(page)

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
            return redirect('degerlendirme_sayfasi', slug)
    except:
        messages.warning(request, 'Değerlendirme yapabilmeniz için giriş yapmanız gerekmektedir.')
        return redirect('degerlendirme_sayfasi', slug)

    context.update({
        'product':product,
        'product_reviews':product_reviews,
        'reviews_count':reviews_count,
        'orderproduct':orderproduct,
    })

    return render(request, 'frontend/v_2_0/sayfalar/urun/yorum.html', context)

def filter_yorum(request, id):
    product = get_object_or_404(ApiProduct, id=id)
    filtered = request.GET.get('filter')
    reviews = ReviewRating.objects.filter(product=product).order_by(filtered)[:10]
    t = render_to_string('frontend/v_2_0/partials/__filter_degerlendirme.html', {'reviews': reviews})
    return JsonResponse({'data': t})

def load_more_degerlendirme(request, id):
    product = get_object_or_404(ApiProduct, id=id)

    filtered = request.GET.get('filter')
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])

    reviews = ReviewRating.objects.filter(product=product).order_by(filtered)[offset:offset + limit]

    t = render_to_string('frontend/v_2_0/partials/__filter_degerlendirme.html', {'reviews': reviews})
    return JsonResponse({'data': t})


def soru_sayfasi(request, slug):
    context = {}
    product = get_object_or_404(ApiProduct, slug=slug)

    question_reviews = Question.objects.filter(product=product).order_by("created_at")[:20]
    question_count = Question.objects.filter(product=product).count()

    try:
        if 'submitQuestion' in request.POST:
            question = request.POST.get("question")
            ip = request.META.get('REMOTE_ADDR')
            Question.objects.create(user=request.user, question=question, product=product, ip=ip)

            messages.success(request, 'Sorunuz başarıyla iletildi. En kısa sürede cevaplanacaktır.')
            return redirect('soru_sayfasi', slug)
    except:
        messages.warning(request, 'Değerlendirme yapabilmeniz için giriş yapmanız gerekmektedir.')
        return redirect('degerlendirme_sayfasi', slug)

    context.update({
        'product': product,
        'question_reviews': question_reviews,
        'question_count': question_count,
    })

    return render(request, 'frontend/v_2_0/sayfalar/urun/soru.html', context)


def load_more_question(request, id):
    product = get_object_or_404(ApiProduct, id=id)
    offset = int(request.GET['offset'])
    product_id = request.GET.get('product_id')
    limit = int(request.GET['limit'])
    question = Question.objects.all().filter(product=product)[offset:limit + offset]
    totalData = Question.objects.all().filter(product=product).count()

    t = render_to_string('frontend/v_2_0/sayfalar/urun/__daha_fazla_soru.html', {'question_reviews': question})
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
