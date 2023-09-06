import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
import random
from adminpage.models import Notification
from carts.helpers import paytr_api, card_type, paytr_iframe
from customer.forms import AddressForm
from customer.models import CustomerAddress, Bonuses, Coupon
from ecommerce.settings import EMAIL_HOST_USER
from mainpage.models import Setting
from carts.models import Cart, CartItem
from orders.models import Order, OrderProduct, BankInfo, PreOrder
from product.models import *
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
import base64
import hashlib
import hmac
from django.shortcuts import render, HttpResponse


# Create your views here.
def add_cart(request, product_id):
    quantity = int(request.GET.get('quantity', 1))
    data = {'is_active': 'is_active'}
    is_active = False
    url = request.META.get('HTTP_REFERER')
    variantid = request.GET.get('variantid')
    product = Product.objects.get(id=product_id, is_publish=True)  # get the product
    same_product = 0

    if request.user.is_authenticated:
        if product.variant != 'Yok':
            checkvariant = CartItem.objects.filter(variant_id=variantid, user_id=request.user.id)
            if checkvariant:
                control = 1
            else:
                control = 2
        else:
            checkinproduct = CartItem.objects.filter(product_id=product_id, user_id=request.user.id)
            if checkinproduct:
                control = 1
            else:
                control = 2

        if request.method == 'GET':
            if control == 1:
                if product.variant == 'Yok':
                    data = CartItem.objects.get(product_id=product_id, user_id=request.user.id)
                    same_product = 1
                else:
                    data = CartItem.objects.get(product_id=product_id, variant_id=variantid, user_id=request.user.id)
                    same_product = 1
                data.quantity += quantity
                try:
                    cart = Cart.objects.get(
                        cart_id=request.user.id)
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=request.user.id)
                cart.save()
                data.save()
            else:
                same_product = 2
                try:
                    cart = Cart.objects.get(
                        cart_id=request.user.id)
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=request.user.id)
                cart.save()
                data = CartItem()
                data.user = request.user
                data.product_id = product_id
                data.variant_id = variantid
                data.cart = cart
                data.quantity = quantity
                data.save()
            return JsonResponse({'data': 'added', 'plus': '1', 'control': control, 'same_product': same_product})

        else:  # if there is no post
            if control == 1:
                data = CartItem.objects.get(product_id=product_id, user_id=request.user.id)
                data.quantity += 1
                try:
                    cart = Cart.objects.get(
                        cart_id=request.user.id)
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=request.user.id)
                cart.save()
                data.save()
            else:
                try:
                    cart = Cart.objects.get(
                        cart_id=request.user.id)
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=request.user.id)
                cart.save()
                data = CartItem()
                data.user = request.user
                data.product_id = product_id
                data.variant_id = variantid
                data.quantity = 1
                data.cart = cart
                data.variant_id = None
                data.save()
            return JsonResponse({'data': 'added', 'plus': '2'})

    else:
        try:
            cart = Cart.objects.get(
                cart_id=request.user.id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=request.user.id)

        if product.variant != 'Yok':
            checkvariant = CartItem.objects.filter(variant_id=variantid, cart=cart)
            if checkvariant.count() > 0:
                control = 1
            else:
                control = 2
        else:
            checkinproduct = CartItem.objects.filter(product_id=product_id, cart=cart)
            if checkinproduct:
                control = 1
            else:
                control = 2
        if request.method == 'GET':
            if control == 1:
                if product.variant == 'Yok':
                    data = CartItem.objects.get(product_id=product_id, cart=cart)
                else:
                    data = CartItem.objects.get(product_id=product_id, variant_id=variantid,
                                                cart=cart)
                data.quantity += quantity
                try:
                    cart = Cart.objects.get(
                        cart_id=request.user.id)
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=request.user.id)
                cart.save()
                data.save()
            else:
                try:
                    cart = Cart.objects.get(
                        cart_id=request.user.id)
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=request.user.id)
                cart.save()
                data = CartItem()
                data.product_id = product_id
                data.variant_id = variantid
                data.cart = cart
                data.quantity = quantity
                data.save()
            return JsonResponse({'data': 'added', 'plus': '3'})
        else:  # if there is no post
            if control == 1:
                data = CartItem.objects.get(product_id=product_id, cart=cart)
                data.quantity += 1
                try:
                    cart = Cart.objects.get(
                        cart_id=request.user.id)
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=request.user.id)
                cart.save()
                data.save()
            else:
                try:
                    cart = Cart.objects.get(
                        cart_id=request.user.id)
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=request.user.id)
                cart.save()
                data = CartItem()
                data.product_id = product_id
                data.quantity = 1
                data.cart = cart
                data.variant_id = None
                data.save()
            return JsonResponse({'data': 'added', 'plus': '4'})


def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=request.user.id)
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id, user=request.user)
        cart_item.delete()
        return redirect('cart')
    except:
        pass
    return redirect('cart')


def minus_quantity(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=request.user.id)
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return redirect('cart')
    except:
        pass
    return redirect('cart')


def plus_quantity(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=request.user.id)
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id, user=request.user)
        if cart_item.product.variant != 'Yok':
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            if cart_item.quantity == cart_item.variant.quantity:
                cart_item.quantity = cart_item.variant.quantity
                cart_item.save()
                messages.warning(request,
                                 'Malasef stoklarımızda ilgili üründen daha fazla bulunmadığından artış yapılamamıştır.')
                return redirect('cart')
            else:
                cart_item.quantity += 1
                cart_item.save()
        else:
            if cart_item.quantity == cart_item.product.amount:
                cart_item.quantity = cart_item.product.amount
            else:
                cart_item.quantity += 1
                cart_item.save()
        return redirect('cart')
    except:
        pass
    return redirect('cart')


@login_required(login_url="/giris-yap")
def cart(request, total=0, general_total=0, quantity=0, cart_items=None):
    query = None
    context = {}
    cart = None
    coupon = None
    coupon_exist = False

    try:
        all_address = CustomerAddress.objects.all().filter(user=request.user, is_active="Hayır")
        add_form = AddressForm(data=request.POST or None, files=request.FILES or None)

        try:
            address = CustomerAddress.objects.get(is_active="Evet", user=request.user)
        except:
            address = None

        context.update({
            'add_form': add_form,
            'all_address': all_address,
            'address': address
        })

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
                        data.user = request.user
                        data.save()
                        messages.success(request, 'Adres başarıyla eklendi.')
                        return redirect('cart')
                    else:
                        messages.error(request, 'T.C. Kimlik Numarası 11 basamaklı olmalıdır.')
                        return redirect('cart')
                if type == "Kurumsal":
                    if current_address == "Evet":
                        user_address = CustomerAddress.objects.filter(is_active="Evet")
                        for u in user_address:
                            u.is_active = "Hayır"
                            u.save()

                    data = add_form.save(commit=False)
                    data.tc = None
                    data.user = request.user
                    data.save()
                    messages.success(request, 'Adres başarıyla eklendi.')
                    return redirect('cart')

        setting = Setting.objects.filter().last()

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)

            coupon_exist = Coupon.objects.filter(user=request.user, is_active=True).exists()
            try:
                coupon = Coupon.objects.get(user=request.user, is_active=True)
                if cart_items.count() == 0:
                    coupon.is_active = False
                    coupon.save()
            except:
                pass

        if cart_items.count() > 0:

            for cart_item in cart_items:
                if cart_item.product.variant != 'Yok':
                    variants = Variants.objects.filter(product_id=cart_item.product.id)
                    variant = Variants.objects.get(id=variants[1].id)

                    if cart_item.variant.quantity < cart_item.quantity:
                        cart_item.quantity = cart_item.variant.quantity
                        cart_item.save()

                    if cart_item.variant.is_discountprice == True:
                        total += (round(float(cart_item.variant.discountprice), 2) * cart_item.quantity)
                    else:
                        total += (round(float(cart_item.variant.price), 2) * cart_item.quantity)
                    quantity += cart_item.quantity
                    if total < setting.free_shipping:
                        if coupon_exist == True:
                            general_total = float(total) + float(setting.shipping_price) - float(coupon.coupon_price)
                        else:
                            general_total = float(total) + float(setting.shipping_price)
                    else:
                        if coupon_exist == True:
                            general_total = float(total) - float(coupon.coupon_price)
                        else:
                            general_total = total

                    context.update({
                        'variant': variant,
                        'total': total,
                    })

                else:
                    if cart_item.product.is_discountprice == True:
                        total += float(cart_item.product.discountprice) * int(cart_item.quantity)
                    else:
                        total += float(cart_item.product.price) * cart_item.quantity
                    quantity += cart_item.quantity

                    if total < setting.free_shipping:
                        if coupon_exist == True:
                            general_total = float(total) + float(setting.shipping_price) - float(coupon.coupon_price)
                        else:
                            general_total = float(total) + float(setting.shipping_price)
                    else:
                        if coupon_exist == True:
                            general_total = float(total) + float(setting.shipping_price) - float(coupon.coupon_price)
                        else:
                            general_total = total


    except Cart.DoesNotExist:
        pass

    context.update({
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'general_total': general_total,
        'coupon': coupon,
    })

    return render(request, 'frontend/pages/carts.html', context)


def submitCheckout(request):
    addres_id = request.POST.get('addres_id')
    approved = request.POST.get('approved')
    coupon = request.POST.get('coupon')
    delivery_price = request.POST.get('delivery_price')
    preliminary_form = request.POST.get("preliminary_form")
    distance_selling_form = request.POST.get("distance_selling_form")

    data = 'failed'
    if addres_id and approved == 'True':
        address = CustomerAddress.objects.get(id=addres_id)
        cart = Cart.objects.get(cart_id=request.user.id)

        if PreOrder.objects.filter(user=request.user, cart=cart).count() < 1:
            if coupon:
                pre_order = PreOrder.objects.create(user=request.user, delivery_address=address, coupon=coupon,
                                                    cart=cart, delivery_price=delivery_price,
                                                    approved_contract=True,
                                                    preliminary_information_form=preliminary_form,
                                                    distance_selling_contract=distance_selling_form)
            else:
                pre_order = PreOrder.objects.create(user=request.user, delivery_address=address, cart=cart,
                                                    approved_contract=True,
                                                    preliminary_information_form=preliminary_form,
                                                    delivery_price=delivery_price,
                                                    distance_selling_contract=distance_selling_form)
        else:
            pre_order = PreOrder.objects.get(user=request.user, cart=cart)
            pre_order.delivery_address = address
            pre_order.save()
        data = 'success'

    return JsonResponse(data=data, safe=False)


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
def createOrder(request, order_number, order_total, status):
    cart = Cart.objects.get(cart_id=request.user.id)
    pre_order = PreOrder.objects.get(cart=cart)
    user = pre_order.user
    ip = request.META.get('REMOTE_ADDR')
    address = pre_order.delivery_address
    coupon = pre_order.coupon
    delivery_price = pre_order.delivery_price
    preliminary_form = pre_order.preliminary_information_form
    distance_selling_form = pre_order.distance_selling_contract

    data = Order.objects.create(order_number=str(order_number), user=user, address_id=address.id,
                                order_total=float(order_total),
                                delivery_price=delivery_price, is_ordered=True, approved_contract=True,
                                ip=ip, status=status,
                                paymenttype='Banka/Kredi Kartı', preliminary_information_form=preliminary_form,
                                distance_selling_contract=distance_selling_form)

    if coupon != '' and coupon != None:
        used_coupon = float(coupon)
        data.used_coupon = used_coupon
        coupon.delete()

    data.save()
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        if item.product.variant != 'Yok':
            orderproduct = OrderProduct()
            orderproduct.order = data
            orderproduct.user = pre_order.user
            orderproduct.product = item.variant.product
            orderproduct.variation = item.variant
            orderproduct.color = item.variant.color
            orderproduct.size = item.variant.size
            orderproduct.quantity = item.quantity
            if item.variant.is_discountprice == True:
                orderproduct.product_price = item.variant.discountprice
            else:
                orderproduct.product_price = item.variant.price
            orderproduct.ordered = True
            orderproduct.save()

            variant = Variants.objects.get(id=item.variant.id)
            product = Product.objects.get(id=item.product.id)
            variant.quantity -= item.quantity
            variant.sell_count += item.quantity
            product.sell_count += item.quantity
            product.save()
            if variant.quantity <= 0:
                variant.is_publish = False
            variant.save()

        else:
            orderproduct = OrderProduct()
            orderproduct.order = data
            orderproduct.user = pre_order.user
            orderproduct.product = item.product
            orderproduct.quantity = item.quantity
            if item.product.is_discountprice == True:
                orderproduct.product_price = item.product.discountprice
            else:
                orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            product = Product.objects.get(id=item.product.id)
            product.amount -= item.quantity
            product.sell_count += item.quantity
            if product.amount <= 0:
                product.is_publish = False
            product.save()
    cart = Cart.objects.get(cart_id=pre_order.user.id)
    cart.delete()

    return data


@login_required(login_url="/giris-yap")
def checkout(request, total=0, cart_items=None):
    context = {}
    grand_total = 0
    items = []
    pre_order = None

    cart_items = CartItem.objects.filter(user=request.user)
    for i in cart_items:
        if i.product.is_discountprice == True:
            items.append([str(i.product.title), str(i.product.discountprice), i.quantity])
        else:
            items.append([i.product.title, float(i.product.price), i.quantity])

    yr = int(datetime.date.today().strftime('%Y'))
    dt = int(datetime.date.today().strftime('%d'))
    mt = int(datetime.date.today().strftime('%m'))
    d = datetime.date(yr, mt, dt)
    current_date = d.strftime("%y%m%d")
    order_number = 'SN' + current_date + random.randint(1, 9999999).__str__()

    coupon = None
    coupon_exist = Coupon.objects.filter(user=request.user, is_active=True).exists()

    try:
        coupon = Coupon.objects.get(user=request.user, is_active=True)
    except:
        pass

    try:
        cart = Cart.objects.get(cart_id=request.user.id)
        pre_order = PreOrder.objects.get(user=request.user, cart=cart)
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        setting = Setting.objects.filter().last()
        for cart_item in cart_items:
            if cart_item.product.variant != 'Yok':
                variants = Variants.objects.filter(product_id=cart_item.product.id)
                variant = Variants.objects.get(id=variants[0].id)
                if cart_item.variant.is_discountprice:
                    total += (float(cart_item.variant.discountprice) * cart_item.quantity)
                else:
                    total += (float(cart_item.variant.price) * cart_item.quantity)

                context.update({
                    'variant': variant,
                    'total': total,
                })

            else:
                if cart_item.product.is_discountprice:
                    total += (float(cart_item.product.discountprice) * cart_item.quantity)
                else:
                    total += (float(cart_item.product.price) * cart_item.quantity)

            if total < setting.free_shipping:
                if coupon_exist == True:
                    grand_total = total + float(setting.shipping_price) - float(coupon.coupon_price)
                else:
                    grand_total = total + float(setting.shipping_price)
            else:
                if coupon_exist == True:
                    grand_total = total - float(coupon.coupon_price)
                else:
                    grand_total = total
        pre_order = PreOrder.objects.get(cart=cart)
        pre_order.cart_total = grand_total
        pre_order.save()
    except ObjectDoesNotExist:
        pass

    get_user = get_object_or_404(User, id=request.user.id)
    get_user_mobile = None
    if get_user.mobile:
        get_user_mobile = get_user.mobile
    else:
        get_user_mobile = '05426561106'

    token = paytr_iframe(email=request.user.email, payment_amount=grand_total, merchant_oid=str(order_number),
                         fullname=f"{request.user.get_full_name()}",
                         address=f"{pre_order.delivery_address.address} {pre_order.delivery_address.neighbourhood} Mah. / {pre_order.delivery_address.county} / {pre_order.delivery_address.city}",
                         mobile=get_user_mobile, item=items, ip=request.META.get('REMOTE_ADDR'),
                         installment_option=True)

    context.update(
        {'cart_items': cart_items, 'total': total, 'grand_total': grand_total, 'coupon': coupon, 'token': token,
         'pre_order': pre_order})
    return render(request, 'frontend/pages/checkout.html', context)


@csrf_exempt
def callback(request):
    if request.method != 'POST':
        return HttpResponse(str('OK'))

    post = request.POST

    merchant_key = b'xXWCLan3y1m97K4u'
    merchant_salt = b'3yfMDbiraNXoG311'

    # if Order.objects.filter(order_number=post['merchant_oid']).exists():
    #    order = get_object_or_404(Order, order_number=post['merchant_oid'])
    #    order.order_total = float(post['total_amount'])
    #    return HttpResponse(str('OK'))

    order_number = post['merchant_oid']
    order_total = float(float(post['total_amount']) / 100)

    if post['status'] == 'success':
        return HttpResponse(str('OK'))
    else:
        return HttpResponse(str('OK'))


def completed_checkout(request, order_number):
    context = {}

    if Order.objects.filter(order_number=order_number).exists():
        order = Order.objects.get(order_number=order_number)
        context.update({
            'order': order,
        })

    else:
        cart = Cart.objects.get(cart_id=request.user.id)
        pre_order = PreOrder.objects.get(cart=cart)
        cart_total = pre_order.cart_total
        order = createOrder(request, order_number=str(order_number), order_total=cart_total, status="Yeni")
        context.update({
            'order': order,
        })

    return render(request, 'frontend/pages/completed_checkout.html', context)


def payment_failed(request):
    return render(request, 'frontend/partials/odeme_basarisiz.html')


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
        return redirect('cart')
    except:
        messages.warning(request, 'Adresiniz seçilemedi. Tekrar deneyiniz.')
        return redirect('cart')
