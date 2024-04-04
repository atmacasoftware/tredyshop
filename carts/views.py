from datetime import date
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import random

from adminpage.custom import customerTredyShopCreateOrder, sendOrderInfoEmail, productStatistic
from carts.helpers import paytr_api, card_type, paytr_sorgu, paytr_taksit_sorgu, taksit_hesaplama, \
    bin_sorgu, paytr_post, create_order_token
from customer.forms import AddressForm
from customer.models import CustomerAddress, Bonuses, Coupon
from ecommerce import settings
from mainpage.models import Setting
from carts.models import Cart, CartItem
from orders.models import Order, OrderProduct
from product.models import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request):
    quantity = int(request.GET.get('quantity', 1))
    barcode = request.POST.get('barcode')
    data = None
    url = request.META.get('HTTP_REFERER')
    product = ProductVariant.objects.get(barcode=barcode, is_publish=True)
    current_user = request.user

    same_product = 0
    if current_user.is_authenticated:
        checkinproduct = CartItem.objects.filter(product=product, user=current_user).exists()
        if checkinproduct:
            control = 1
        else:
            control = 2

        if request.method == 'POST':
            if control == 1:
                data = CartItem.objects.get(product=product, user=current_user)
                same_product = 1
                data.quantity += quantity
                try:
                    cart = Cart.objects.get(
                        cart_id=_cart_id(request))
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=_cart_id(request))
                cart.save()
                data.save()
            else:
                same_product = 2
                try:
                    cart = Cart.objects.get(
                        cart_id=_cart_id(request))
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=_cart_id(request))
                cart.save()
                data = CartItem()
                data.user = request.user
                data.product = product
                data.cart = cart
                data.quantity = quantity
                data.save()
            return JsonResponse({'data': 'added', 'plus': '1', 'control': control, 'same_product': same_product})

    else:

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        checkinproduct = CartItem.objects.filter(product=product, cart=cart).exists()
        if checkinproduct:
            control = 1
        else:
            control = 2

        if request.method == 'POST':
            if control == 1:
                data = CartItem.objects.get(product=product, cart=cart)
                same_product = 1
                data.quantity += quantity
                try:
                    cart = Cart.objects.get(
                        cart_id=_cart_id(request))
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=_cart_id(request))
                cart.save()
                data.save()
            else:
                same_product = 2
                try:
                    cart = Cart.objects.get(
                        cart_id=_cart_id(request))
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=_cart_id(request))
                cart.save()
                data = CartItem()
                data.product = product
                data.cart = cart
                data.quantity = quantity
                data.save()
            return JsonResponse({'data': 'added', 'plus': '1', 'control': control, 'same_product': same_product})


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(ProductVariant, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, id=cart_item_id, user=request.user)
            cart_item.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            cart_item.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def minus_quantity(request, product_id, cart_item_id):
    product = get_object_or_404(ProductVariant, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, id=cart_item_id, user=request.user)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def plus_quantity(request, product_id, cart_item_id):
    product = get_object_or_404(ProductVariant, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, id=cart_item_id, user=request.user)
            if cart_item.quantity == cart_item.product.quantity:
                cart_item.quantity = cart_item.product.quantity
                messages.warning(request,
                                 'Malasef stoklarımızda ilgili üründen daha fazla bulunmadığından artış yapılamamıştır.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                cart_item.quantity += 1
                cart_item.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            if cart_item.quantity == cart_item.product.quantity:
                cart_item.quantity = cart_item.product.quantity
                messages.warning(request,
                                 'Malasef stoklarımızda ilgili üründen daha fazla bulunmadığından artış yapılamamıştır.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                cart_item.quantity += 1
                cart_item.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart(request, cart_items=None):
    context = {}
    cart = None
    cartitem_count = 0
    favourite_status = 0
    products = ProductVariant.objects.filter(is_publish=True).order_by('?')[:8]
    add_form = None

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            cartitem_count = CartItem.objects.filter(user=request.user, is_active=True).count()
            all_address = CustomerAddress.objects.all().filter(user=request.user)
            add_form = AddressForm(data=request.POST or None, files=request.FILES or None)

            try:
                address = CustomerAddress.objects.get(is_active="Evet", user=request.user)
            except:
                address = None

            total_count = 0
            total_price = 0
            minus = 0
            setting = Setting.objects.all().last()
            delivery_price = 0

            for c in cart_items:
                total_count += c.quantity
                if c.product.product.is_discountprice:
                    total_price += c.product.product.discountprice * c.quantity
                else:
                    total_price += c.product.product.price * c.quantity
                try:
                    favourite_product = Favorite.objects.filter(product=c.product, customer=request.user)
                    if favourite_product.count() > 0:
                        favourite_status = 1
                except:
                    pass
                if c.product.is_publish == False or c.product.quantity == 0:
                    c.delete()
                    return redirect('cart')

                if c.product.product.is_discountprice == True:
                    total_discount_price = c.product.product.discountprice * c.quantity
                    total_price = c.product.product.price * c.quantity
                    minus = total_price - total_discount_price

            if total_price > setting.free_shipping:
                delivery_price = 0
            else:
                delivery_price = setting.shipping_price

            general_total = total_price + delivery_price

            context.update({
                'all_address': all_address,
                'address': address,
                'total_count': total_count,
                'total_price': total_price,
                'delivery_price': delivery_price,
                'minus': minus,
                'general_total': general_total,
            })

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            cartitem_count = CartItem.objects.filter(cart=cart, is_active=True).count()

        if request.is_ajax():
            status = request.POST.get('status')
            if status == 'ok':
                yr = int(date.today().strftime('%Y'))
                dt = int(date.today().strftime('%d'))
                mt = int(date.today().strftime('%m'))
                d = date(yr, mt, dt)
                current_date = d.strftime("%y%m%d")
                order_number = 'SN' + current_date + random.randint(1, 9999999).__str__()
                request.session['order_number'] = order_number
                return JsonResponse(data='ok', status=200, safe=False)

    except Cart.DoesNotExist:
        pass
    context.update({
        'cart_items': cart_items,
        'cartitem_count': cartitem_count,
        'cart': cart,
        'favourite_status': favourite_status,
        'products': products,
        'add_form': add_form,
    })

    return render(request, 'frontend/v_2_0/sayfalar/sepet/sepet.html', context)


def uses_coupon(request):
    user_coupon = Coupon.objects.filter(user=request.user)
    data = ''

    if request.method == 'POST':
        code = request.POST.get('code')
        for user_c in user_coupon:
            if user_c.coupon_code == code:
                coupon = Coupon.objects.get(coupon_code=code)
                data = {
                    'price': user_c.coupon_price,
                    'name': user_c.coupon_code,
                    'condition': user_c.coupon_conditional,
                }

                active_coupon = Coupon.objects.filter(is_active=True)
                for u in active_coupon:
                    u.is_active = False
                    u.save()

                coupon.is_active = True
                coupon.save()
                break
            else:
                data = {
                    'none': 'none'
                }
        return JsonResponse({'data': data})


def delete_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            coupon = Coupon.objects.get(coupon_code=code)
            coupon.is_active = False
            coupon.save()
        except:
            pass
    return JsonResponse({'data': 'deleted'})


@login_required(login_url="/giris-yap")
def checkout(request):
    context = {}
    items = []
    total = 0
    grand_total = 0
    total_quantity = 0
    minus = 0
    delivery_price = 0
    order_number = request.session.get('order_number')
    cart_items = CartItem.objects.filter(user=request.user)

    # Sepette bulunan ürünlerin getirilmesi
    for i in cart_items:
        if i.product.product.is_discountprice == True:
            items.append([str(i.product.title).replace("İ", "I").replace("ş", "s").replace("ü", "u").replace("Ş",
                                                                                                             "S").replace(
                "Ü", "U").replace("ğ", "g").replace("ç", "c").replace("Ç", "C").replace("ö", "o").replace("Ö", "O"),
                          str(i.product.discountprice), i.quantity])
        else:
            items.append([(i.product.title).replace("İ", "I").replace("ş", "s").replace("ü", "u").replace("Ş",
                                                                                                          "S").replace(
                "Ü", "U").replace("ğ", "g").replace("ç", "c").replace("Ç", "C").replace("ö", "o").replace("Ö", "O"),
                          float(i.product.product.price), i.quantity])

    add_form = AddressForm(data=request.POST or None, files=request.FILES or None)

    # Aktif adres kontrolü
    all_address = CustomerAddress.objects.all().filter(user=request.user)
    try:
        active_address = CustomerAddress.objects.get(user=request.user, is_active="Evet")
    except:
        messages.warning(request, 'Kayıtlı aktif adresiniz bulunmamaktadır. Adres eklemeniz gerekmektedir.')
        return redirect('address')

    # Kupon kullanıldı ise kuponun getirilmesi
    coupon = None
    coupon_exist = Coupon.objects.filter(user=request.user, is_active=True).exists()
    try:
        coupon = Coupon.objects.get(user=request.user, is_active=True)
    except:
        pass

    try:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        setting = Setting.objects.filter().last()

        for cart_item in cart_items:
            if cart_item.product.product.is_discountprice:
                total += (float(cart_item.product.product.discountprice) * cart_item.quantity)
            else:
                total += (float(cart_item.product.product.price) * cart_item.quantity)

            if total < setting.free_shipping:
                if coupon_exist == True:
                    grand_total = total + float(setting.shipping_price) - float(coupon.coupon_price)
                else:
                    grand_total = total + float(setting.shipping_price)
                delivery_price = setting.shipping_price
            else:
                if coupon_exist == True:
                    grand_total = total - float(coupon.coupon_price)
                else:
                    grand_total = total

            if cart_item.product.product.is_discountprice == True:
                total_discount_price = cart_item.product.product.discountprice * cart_item.quantity
                total_price = cart_item.product.product.price * cart_item.quantity
                minus = total_price - total_discount_price

            total_quantity += cart_item.quantity
            context.update({
                'total': total,
                'grand_total': grand_total,
                'total_quantity': total_quantity,
                'minus': minus
            })

    except:
        pass

    get_user = get_object_or_404(User, id=request.user.id)

    if get_user.mobile:
        get_user_mobile = get_user.mobile
    else:
        get_user_mobile = '05426561106'

    fullname = request.user.get_full_name()
    if fullname == '' or fullname == None:
        fullname = "TredyShop Alışveriş"

    user_ip = request.META.get('REMOTE_ADDR')
    if settings.DEBUG == True:
        user_ip = '213.238.183.81'
    else:
        user_ip = user_ip
    email = request.user.email

    if email == '' or email == None:
        email = "siparis@tredyshop.com"

    address = f"{active_address.address} {active_address.neighbourhood} Mah. / {active_address.county} / {active_address.city}"

    paytr_data = paytr_api(email=email, payment_amount=float(grand_total), merchant_oid=str(order_number),
                           full_name=fullname, address=address,
                           mobile=get_user_mobile, item=items, ip=user_ip, installment_count="0")

    all_taksit_data = paytr_taksit_sorgu()
    taksitler = []
    taksitler.append({
        "taksit_sayisi": "Tek Çekim",
        "vadeli_fiyat": grand_total,
    })
    brand = None
    if request.is_ajax():
        bin_code = request.GET.get('bin_code')
        try:
            order = Order.objects.get(order_number=order_number, user=request.user)
            order.status = 'Ödeme Yapılmadı'
            order.save()
        except Order.DoesNotExist:
            order = Order.objects.create(order_number=order_number, user=request.user, order_amount=grand_total,
                                         order_total=grand_total, order_platform="TredyShop",
                                         paymenttype="Banka/Kredi Kartı", address=CustomerAddress.objects.get(user=request.user, is_active="Evet"),
                                         status="Ödeme Yapılmadı", delivery_price=delivery_price)

            cart_items = CartItem.objects.filter(user=request.user, is_active=True)

            for item in cart_items:
                o_product_price = item.product.product.price
                if item.product.product.is_discountprice:
                    o_product_price = item.product.product.discountprice
                item_price = o_product_price
                item_weight = float(item_price) / (float(order.order_amount) - float(order.delivery_price))
                forward_sale = order.order_total * item_weight
                orderproduct = OrderProduct.objects.create(order=order, user=request.user, product=item.product,
                                                           title=item.product.title, product_slug=item.product.slug,
                                                           quantity=item.quantity, size=item.product.size.name,
                                                           color=item.product.color.name,
                                                           product_price=o_product_price, forward_sale=forward_sale)
        try:
            bank = bin_sorgu(bin_code)
            brand = bank['brand']
            brand_taksit_rates = all_taksit_data[brand]

            for taksit_orani in brand_taksit_rates:
                vadeli_hesaplama = taksit_hesaplama(paymant_amount=grand_total, vade=taksit_orani.split("_")[1],
                                                    faiz=brand_taksit_rates[taksit_orani])
                taksitler.append({
                    "taksit_sayisi": taksit_orani.split("_")[1],
                    "vadeli_fiyat": vadeli_hesaplama,
                })
        except:
            taksitler.append({
                "taksit_sayisi": "Tek Çekim",
                "vadeli_fiyat": grand_total,
            })
        return JsonResponse(data=[taksitler, brand], safe=False)

    paytr_form_action = "https://www.paytr.com/odeme"

    context.update(
        {'cart_items': cart_items, 'total': total, 'grand_total': grand_total, 'coupon': coupon,
         'address': active_address, 'add_form': add_form, 'all_address': all_address,
         'paytr_data': paytr_data, 'taksitler': taksitler, 'paytr_form_action': paytr_form_action})

    return render(request, 'frontend/v_2_0/sayfalar/sepet/odeme.html', context)


def order_token(request):
    user_ip = request.POST.get('user_ip')
    merchant_oid = request.POST.get('merchant_oid')
    email = request.POST.get('email')
    payment_amount = request.POST.get('payment_amount')
    installment_count = request.POST.get('installment_count')
    token = create_order_token(user_ip=user_ip, email=email, merchant_oid=merchant_oid, payment_amount=payment_amount,
                               installment_count=installment_count)
    data = token
    return JsonResponse(data=data, safe=False)


def contracts(request):
    data = 'success'
    user_id = request.user.id
    order_number = request.POST.get('order_number')
    try:
        order = Order.objects.get(user=request.user, order_number=order_number)

        preliminary_form = request.POST.get('preliminary_form')
        distance_selling_contract = request.POST.get('distance_selling_contract')

        order.distance_selling_contract = distance_selling_contract
        order.preliminary_information_form = preliminary_form

        order.save()
    except Order.DoesNotExist:
        pass

    return JsonResponse(data=data, safe=False)


@csrf_exempt
def callback(request):
    if request.method != 'POST':
        return HttpResponse(str('OK'))

    post = request.POST

    merchant_key = b'xXWCLan3y1m97K4u'
    merchant_salt = b'3yfMDbiraNXoG311'

    order_number = post['merchant_oid']
    order_total = float(float(post['total_amount']) / 100)

    if post['status'] == 'success':
        return HttpResponse(str('OK'))
    else:
        return HttpResponse(str('OK'))


def completed_checkout(request, order_number):
    context = {}

    try:
        sorgu_durum = paytr_sorgu(order_number=order_number)
        taksit_durum = False
        if int(sorgu_durum['taksit']) != 0:
            taksit_durum = True
        order = Order.objects.get(order_number=order_number)
        total = 0
        order_list = OrderProduct.objects.filter(order__order_number=order_number)
        for p in order_list:
            total += (float(p.quantity * p.product_price))

        customerTredyShopCreateOrder(request=request, email=request.user.email, address=order.address.address,
                                     order=order[1], order_list=order_list,
                                     total=total, grand_total=float(sorgu_durum['payment_total']))
        sendOrderInfoEmail(email="atmacaahmet5261@hotmail.com", platform="TredyShop", order=order[1])

        if sorgu_durum == 'success':
            order.status = 'Yeni'
            cart_items = CartItem.objects.filter(user=request.user)
            for cart_item in cart_items:
                cart_item.delete()
        elif sorgu_durum == 'failed':
            return redirect('payment_failed')
        context.update({
            'order': order[1],
        })
    except Order.DoesNotExist:
        return redirect("cart")

    return render(request, 'frontend/v_2_0/sayfalar/sepet/basarili_sonuc.html', context)


def payment_failed(request):
    return render(request, 'frontend/v_2_0/sayfalar/sepet/basarisiz_sonuc.html')


def select_address(request, address_id):
    try:

        address = CustomerAddress.objects.get(id=address_id)

        user_address = CustomerAddress.objects.filter(is_active="Evet").exclude(id=address_id)
        for u in user_address:
            u.is_active = "Hayır"
            u.save()
        address.is_active = "Evet"
        address.save()
        messages.success(request, 'Adresiniz seçildi. Ödeme işlemine devam edebilirsiniz.')
        return redirect('checkout')
    except:
        messages.warning(request, 'Adresiniz seçilemedi. Tekrar deneyiniz.')
        return redirect('checkout')
