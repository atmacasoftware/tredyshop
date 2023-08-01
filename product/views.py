from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from orders.models import OrderProduct
from product.models import *
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

from product.read_xml import modaymissaveXML2db, updateModaymisSaveXML2db


# Create your views here.

def products_detail(request, product_slug):
    context = {}
    query = ''
    product = Product.objects.get(slug=product_slug)
    product_images = Images.objects.filter(product=product)
    product_descriptions = DescriptionList.objects.filter(product=product)[:5]
    product_keywords = ProductKeywords.objects.filter(product=product)
    product_keywords_count = ProductKeywords.objects.filter(product=product).count()
    product_reviews = ReviewRating.objects.all().filter(product=product)
    product_question = Question.objects.all().filter(product=product)
    product_question_count = Question.objects.all().filter(product=product).count()
    product_spesicifation = Specification.objects.filter(product=product)
    paginator_reviews = Paginator(product_reviews, 10)
    page_number = request.GET.get('page')
    reviews_obj = paginator_reviews.get_page(page_number)

    ip = request.META.get('REMOTE_ADDR')

    paginator_question = Paginator(product_question, 10)
    page_number_question = request.GET.get('page')
    question_obj = paginator_question.get_page(page_number_question)

    try:
        if request.user.is_authenticated:
            stock_alarm = StockAlarm.objects.get(user=request.user, product=product)
        else:
            stock_alarm = StockAlarm.objects.get(ip=ip, product=product)
    except:
        stock_alarm = None

    similar_product = Product.objects.filter(category=product.category).exclude(slug=product.slug)

    favourite_status = 0
    try:
        favourite_product = Favorite.objects.filter(product=product, customer=request.user)

        if favourite_product.count() > 0:
            favourite_status = 1
    except:
        pass

    if similar_product.count() > 20:
        similar_product = similar_product[:20]

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

    try:
        if 'addQuestionBtn' in request.POST:
            question = request.POST.get('question')
            ip = request.META.get('REMOTE_ADDR')

            if question != '':
                data = Question.objects.create(user=request.user, product=product, question=question, ip=ip)
                messages.success(request, 'Sorunuz başarıyla iletilmiştir.')
                return redirect('products_detail', product_slug)

    except:
        messages.warning(request, 'Soru sorabilmeniz için giriş yapmanız gerekmektedir.')
        return redirect('products_detail', product_slug)

    context.update({
        'product': product,
        'product_images': product_images,
        'product_descriptions': product_descriptions,
        'product_keywords': product_keywords,
        'product_keywords_count': product_keywords_count,
        'product_reviews': reviews_obj,
        'product_question': question_obj,
        'product_question_count': product_question_count,
        'similar_product': similar_product,
        'favourite_status': favourite_status,
        'orderproduct': orderproduct,
        'product_spesicifation': product_spesicifation,
        'stock_alarm': stock_alarm,
    })

    if product.variant != 'Yok':
        if request.method == 'POST':
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)
            colors = Variants.objects.filter(product_id=product.id, size_id=variant.size_id)
            sizes = Variants.objects.raw('SELECT * FROM product_variants WHERE product_id=%s GROUP BY size_id',
                                         [product.id])
            query += variant.title + ' Size:' + str(variant.size.code) + ' Color:' + str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=product.id)
            print(variants)
            colors = Variants.objects.filter(product_id=product.id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw('SELECT * FROM product_variants WHERE product_id=%s GROUP BY size_id',
                                         [product.id])
            variant = Variants.objects.get(id=variants[0].id)

        context.update({
            'sizes': sizes,
            'colors': colors,
            'variant': variant,
            'query': query
        })

    return render(request, 'frontend/pages/product_detail.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productId = request.POST.get('productId')
        colors = Variants.objects.filter(product_id=productId, size_id=size_id)
        context = {
            'size_id': size_id,
            'product_id': productId,
            'colors': colors
        }

        print(colors)

        data = {'rendered_table': render_to_string('frontend/partials/product_color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def load_more_reviews(request):
    offset = int(request.GET['offset'])
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    limit = 10
    reviews = ReviewRating.objects.all().filter(product=product)[offset:limit + offset]
    totalData = ReviewRating.objects.all().filter(product=product).count()
    t = render_to_string('frontend/partials/__load_more_reviews.html', {'data': reviews})
    return JsonResponse({'data': t})


def load_more_question(request):
    offset = int(request.GET['offset'])
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    limit = 10
    question = Question.objects.all().filter(product=product)[offset:limit + offset]
    totalData = Question.objects.all().filter(product=product).count()
    t = render_to_string('frontend/partials/__load_more_question.html', {'data': question})
    return JsonResponse({'data': t})


def ajax_favourite(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    favourite = Favorite.objects.filter(customer=request.user, product=product)
    data = {}
    if favourite.count() > 0:
        Favorite.objects.get(customer=request.user, product=product).delete()
        data = {'favourite': 'deleted'}
    else:
        Favorite.objects.create(customer=request.user, product=product)
        data = {'favourite': 'added'}
    return JsonResponse({'data': data})


def ajax_stockalarm(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
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

@login_required(login_url="/yonetim-paneli/")
def modaymis_product_load(request):
    if request.user.is_superuser == True:
        if 'upload' in request.POST:
            modaymissaveXML2db()
            messages.success(request, 'Veriler yüklendi!')
            return redirect("modaymis_product_load")
        if 'update' in request.POST:
            updateModaymisSaveXML2db()
            messages.success(request, 'Veriler güncelledi!')
            return redirect("modaymis_product_load")
    else:
        return redirect("mainpage")
    return render(request, "backend/pages/load_modaymis.html")