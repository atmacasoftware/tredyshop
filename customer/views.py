import math
import random
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout


from adminpage.custom import sendAccountVerificationEmail, customerTredyShopExtraditionRequestOrder, \
    sendExtraditionRequestInfoEmail
from adminpage.models import Notification
from carts.models import Cart, CartItem
from customer.forms import *
from customer.models import CustomerAddress
from ecommerce.settings import EMAIL_HOST_USER
from orders.models import Order, OrderProduct, ExtraditionRequest, ExtraditionRequestResult, \
    CancellationRequest
from user_accounts.models import User
from product.models import Favorite, ReviewRating, Question, Product, ProductVariant


# Create your views here.

def login(request):
    try:
        if request.user.is_authenticated:
            messages.success(request, 'Giriş yapıldı')
            return redirect('mainpage')
        if 'login_btn' in request.POST:
            if request.method == 'POST':
                email = request.POST.get('email')
                password = request.POST.get('password')
                remember_me = request.POST.get('remember_me')
                user_obj = User.objects.filter(email=email)
                if not user_obj.exists():
                    messages.error(request, 'Bu kullanıcı mevcut değil.')
                    return redirect('login')
                user_obj = authenticate(email=email, password=password)
                if user_obj is not None:
                    if user_obj.is_activated == True:
                        try:
                            cart = Cart.objects.get(cart_id=request.META.get('REMOTE_ADDR'))
                            is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                            if is_cart_item_exists:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user_obj
                                    item.save()
                        except:
                            pass
                        auth_login(request, user_obj)
                        if not remember_me:
                            request.session.set_expiry(18000)
                        return redirect('mainpage')

                    else:
                        messages.warning(request,
                                         "Hesap etkinleştirilmemiştir. Lütfen kayıtlı e-posta adresinize gönderilen mail üzerindeki linke tıklayarak hesabınızı etkinleştiriniz.")
                        return redirect('mainpage')
                else:
                    messages.warning(request, "E-posta veya şifre hatalı. Lütfen tekrar deneyiniz.")
                    return redirect('login')
        return render(request, 'frontend/v_2_0/kullanici_islemleri/giris_yap.html')
    except Exception as e:
        return redirect('login')

def generateOTP():
    digits = "0123456789"
    otp = ""
    for i in range(6):
        otp += digits[math.floor(random.random() * 10)]
    return otp

def register(request):
    try:
        if request.user.is_authenticated:
            messages.success(request, 'Giriş yapıldı')
            return redirect('mainpage')
        if request.is_ajax():
            otp = generateOTP()
            return JsonResponse(data=otp, safe=False)
        return render(request, 'frontend/v_2_0/kullanici_islemleri/kayit-ol.html')
    except Exception as e:
        messages.warning(request, 'Bir hata meydana geldi!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def register_ajax(request):
    data = 'error'

    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    mobile = request.POST.get('mobile')
    password = request.POST.get('password')
    otp = request.POST.get('otp')
    user_obj = User.objects.filter(email=email)

    if user_obj.exists():
        messages.error(request, 'Bu kullanıcı zaten mevcuttur!')
        return redirect('login')
    if first_name != '' and last_name != '' and email != '' and mobile != '' and password != '':
        data = 'success'
        sendAccountVerificationEmail(request=request, first_name=first_name, last_name=last_name, email=email, otp=otp)
    else:
        data = 'error'

    return JsonResponse(data=data, safe=False)

def createUser(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    mobile = request.POST.get('mobile')
    password = request.POST.get('password')

    hass_pass = make_password(password)

    user = User.objects.create(first_name=first_name, last_name=last_name, email=email,
                                    password=hass_pass,
                                    mobile=mobile, is_customer=True, is_staff=False, is_activated=True)
    notify = Notification.objects.create(noti_type="8", customer=user,
                                         title="Yeni müşteri kaydı yapıldı.",
                                         detail="Yeni müşteri kaydı yapıldı.")

    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/giris-yap")
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def validate_email(request, *args, **kwargs):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email=email).exists()
    }
    return JsonResponse(data)


@login_required(login_url="/giris-yap")
def profile_mainpage(request):
    user = request.user

    if 'userInfoBtn' in request.POST:
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            birthday = request.POST.get('birthday')
            gender = request.POST.get('gender')
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.mobile = mobile
            if birthday:
                user.birthday = birthday
            if gender == "1":
                user.gender = False
            else:
                user.gender = True
            user.save()
            messages.success(request, 'Tebrikler üyeliğiniz başarıyla güncellendi.')
            return redirect('profile_mainpage')

    if 'createPasswordBtn' in request.POST:
        password = request.POST.get('new_password')
        hasspass = make_password(password)
        user.password = hasspass
        user.username = None
        user.is_activated = True
        user.save()
        messages.success(request, 'Şifreniz başarıyla oluşturuldu.')
        return redirect('profile_mainpage')

    if 'changePasswordBtn' in request.POST:
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        flag = check_password(current_password, request.user.password)

        if flag:
            haspass = make_password(new_password)
            request.user.password = haspass
            request.user.save()
            messages.success(request, 'Şifreniz başarıyla değiştirildi. Tekrar giriş yapmanız gerekmektedir.')
            return redirect('logout')

        else:
            messages.error(request, 'Mevcut şifreniz doğru değil!')
            return redirect('profile_mainpage')

    return render(request, 'frontend/v_2_0/sayfalar/profil/anasayfa.html')


@login_required(login_url="/giris-yap")
def address(request):
    context = {}
    user = request.user
    all_address = CustomerAddress.objects.filter(user=user)

    add_form = AddressForm(data=request.POST or None, files=request.FILES or None)
    context.update({'all_address': all_address, 'add_form': add_form})

    if 'addAddressBtn' in request.POST:
        if add_form.is_valid():
            current_address = request.POST.get("is_active")
            type = request.POST.get("bill_type")
            tc = request.POST.get("tc")
            if type == "Bireysel":
                if len(tc) == 11:
                    if current_address == "Evet":
                        user_address = CustomerAddress.objects.filter(is_active="Evet")
                        for u in user_address:
                            u.is_active = "Hayır"
                            u.save()

                    data = add_form.save(commit=False)
                    data.company_name = None
                    data.tax_number = None
                    data.tax_administration = None
                    data.user = user
                    data.save()
                    messages.success(request, 'Adres başarıyla eklendi.')
                    return redirect('address')
                else:
                    messages.error(request, 'T.C. Kimlik Numarası 11 basamaklı olmalıdır.')
                    return redirect('address')
            if type == "Kurumsal":
                if current_address == "Evet":
                    user_address = CustomerAddress.objects.filter(is_active="Evet")
                    for u in user_address:
                        u.is_active = "Hayır"
                        u.save()

                data = add_form.save(commit=False)
                data.tc = None
                data.user = user
                data.save()
                messages.success(request, 'Adres başarıyla eklendi.')
                return redirect('address')
    return render(request, 'frontend/v_2_0/sayfalar/profil/adresler.html', context)


def load_counties(request):
    city_id = request.GET.get('city_id')
    counties = County.objects.filter(city_id=city_id)
    return render(request, 'frontend/v_2_0/sayfalar/profil/dropdown_ilceler.html', {'counties': counties})


@login_required(login_url="/giris-yap")
def update_address(request, id):
    context = {}
    address = get_object_or_404(CustomerAddress, id=id)
    update_form = AddressForm(instance=address, data=request.POST or None, files=request.FILES or None)
    context.update({'address': address, 'update_form': update_form})

    if 'updateAddressBtn' in request.POST:
        if update_form.is_valid():
            data = update_form.save(commit=False)
            type = request.POST.get("bill_type")
            tc = request.POST.get("tc")
            company_name = request.POST.get("company_name")
            tax_number = request.POST.get("tax_number")
            tax_administration = request.POST.get("tax_administration")

            if type == "Bireysel":
                data.company_name = None
                data.tax_number = None
                data.tax_administration = None

            if type == "Kurumsal":
                data.tc = None
            data.save()
            messages.success(request, 'Adres başarıyla güncellendi.')
            return redirect('update_address', id)

    return render(request, 'frontend/v_2_0/sayfalar/profil/adres_guncelle.html', context)


@login_required(login_url="/giris-yap")
def is_active_address(request, id):
    address = get_object_or_404(CustomerAddress, id=id)
    address.is_active = "Evet"
    address.save()
    messages.success(request, f'{address.title} aktif adres olarak seçildi.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/giris-yap")
def delete_address(request, id):
    address = get_object_or_404(CustomerAddress, id=id)
    address.delete()
    messages.success(request, 'Adres başarıyla silindi.')
    return redirect('address')


@login_required(login_url="/giris-yap")
def wishlist(request):
    context = {}

    favourite_products = Favorite.objects.filter(customer=request.user, product__is_publish=True)
    favourite_products_count = Favorite.objects.filter(customer=request.user).count()
    context.update({
        'favourite_products': favourite_products,
        'favourite_products_count':favourite_products_count,
    })

    return render(request, 'frontend/v_2_0/sayfalar/profil/favoriler.html', context)


@login_required(login_url="/giris-yap")
def delete_wishlist(request, id):
    favourite_product = Favorite.objects.get(customer=request.user, id=id)
    favourite_product.delete()
    messages.success(request, f'{favourite_product.product.title} ürünü favorilerden çıkartıldı.')
    return redirect('wishlist')


@login_required(login_url="/giris-yap")
def reviews(request):
    context = {}

    reviews = ReviewRating.objects.all().filter(user=request.user)
    reviews_count = ReviewRating.objects.all().filter(user=request.user).count()
    context.update({
        'reviews': reviews,
        'reviews_count': reviews_count
    })
    return render(request, 'frontend/v_2_0/sayfalar/profil/degerlendirmeler.html', context)


@login_required(login_url="/giris-yap")
def order_page(request):
    context = {}
    orders = Order.objects.filter(user=request.user)
    orders_count = Order.objects.filter(user=request.user).count()
    context.update({
        'orders': orders,
        'orders_count': orders_count
    })
    return render(request, 'frontend/v_2_0/sayfalar/profil/siparisler.html', context)


@login_required(login_url="/giris-yap")
def order_detail(request, order_number):

    context = {}
    order = Order.objects.get(user=request.user, order_number=order_number)
    orderproducts = OrderProduct.objects.filter(order=order)
    orderproduct_count = orderproducts.count()
    extraditionrequest_exists = ExtraditionRequest.objects.filter(user=request.user, order=order).exists()
    cancelling_request = CancellationRequest.objects.filter(user=request.user, order=order)
    address = order.address
    cart_items = orderproducts

    context.update({
        'order': order,
        'orderproducts': orderproducts,
        'orderproduct_count': orderproduct_count,
        'extraditionrequest_exists': extraditionrequest_exists,
        'cancelling_request': cancelling_request,
        'address':address,
        'cart_items':cart_items
    })
    if 'addExtraditionRequestBtn' in request.POST:
        extradition_type = request.POST.get('extraditiontype')
        desc = request.POST.get('description')
        product_id = request.POST.get('product_id')
        product = ProductVariant.objects.get(id=product_id)
        orderproduct = OrderProduct.objects.get(order=order, product=product)
        extradition = ExtraditionRequest.objects.create(order=order, user=request.user,
                                                        extradition_type=extradition_type, description=desc,
                                                        product=product)
        orderproduct.is_extradation = True
        orderproduct.save()
        customerTredyShopExtraditionRequestOrder(request=request, email=request.user.email, order_number=order.order_number)
        sendExtraditionRequestInfoEmail(request=request, email="atmacaahmet5261@hotmail.com", order_number=order.order_number, siparis_tarihi=order.created_at, iade_tarihi=extradition.created_at, urun_id=product_id)
        messages.success(request, 'Ürün iade talebi iletildi.')
        return redirect('order_detail', order_number)
    return render(request, 'frontend/v_2_0/sayfalar/profil/siparis_detay.html', context)



@login_required(login_url="/giris-yap")
def cancellig_order_product(request, order_number, product_id):
    order = Order.objects.get(order_number=order_number)
    product = ProductVariant.objects.get(id=product_id)
    orderproduct = OrderProduct.objects.get(order=order, product=product)
    cancelling = CancellationRequest.objects.create(order=order, user=request.user, product=product)
    orderproduct.is_cancelling = True
    orderproduct.save()
    messages.success(request, 'Ürün iptal edildi.')
    return redirect('order_detail', order_number)


@login_required(login_url="/giris-yap")
def coupon_page(request):
    context = {}
    coupons = Coupon.objects.filter(user=request.user)
    coupon_count = Coupon.objects.filter(user=request.user).count()

    context.update({
        'coupons': coupons,
        'coupon_count': coupon_count,
    })
    return render(request, 'frontend/v_2_0/sayfalar/profil/kuponlar.html', context)


@login_required(login_url="/giris-yap")
def question_page(request):
    context = {}
    question = Question.objects.filter(user=request.user)
    question_count = Question.objects.filter(user=request.user).count()

    context.update({
        'question': question,
        'question_count': question_count,
    })
    return render(request, 'frontend/v_2_0/sayfalar/profil/soru_taleplerim.html', context)
