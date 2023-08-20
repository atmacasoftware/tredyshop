import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from customer.forms import AddressForm
from customer.models import CustomerAddress, Bonuses, Coupon
from mainpage.models import Setting
from carts.models import Cart, CartItem
from orders.models import Order, OrderProduct, BankInfo
from product.models import *


# Create your views here.
def add_cart(request, product_id):
    quantity = int(request.GET.get('quantity', 1))
    print(quantity)
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
                        cart_id=request.META.get('REMOTE_ADDR'))
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=request.META.get('REMOTE_ADDR'))
                cart.save()
                data.save()
            else:
                same_product = 2
                try:
                    cart = Cart.objects.get(
                        cart_id=request.META.get('REMOTE_ADDR'))
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=request.META.get('REMOTE_ADDR'))
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
                        cart_id=request.META.get(
                            'REMOTE_ADDR'))  # get the cart using the cart_id present in the session
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=request.META.get('REMOTE_ADDR'))
                cart.save()
                data.save()
            else:
                try:
                    cart = Cart.objects.get(
                        cart_id=request.META.get(
                            'REMOTE_ADDR'))  # get the cart using the cart_id present in the session
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=request.META.get('REMOTE_ADDR'))
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
                cart_id=request.META.get('REMOTE_ADDR'))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=request.META.get('REMOTE_ADDR'))

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
                        cart_id=request.META.get('REMOTE_ADDR'))
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=request.META.get('REMOTE_ADDR'))
                cart.save()
                data.save()
            else:
                try:
                    cart = Cart.objects.get(
                        cart_id=request.META.get('REMOTE_ADDR'))
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=request.META.get('REMOTE_ADDR'))
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
                        cart_id=request.META.get(
                            'REMOTE_ADDR'))  # get the cart using the cart_id present in the session
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=request.META.get('REMOTE_ADDR'))
                cart.save()
                data.save()
            else:
                try:
                    cart = Cart.objects.get(
                        cart_id=request.META.get(
                            'REMOTE_ADDR'))  # get the cart using the cart_id present in the session
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=request.META.get('REMOTE_ADDR'))
                cart.save()
                data = CartItem()
                data.product_id = product_id
                data.quantity = 1
                data.cart = cart
                data.variant_id = None
                data.save()
            return JsonResponse({'data': 'added', 'plus': '4'})


def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=request.META.get('REMOTE_ADDR'))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id, user=request.user)
        cart_item.delete()
        return redirect('cart')
    except:
        pass
    return redirect('cart')


def minus_quantity(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=request.META.get('REMOTE_ADDR'))
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
    cart = Cart.objects.get(cart_id=request.META.get('REMOTE_ADDR'))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id, user=request.user)
        if cart_item.product.variant != 'Yok':
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            if cart_item.quantity == cart_item.variant.quantity:
                cart_item.quantity = cart_item.variant.quantity
                cart_item.save()
                messages.warning(request, 'Malasef stoklarımızda ilgili üründen daha fazla bulunmadığından artış yapılamamıştır.')
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


def cart(request, total=0, general_total=0, quantity=0, cart_items=None):
    query = None
    context = {}
    cart = None
    coupon = None
    coupon_exist = False
    try:
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
        else:
            cart = Cart.objects.get(cart_id=request.META.get('REMOTE_ADDR'))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

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
def checkout(request, total=0, cart_items=None):
    context = {}
    address = None
    grand_total = 0

    bankaccounts = BankInfo.objects.all()

    coupon = None
    coupon_exist = Coupon.objects.filter(user=request.user, is_active=True).exists()
    try:
        address = CustomerAddress.objects.get(is_active="Evet", user=request.user)
    except:
        address = None

    try:
        coupon = Coupon.objects.get(user=request.user, is_active=True)
    except:
        pass

    try:
        cart = Cart.objects.get(cart_id=request.META.get('REMOTE_ADDR'))
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
    except ObjectDoesNotExist:
        pass

    all_address = CustomerAddress.objects.all().filter(user=request.user)
    add_form = AddressForm(data=request.POST or None, files=request.FILES or None)

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
                    return redirect('checkout')
                else:
                    messages.error(request, 'T.C. Kimlik Numarası 11 basamaklı olmalıdır.')
                    return redirect('checkout')
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
                return redirect('checkout')

    if 'paymentBtn' in request.POST:
        select_address = request.POST.get('selectedAddress')
        order_total = request.POST.get('order_total')
        delivery_price = request.POST.get('delivery_price')
        approved_contract = request.POST.get('approved_contract')
        approved_status = None
        payment_type = request.POST.get('payment_type')
        ip = request.META.get('REMOTE_ADDR')
        used_coupon = request.POST.get('used_coupon', None)
        preliminary_form = request.POST.get("preliminary_form")
        distance_selling_form = request.POST.get("distance_selling_form")
        cardholder = None
        cardnumber = None

        if select_address == '' or select_address == None:
            messages.warning(request,
                             'Adres seçimi yapılması gerekmektedir.')
            return redirect('checkout')

        if approved_contract == 'approved':
            approved_status = True
        else:
            approved_status = False

        if payment_type == 'Banka/Kredi Kartı':
            cardholder = request.POST.get('cardholder')
            cardnumber = request.POST.get('cardnumber')

            if cardholder == '' and cardnumber == '':
                messages.warning(request,
                                 'Ödeme yöntemi Banka/Kredi Kartı seçilmesinden dolayı kart bilgileri eksiksiz doldurulmalıdır.')
                return redirect('checkout')

        data = Order.objects.create(user=request.user, address_id=select_address,
                                    order_total=float(order_total.replace(',', '.')), cardholder=cardholder, delivery_price=delivery_price,
                                    cardnumber=cardnumber, is_ordered=True, approved_contract=approved_status, ip=ip,
                                    paymenttype=payment_type, preliminary_information_form=preliminary_form,distance_selling_contract=distance_selling_form)

        if used_coupon !='':
            used_coupon = float(used_coupon.replace(',', '.'))
            data.used_coupon = used_coupon
            coupon.delete()

        data.save()

        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%y%m%d")
        order_number = current_date + str(data.id)

        data.order_number = order_number
        data.save()

        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            if item.product.variant != 'Yok':

                orderproduct = OrderProduct()
                orderproduct.order = data
                orderproduct.user = request.user
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
                orderproduct.user = request.user
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

            item.delete()
        cart = Cart.objects.get(cart_id=request.META.get('REMOTE_ADDR'))
        cart.delete()
        return redirect('completed_checkout', data.order_number)

    context.update({'address': address, 'add_form': add_form, 'all_address': all_address, 'cart_items': cart_items,
                    'total': total, 'grand_total': grand_total, 'coupon': coupon, 'bankaccounts':bankaccounts})
    return render(request, 'frontend/pages/checkout.html', context)


def completed_checkout(request, order_number):
    try:
        context = {}
        order = Order.objects.get(order_number=order_number)
        if order.paymenttype == 'Banka/Kredi Kartı':
            cardnumber_first = order.cardnumber[:4]
            cardnumber_last = order.cardnumber[15:20]
            context.update({'cardnumber_first': cardnumber_first, 'cardnumber_last': cardnumber_last})

        context.update({
            'order': order
        })
        return render(request, 'frontend/pages/completed_checkout.html', context)
    except:
        return redirect('checkout')


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
