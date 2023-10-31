from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage

from adminpage.models import Notification
from carts.models import Cart, CartItem
from customer.forms import *
from customer.models import CustomerAddress
from ecommerce.settings import EMAIL_HOST_USER
from orders.models import Order, OrderProduct, ExtraditionRequest, ExtraditionRequestResult, \
    CancellationRequest
from user_accounts.models import User
from product.models import Favorite, ReviewRating, Question, ApiProduct


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
                        messages.success(request,
                                         f'Hoşgeldin {request.user.get_full_name()}. Alışveriş keyfini çıkarın.')
                        return redirect('mainpage')

                    else:
                        messages.warning(request,
                                         "Hesap etkinleştirilmemiştir. Lütfen kayıtlı e-posta adresinize gönderilen mail üzerindeki linke tıklayarak hesabınızı etkinleştiriniz.")
                        return redirect('mainpage')
                else:
                    messages.warning(request, "E-posta veya şifre hatalı. Lütfen tekrar deneyiniz.")
                    return redirect('login')
        return render(request, 'frontend/pages/login.html')
    except Exception as e:
        return redirect('login')


def register(request):
    try:
        if request.user.is_authenticated:
            messages.success(request, 'Giriş yapıldı')
            return redirect('mainpage')
        if 'register_btn' in request.POST:
            if request.method == 'POST':
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                mobile = request.POST.get('mobile')
                password = request.POST.get('password')
                user_obj = User.objects.filter(email=email)
                if user_obj.exists():
                    messages.error(request, 'Bu kullanıcı zaten mevcuttur!')
                    return redirect('login')
                if first_name != '' and last_name != '' and email != '' and mobile != '' and password != '':
                    user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                                    password=password,
                                                    mobile=mobile, is_customer=True)
                    try:
                        current_site = get_current_site(request)
                        from_email = EMAIL_HOST_USER
                        mail_subject = "Lütfen hesabınızı aktif ediniz."
                        message = render_to_string("frontend/acccounts/account_verification_email.html", {
                            'user': user,
                            'domain': current_site,
                            'uid': urlsafe_base64_encode(force_bytes(user.id)),
                            'token': default_token_generator.make_token(user),
                        })
                        to_email = email
                        send_email = EmailMessage(mail_subject, message, to=[to_email])
                        send_email.send()
                    except Exception as e:
                        pass

                    notify = Notification.objects.create(noti_type="8", customer=user,
                                                         title="Yeni müşteri kaydı yapıldı.",
                                                         detail="Yeni müşteri kaydı yapıldı.")
                    messages.success(request,
                                     'Tebrikler üyeliğiniz başarıyla oluşturuldu. E-Posta adresinize gelen link üzerinden üyeliğinizi aktif edebilirsiniz. Spam klasörünü kontrol etmeyi unutmayınız. Keyifli alışverişler dileriz.')
                    return redirect('login')
                messages.warning(request, 'Yanlış şifre!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, 'frontend/pages/register.html')
    except Exception as e:
        print(e)
        messages.warning(request, 'Bir hata meydana geldi!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_activated = True
        user.save()
        messages.success(request, "Tebrikler! Hesabınız aktif edilmiştir. Keyifli alışverişler dileriz.")
        return redirect('login')
    else:
        messages.error(request, "Geçersiz aktivasyon linki!")
        return redirect('register')


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

    if 'changePasswordBtn' in request.POST:
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        flag = check_password(current_password, request.user.password)

        if flag:
            haspass = make_password(new_password)
            request.user.password = haspass
            request.user.save()
            messages.success(request, 'Şifreniz başarıyla değiştirildi. Tekrar giriş yapmanız gerekmektedir.')
            return redirect('authenticated_page')

    return render(request, 'frontend/pages/profile/mainpage.html')


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
    return render(request, 'frontend/pages/profile/address.html', context)


def load_counties(request):
    city_id = request.GET.get('city_id')
    counties = County.objects.filter(city_id=city_id)
    return render(request, 'frontend/pages/profile/partials/dropdown_ilceler.html', {'counties': counties})


@login_required(login_url="/giris-yap")
def update_address(request, id):
    context = {}
    address = CustomerAddress.objects.get(id=id)
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

    return render(request, 'frontend/pages/profile/update_address.html', context)


@login_required(login_url="/giris-yap")
def delete_address(request, id):
    address = CustomerAddress.objects.get(id=id)
    address.delete()
    messages.success(request, 'Adres başarıyla silindi.')
    return redirect('address')


@login_required(login_url="/giris-yap")
def wishlist(request):
    context = {}

    favourite_products = Favorite.objects.filter(customer=request.user)
    context.update({
        'favourite_products': favourite_products
    })

    return render(request, 'frontend/pages/profile/wishlist.html', context)


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
    return render(request, 'frontend/pages/profile/reviews.html', context)


@login_required(login_url="/giris-yap")
def order_page(request):
    context = {}
    orders = Order.objects.filter(user=request.user)
    orders_count = Order.objects.filter(user=request.user).count()
    context.update({
        'orders': orders,
        'orders_count': orders_count
    })
    return render(request, 'frontend/pages/profile/orders.html', context)


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
        product = ApiProduct.objects.get(id=product_id)
        orderproduct = OrderProduct.objects.get(order=order, product=product)
        extradition = ExtraditionRequest.objects.create(order=order, user=request.user,
                                                        extradition_type=extradition_type, description=desc,
                                                        product=product)
        orderproduct.is_extradation = True
        orderproduct.save()
        messages.success(request, 'Ürün iade talebi iletildi.')
        return redirect('order_detail', order_number)
    return render(request, 'frontend/pages/profile/order_detail.html', context)



@login_required(login_url="/giris-yap")
def cancellig_order_product(request, order_number, product_id):
    order = Order.objects.get(order_number=order_number)
    product = ApiProduct.objects.get(id=product_id)
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
    return render(request, 'frontend/pages/profile/coupons.html', context)


@login_required(login_url="/giris-yap")
def question_page(request):
    context = {}
    question = Question.objects.filter(user=request.user)
    question_count = Question.objects.filter(user=request.user).count()

    context.update({
        'question': question,
        'question_count': question_count,
    })
    return render(request, 'frontend/pages/profile/question.html', context)
