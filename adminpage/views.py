import json
import os
from math import ceil
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone, timedelta
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from adminpage.analtycs import initialize_analyticsreporting
from amazon.models import *
from carts.helpers import paytr_sorgu
from hepsiburada.api import HepsiburadaApiClient
from hepsiburada.models import *
from hepsiburada.services import HepsiburadaProductIntegrationService
from trendyol.api import TrendyolApiClient
from carts.models import CartItem
from mainpage.models import City, Slider
from trendyol.models import LogRecords, TrendyolMoreProductOrder
from trendyol.services import ProductIntegrationService, OrderIntegrationService
from adminpage.custom import exportExcel, exportPdf, readNotification, createNotification, notReadNotification, izinSor, \
    sendOrderInfoEmail, customerTredyShopDeliveryOrder
from adminpage.forms import *
from categorymodel.models import SubCategory, SubBottomCategory, MainCategory
from customer.models import CustomerAddress, Coupon
from ecommerce import settings
from orders.models import Order, ExtraditionRequest, OrderProduct, CancellationRequest
from product.models import Color, ApiProduct, ReviewRating, Favorite, FabricType, Height, Pattern, \
    ArmType, CollerType, WeavingType, MaterialType, HeelType, HeelSize, Pocket
from product.read_xml import modaymissaveXML2db, updateModaymisSaveXML2db, updateTahtakaleSaveXML2db, \
    tahtakaleSaveXML2db, notActiveModaymisProduct
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
import requests
from user_accounts.models import User
from product.update import *


def admin_login(request):
    try:
        if request.user.is_authenticated:
            messages.success(request, 'Giriş yapıldı')
            return redirect('mainpage')
        if 'loginBtn' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            remember = request.POST.get('remember_me')
            user_obj = User.objects.filter(email=email)
            if not user_obj.exists():
                messages.error(request, 'Bu kullanıcı mevcut değil.')
                return redirect('admin_login')
            user_obj = authenticate(email=email, password=password)
            if user_obj is not None:
                if User.objects.get(email=email, is_superuser=True):
                    auth_login(request, user_obj)
                    if not remember:
                        request.session.set_expiry(18000)
                    messages.success(request,
                                     f'Hoşgeldin {request.user.get_full_name()}.')
                    return redirect('admin_mainpage')
    except Exception as e:
        return redirect('admin_login')

    return render(request, 'backend/adminpage/pages/login.html')


@login_required(login_url="/yonetim/giris-yap/")
def user_info(request):
    if 'updateBtn' in request.POST:
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')

        try:
            user = get_object_or_404(User, id=request.user.id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.mobile = mobile
            user.save()
            messages.success(request,
                             'Hesap bilgileriniz başarıyla güncellenmiştir.')
            return redirect('user_info')
        except:
            messages.warning(request,
                             'Bir hata meydana geldi!')
            return redirect('user_info')
    return render(request, 'backend/adminpage/pages/user_info.html')


@login_required(login_url="/yonetim/giris-yap/")
def change_password(request):
    if 'changePasswordBtn' in request.POST:
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        re_password = request.POST.get('re_password')

        if new_password == re_password:
            flag = check_password(current_password, request.user.password)
            if flag:
                haspass = make_password(new_password)
                request.user.password = haspass
                request.user.save()
                messages.success(request, 'Şifreniz başarıyla değiştirildi.')
                return redirect('admin_change_password')
        else:
            messages.warning(request, 'Yeni şifre ve şifre tekrar aynı olmalıdır.')
            return redirect('admin_change_password')
    return render(request, 'backend/adminpage/pages/change_password.html')


@login_required(login_url="/yonetim/giris-yap/")
def mainpage(request):
    context = {}
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    product_count = ApiProduct.objects.all().count()
    user_count = User.objects.all().count()
    order_count = Order.objects.all().count() + TrendyolOrders.objects.all().count()
    delivery_product = Order.objects.all().exclude(status="Kargolandı").count()
    sold_out_product_count = ApiProduct.objects.filter(quantity=0).count()
    trendyol_product_count = ApiProduct.objects.filter(is_publish_trendyol=True).count()

    total_cash_list = []
    total_cash = 0

    for o in Order.objects.all():
        total_cash_list.append(o.order_total)

    for o in TrendyolOrders.objects.all():
        total_cash_list.append(o.sales_amount)

    for tc in total_cash_list:
        total_cash += tc

    waiting_order = Order.objects.filter(status="Yeni").count()

    now = datetime.now(timezone.utc)

    new_order = Order.objects.filter(status="Yeni")

    delayed_list = []
    for no in new_order:
        if (now - no.created_at).days > 2:
            delayed_list.append(no)
    delayed_list_count = len(delayed_list)

    last_orders = Order.objects.all()

    if last_orders.count() > 20:
        last_orders = last_orders[:20]

    last_product = ApiProduct.objects.all().order_by("-create_at")[:10]

    extraditionrequest = ExtraditionRequest.objects.all().exclude(extraditionrequestresult__typ="Kabul Edildi").count()

    campaing_product = ApiProduct.objects.filter(is_discountprice=True).count()

    review_rating = ReviewRating.objects.all().count()

    favoruite_product = Favorite.objects.all().count()

    cart_item_product = CartItem.objects.all().count()

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'product_count': product_count,
        'user_count': user_count,
        'order_count': order_count,
        'delivery_product': delivery_product,
        'last_orders': last_orders,
        'last_product': last_product,
        'sold_out_product_count': sold_out_product_count,
        'trendyol_product_count': trendyol_product_count,
        'waiting_order': waiting_order,
        'delayed_list_count': delayed_list_count,
        'extraditionrequest': extraditionrequest,
        'campaing_product': campaing_product,
        'review_rating': review_rating,
        'favoruite_product': favoruite_product,
        'cart_item_product': cart_item_product,
        'total_cash': total_cash,
    })
    return render(request, 'backend/adminpage/pages/mainpage.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def slider(request):
    context = {}

    slider = Slider.objects.all()

    form = SliderForm(data=request.POST or None, files=request.FILES or None)

    if 'addBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Slider eklendi')
            return redirect("admin_slider")

    paginator = Paginator(slider, 25)
    page = request.GET.get('page')

    try:
        sliders = paginator.page(page)
    except PageNotAnInteger:
        sliders = paginator.page(1)
    except EmptyPage:
        sliders = paginator.page(paginator.num_pages)

    context.update({
        'sliders': sliders,
        'form': form
    })

    return render(request, 'backend/adminpage/pages/frontend_sayfalar/slider.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def slider_detail(request, id):
    context = {}

    slider = Slider.objects.get(id=id)

    form = SliderForm(instance=slider, data=request.POST or None, files=request.FILES or None)

    context.update({
        'slider': slider,
        'form': form
    })

    if 'updateBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Slider güncellendi')
            return redirect("admin_slider")

    return render(request, 'backend/adminpage/pages/frontend_sayfalar/slider_update.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def slider_delete(request, id):
    slider = Slider.objects.get(id=id)
    slider.delete()
    messages.success(request, 'Slider silindi')
    return redirect('admin_slider')


@login_required(login_url="/yonetim/giris-yap/")
def slider_delete_all(request, ):
    sliders = Slider.objects.all()
    for s in sliders:
        s.delete()

    messages.success(request, 'Tüm sliderlar silindi')
    return redirect('admin_slider')


@login_required(login_url="/yonetim/giris-yap/")
def slider_select_delete(request):
    slider_id = request.GET.getlist('slider[]')
    Slider.objects.filter(id__in=slider_id).delete()
    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def slider_publish(request, id):
    slider = Slider.objects.get(id=id)
    slider.is_publish = True
    slider.save()
    messages.success(request, f'{slider.title} yayına alındı')
    return redirect('admin_slider')


@login_required(login_url="/yonetim/giris-yap/")
def slider_not_publish(request, id):
    slider = Slider.objects.get(id=id)
    slider.is_publish = False
    slider.save()
    messages.success(request, f'{slider.title} yayından kaldırıldı')
    return redirect('admin_slider')


@login_required(login_url="/yonetim/giris-yap/")
def notification(request):
    context = {}
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    notify = Notification.objects.all()

    p = Paginator(notify, 20)
    page = request.GET.get('page')
    notifies = p.get_page(page)

    context.update({
        'notify': notify,
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'notifies': notifies,
    })
    return render(request, 'backend/adminpage/pages/bildirimler.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kullanicilar(request):
    context = {}
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    user = User.objects.all()

    p = Paginator(user, 50)
    page = request.GET.get('page')
    users = p.get_page(page)

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'users': users,
    })
    return render(request, 'backend/adminpage/pages/kullanici_yonetimi/kullanicilar.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kullanici_goruntule(request, id):
    context = {}
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()
    address = None
    coupons = None
    user = User.objects.get(id=id)

    if user.is_staff or user.is_customer:
        address = CustomerAddress.objects.filter(user=user)
        coupons = Coupon.objects.filter(user=user)

    context.update({
        'user': user,
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'address': address,
        'coupons': coupons
    })
    return render(request, 'backend/adminpage/pages/kullanici_yonetimi/kullanici_goruntule.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kullanici_sil(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, 'Kullanıcı silindi.')
    return redirect('kullanicilar')


@login_required(login_url="/yonetim/giris-yap/")
def kullanici_ekle(request):
    context = {}

    filter_full_name = request.GET.get('filter_full_name')
    filter_email = request.GET.get('filter_email')
    filter_mobile = request.GET.get('filter_mobile')
    filter_user_type = request.GET.get('filter_user_type')
    filter_activated = request.GET.get('filter_activated')

    query = f"?ad_soyad={filter_full_name}&email={filter_email}&telefon={filter_mobile}&uyelik_tipi={filter_user_type}&aktif={filter_activated}"

    kullanicilar = User.objects.all()

    if filter_full_name:
        kullanicilar = User.objects.filter(Q(first_name__icontains=filter_full_name))
    if filter_email:
        kullanicilar = User.objects.filter(Q(email__icontains=filter_email))
    if filter_mobile:
        kullanicilar = User.objects.filter(Q(mobile__icontains=filter_mobile))
    if filter_user_type:
        if filter_user_type == "Yönetici":
            kullanicilar = User.objects.filter(is_superuser=True)
        if filter_user_type == "Personel":
            kullanicilar = User.objects.filter(is_superuser=False, is_staff=True)
        if filter_user_type == "Müşteri":
            kullanicilar = User.objects.filter(is_superuser=False, is_staff=False, is_customer=True)
    if filter_activated:
        kullanicilar = User.objects.filter(is_activated=filter_activated)

    p = Paginator(kullanicilar, 20)
    page = request.GET.get('page')
    kullanici = p.get_page(page)

    if 'create_user' in request.POST:
        user_type = request.POST.get('user_type')
        ad = request.POST.get('first_name')
        soyad = request.POST.get('last_name')
        email = request.POST.get('email')
        telefon = request.POST.get('mobile')
        sifre = request.POST.get('password')

        if user_type == "Yönetici":
            User.objects.create(first_name=ad, last_name=soyad, email=email, mobile=telefon, password=sifre,
                                is_customer=False, is_superuser=True, is_staff=True, is_activated=True, is_active=True)

        if user_type == "Personel":
            User.objects.create(first_name=ad, last_name=soyad, email=email, mobile=telefon, password=sifre,
                                is_customer=False, is_superuser=False, is_staff=True, is_activated=True, is_active=True)

        if user_type == "Müşteri":
            User.objects.create(first_name=ad, last_name=soyad, email=email, mobile=telefon, password=sifre,
                                is_customer=True, is_superuser=False, is_staff=False, is_activated=True, is_active=True)

        messages.success(request, 'Kullanıcı başarıyla oluşturuldu.')
        return redirect('kullanici_ekle')

    context.update({
        'users': kullanici,
        'query': query,
    })

    return render(request, 'backend/adminpage/pages/kullanici_yonetimi/kullanici_ekle.html', context)


@login_required(login_url="/giris-yap")
def kullanici_izinleri(request, id):
    context = {}

    user = get_object_or_404(User, id=id)

    izin = izinSor(user_id=id)

    context.update({
        'user': user,
        'izin': izin,
    })

    if izin is None:
        form = IzinForm(data=request.POST or None, files=request.FILES or None)
        context.update({'form': form})
        if 'submit_btn' in request.POST:
            if form.is_valid():
                data = form.save(commit=False)
                data.user = user
                data.save()
                messages.success(request, 'İlgili kullanıcının yetkileri başarıyla yapıldı.')
                return redirect('kullanici_izinleri', id)
    else:
        form = IzinForm(instance=izin, data=request.POST or None, files=request.FILES or None)
        context.update({'form': form})
        if 'submit_btn' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, 'İlgili kullanıcının yetkileri güncellendi.')
                return redirect('kullanici_izinleri', id)

    return render(request, 'backend/adminpage/pages/kullanici_yonetimi/kullanici_izinleri.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def read_notification(request, id):
    context = {}
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    notify = Notification.objects.get(id=id)
    notify.is_read = True
    notify.save()

    context.update({
        'notify': notify,
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
    })
    return render(request, 'backend/adminpage/pages/bildirimler_oku.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def sil_notification(request, id):
    Notification.objects.filter(id=id).delete()
    return redirect('notification')


@login_required(login_url="/yonetim/giris-yap/")
def secili_sil_notification(request):
    select_id = request.GET.getlist('select-notify[]')

    Notification.objects.filter(id__in=select_id).delete()
    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def admin_aboutus(request):
    context = {}
    form = AboutUsForm(data=request.POST or None, files=request.FILES or None)
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()
    context.update({
        'form': form,
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count
    })

    aboutus = Hakkimizda.objects.all()
    if aboutus.count() > 0:
        form = AboutUsForm(instance=aboutus.last(), data=request.POST or None, files=request.FILES or None)
        context.update({'form': form})

    categories_count = MainCategory.objects.all().count()
    product_count = ApiProduct.objects.all().count()

    if 'addBtn' in request.POST:
        if form.is_valid():
            data = form.save(commit=False)
            data.category_count = categories_count
            data.product_count = product_count
            data.save()
            messages.success(request, 'Hakkımızda sayfası bilgiler eklendi.')
            return redirect("admin_aboutus")

    return render(request, 'backend/adminpage/pages/frontend_sayfalar/aboutus.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def page_mainpage(request):
    context = {}

    banner_one = BannerOne.objects.filter().last()
    banner_two = BannerTwo.objects.filter().last()

    if banner_one:
        banner_one_form = BannerOneForm(instance=banner_one, data=request.POST or None, files=request.FILES or None)
    else:
        banner_one_form = BannerOneForm(data=request.POST or None, files=request.FILES or None)

    if banner_two:
        banner_two_form = BannerTwoForm(instance=banner_two, data=request.POST or None, files=request.FILES or None)
    else:
        banner_two_form = BannerTwoForm(data=request.POST or None, files=request.FILES or None)

    context.update({
        'banner_one': banner_one,
        'banner_two': banner_two,
        'banner_one_form': banner_one_form,
        'banner_two_form': banner_two_form
    })

    if 'firstBannerBtn' in request.POST:
        if banner_one_form.is_valid():
            banner_one_form.save()
            messages.success(request, '1. Banner düzenlendi.')
            return redirect('page_mainpage')

    if 'secondBannerBtn' in request.POST:
        if banner_two_form.is_valid():
            banner_two_form.save()
            messages.success(request, '2. Banner düzenlendi.')
            return redirect('page_mainpage')

    return render(request, 'backend/adminpage/pages/frontend_sayfalar/page_mainpage.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye1(request):
    context = {}
    category = MainCategory.objects.all()
    subcategory = SubCategory.objects.all()
    form = MainCategoryForm(data=request.POST or None, files=request.FILES or None)
    context.update({
        'category': category,
        'form': form,
        'subcategory': subcategory
    })

    if 'addBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori eklendi.')
            return redirect("kategoriler_seviye1")

    return render(request, 'backend/adminpage/pages/kategori_yonetimi/kategoriler_seviye1.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye1_guncelle(request, id):
    context = {}
    category = MainCategory.objects.get(id=id)
    form = MainCategoryForm(instance=category, data=request.POST or None, files=request.FILES or None)
    context.update({
        'category': category,
        'form': form,
    })

    if 'updateBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori güncellendi.')
            return redirect("kategoriler_seviye1_guncelle", id)

    return render(request, 'backend/adminpage/pages/kategori_yonetimi/kategoriler_seviye1_guncelle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye1_sil(request, id):
    context = {}
    category = MainCategory.objects.get(id=id)
    category_title = category.title
    category.delete()
    messages.success(request, f'{category_title} ve ona bağlı alt kategorilerde silindi.')
    return redirect("kategoriler_seviye1")


def kategoriler_seviye1_export_excel(request):
    columns = ['ID', 'Başlık', 'Sırası',
               'Kategori Numarası', 'Oluşturulma Tarihi']

    rows = MainCategory.objects.all().values_list('id', 'title', 'order', 'category_no', 'created_at')
    return exportExcel('Kategoriler', 'Kategoriler', columns=columns, rows=rows)


def kategoriler_seviye1_export_pdf(request):
    columns = ["ID", "Başlık", "Kategori Sırası", "Kategori Numarası", "Oluşturulma Tarihi"]
    rows = []
    row = MainCategory.objects.all().values_list('id', 'title', 'order', 'category_no', 'created_at')
    for r in row:
        rows.append(r)

    dict = {
        'columns': columns,
        'rows': rows
    }

    pdf = exportPdf(f"{str(settings.BASE_DIR)}" + "/templates/backend/adminpage/partials/table_pdf.html", dict)
    response = HttpResponse(pdf, content_type='application/pdf')
    content = f'attachment; filename=Kategoriler' + '.pdf'
    response['Content-Disposition'] = content

    return response


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye1_hepsini_sil(request):
    context = {}
    category = MainCategory.objects.all().delete()
    messages.success(request, 'Tüm ana kategoriler ve bağlı olan alt kategorilerde silindi.')
    return redirect("kategoriler_seviye1")


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_secilileri_sil(request):
    categoy1_id = request.GET.getlist('seviye1-category[]')

    MainCategory.objects.filter(id__in=categoy1_id).delete()
    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye2(request, slug):
    context = {}
    maincategory = MainCategory.objects.get(slug=slug)
    subcategory = SubCategory.objects.filter(maincategory__slug=slug)
    subbottomcategory = SubBottomCategory.objects.all()
    form = SubCategoryForm(data=request.POST or None, files=request.FILES or None)
    context.update({
        'maincategory': maincategory,
        'subcategory': subcategory,
        'form': form,
        'subbottomcategory': subbottomcategory
    })

    if 'addBtn' in request.POST:
        if form.is_valid():
            data = form.save(commit=False)
            data.maincategory = maincategory
            data.save()
            messages.success(request, 'Kategori başarıyla eklendi.')
            return redirect("kategoriler_seviye2")

    return render(request, 'backend/adminpage/pages/kategori_yonetimi/kategoriler_seviye2.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye2_guncelle(request, id):
    context = {}
    category = SubCategory.objects.get(id=id)
    form = SubCategoryForm(instance=category, data=request.POST or None, files=request.FILES or None)
    context.update({
        'category': category,
        'form': form,
    })

    if 'updateBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori güncellendi.')
            return redirect("kategoriler_seviye2_guncelle", id)

    return render(request, 'backend/adminpage/pages/kategori_yonetimi/kategoriler_seviye2_guncelle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye2_sil(request, id):
    context = {}
    category = SubCategory.objects.get(id=id)
    category_title = category.title
    category.delete()
    messages.success(request, f'{category_title} ve ona bağlı alt kategorilerde silindi.')
    return redirect("kategoriler_seviye2")


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye2_hepsini_sil(request, slug):
    context = {}
    category = SubCategory.objects.filter(maincategory__slug=slug).delete()
    messages.success(request, 'Tüm ana kategoriler ve bağlı olan alt kategorilerde silindi.')
    return redirect("kategoriler_seviye2")


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye2_tum_sil(request):
    context = {}
    category = SubCategory.objects.all().delete()
    messages.success(request, 'Tüm alt kategoriler silindi.')
    return redirect("kategoriler_seviye2")


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler2_secilileri_sil(request):
    categoy_id = request.GET.getlist('seviye2-category[]')
    SubCategory.objects.filter(id__in=categoy_id).delete()
    data = 'success'
    return JsonResponse(data=data, safe=False)


def kategoriler_seviye2_export_excel(request, slug):
    columns = ['ID', 'Üst Kategorisi', 'Başlık',
               'Kategori Numarası', 'Oluşturulma Tarihi']

    seviye1_category = MainCategory.objects.get(slug=slug)
    rows = SubCategory.objects.filter(maincategory=seviye1_category).values_list('id', 'maincategory__title', 'title',
                                                                                 'category_no', 'created_at')
    return exportExcel(f'{slug}-alt-kategorileri', 'Kategoriler', columns=columns, rows=rows)


def kategoriler_seviye2_hepsi_export_excel(request):
    columns = ['ID', 'Üst Kategorisi', 'Başlık',
               'Kategori Numarası', 'Oluşturulma Tarihi']

    rows = SubCategory.objects.all().values_list('id', 'maincategory__title', 'title', 'category_no', 'created_at')
    return exportExcel('tüm-alt-kategorileri', 'Kategoriler', columns=columns, rows=rows)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye3(request, main_slug, sub_slug):
    context = {}
    maincategory = MainCategory.objects.get(slug=main_slug)
    subcategory = SubCategory.objects.get(slug=sub_slug)
    subbottomcategory = SubBottomCategory.objects.filter(subcategory__slug=sub_slug)
    form = SubBottomCategoryForm(data=request.POST or None, files=request.FILES or None)
    context.update({
        'maincategory': maincategory,
        'subcategory': subcategory,
        'form': form,
        'subbottomcategory': subbottomcategory
    })

    if 'addBtn' in request.POST:
        if form.is_valid():
            data = form.save(commit=False)
            data.maincategory = maincategory
            data.subcategory = subcategory
            data.save()
            messages.success(request, 'Kategori başarıyla eklendi.')
            return redirect("kategoriler_seviye3", main_slug, sub_slug)

    return render(request, 'backend/adminpage/pages/kategori_yonetimi/kategoriler_seviye3.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye3_guncelle(request, main_slug, sub_slug, id):
    context = {}
    category = SubCategory.objects.get(id=id)
    form = SubBottomCategoryForm(instance=category, data=request.POST or None, files=request.FILES or None)
    context.update({
        'category': category,
        'form': form,
    })

    if 'updateBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori güncellendi.')
            return redirect("kategoriler_seviye3_guncelle", main_slug, sub_slug, id)

    return render(request, 'backend/adminpage/pages/kategori_yonetimi/kategoriler_seviye3_guncelle.html', context)


def kategoriler_seviye3_export_excel(request, slug):
    columns = ['ID', 'En Üst Kategorisi', 'Üst Kategorisi', 'Başlık', 'Oluşturulma Tarihi']

    seviye2_category = SubCategory.objects.get(slug=slug)
    rows = SubBottomCategory.objects.filter(subcategory=seviye2_category).values_list('id', 'maincategory__title',
                                                                                      'subcategory__title', 'title',
                                                                                      'created_at')
    return exportExcel(f'{slug}-alt-kategorileri', 'Kategoriler', columns=columns, rows=rows)


def kategoriler_seviye3_hepsi_export_excel(request):
    columns = ['ID', 'En Üst Kategorisi', 'Üst Kategorisi', 'Başlık', 'Oluşturulma Tarihi']

    rows = SubBottomCategory.objects.all().values_list('id', 'maincategory__title', 'subcategory__title', 'title',
                                                       'created_at')
    return exportExcel('tüm-alt-kategorileri', 'Kategoriler', columns=columns, rows=rows)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye3_sil(request, main_slug, sub_slug, id):
    context = {}
    category = SubBottomCategory.objects.get(id=id)
    category.delete()
    messages.success(request, 'Kategori silindi.')
    return redirect("kategoriler_seviye3", main_slug, sub_slug)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye3_hepsini_sil(request, main_slug, sub_slug):
    context = {}
    category = SubBottomCategory.objects.filter(subcategory__slug=sub_slug).delete()
    messages.success(request, 'Kategori silindi.')
    return redirect("kategoriler_seviye3", main_slug, sub_slug)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye3_tum_sil(request, main_slug, sub_slug):
    context = {}
    category = SubBottomCategory.objects.all().delete()
    messages.success(request, 'Tüm alt kategoriler silindi.')
    return redirect("kategoriler_seviye3", main_slug, sub_slug)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler3_secilileri_sil(request):
    categoy_id = request.GET.getlist('seviye3-category[]')
    SubBottomCategory.objects.filter(id__in=categoy_id).delete()
    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def products(request):
    context = {}

    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    baslik = request.GET.get("baslik", '')
    barkod = request.GET.get("barkod", '')
    modelKodu = request.GET.get("modelKodu", '')
    stokKodu = request.GET.get("stokKodu", '')
    kategori = request.GET.get("kategori", '')
    dropshipping = request.GET.get("dropshipping", '')
    publish = request.GET.get("publish", True)
    stock = request.GET.get("stock", '')
    desc = request.GET.get('desc', '?')

    query = f"?baslik={baslik}&barkod={barkod}&modelKodu={modelKodu}&stokKodu={stokKodu}&kategori={kategori}&dropshipping={dropshipping}&publish={publish}&stock={stock}&desc={desc}"

    product = ApiProduct.objects.all()

    if desc:
        product = product.order_by(desc)

    if baslik:
        product = ApiProduct.objects.filter(Q(title__icontains=baslik))

    if barkod:
        product = ApiProduct.objects.filter(Q(barcode__icontains=barkod))

    if modelKodu:
        product = ApiProduct.objects.filter(Q(model_code__icontains=modelKodu))

    if stokKodu:
        product = ApiProduct.objects.filter(Q(stock_code__icontains=stokKodu))

    if kategori:

        if kategori == "None":
            product = ApiProduct.objects.filter(subbottomcategory__isnull=True)
        else:
            product = ApiProduct.objects.filter(subbottomcategory_id=kategori)

    if dropshipping:
        product = ApiProduct.objects.filter(Q(dropshipping__icontains=dropshipping))

    if publish:
        product = ApiProduct.objects.filter(is_publish=publish)

    if stock:
        if stock == "True":
            product = ApiProduct.objects.filter(quantity__gte=1)
        else:
            product = ApiProduct.objects.filter(quantity=0)

    if kategori and publish:
        if kategori == "None":
            product = ApiProduct.objects.filter(subbottomcategory__isnull=True, is_publish=publish)
        else:
            product = ApiProduct.objects.filter(subbottomcategory_id=kategori, is_publish=publish)

    paginator = Paginator(product, 50)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    categories = SubBottomCategory.objects.all()

    product_count = product.count()
    modaymis_product_count = product.filter(dropshipping="Modaymış").count()
    tahtakale_product_count = product.filter(dropshipping="Tahtakale").count()
    upload_trendyol_count = product.filter(is_publish_trendyol=True).count()
    active_product_count = ApiProduct.objects.filter(is_publish=True).count()
    not_active_product_count = ApiProduct.objects.filter(is_publish=False).count()
    insufficient_count = product.filter(quantity=0).count()

    context.update({
        'products': products,
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'product_count': product_count,
        'modaymis_product_count': modaymis_product_count,
        'tahtakale_product_count': tahtakale_product_count,
        'upload_trendyol_count': upload_trendyol_count,
        'active_product_count': active_product_count,
        'insufficient_count': insufficient_count,
        'categories': categories,
        'query': query,
        'not_active_product_count': not_active_product_count,
        'baslik': baslik,
        'barkod': barkod,
        'modelKodu': modelKodu,
        'stokKodu': stokKodu,
        'kategori': kategori,
        'dropshipping': dropshipping,
        'publish': publish,
        'stock': stock,
        'desc': desc,
    })

    return render(request, 'backend/adminpage/pages/urun_yonetimi/products.html', context)


def clean_filters(filters):
    filters = {k: v for k, v in filters.items() if v}
    return filters


@login_required(login_url="/yonetim/giris-yap/")
def product_detail(request, id):
    context = {}

    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    product = ApiProduct.objects.get(id=id)

    try:
        form = ProductForm(instance=product, data=request.POST or None, files=request.FILES or None)
    except:
        form = ErrorProductForm(instance=product, data=request.POST or None, files=request.FILES or None)
    variants = ApiProduct.objects.filter(model_code=product.model_code).exclude(id=product.id)

    context.update({
        'product': product,
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'form': form,
        'variants': variants,
    })

    if 'updateBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Ürün güncellendi.')
            return redirect('product_detail', id)
    if 'updateAndCloseBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Ürün güncellendi.')
            return redirect('admin_product')

    if 'variantUpdateBtn' in request.POST:
        kapak = request.FILES['kapak']
        image1 = request.POST.get('fabrictype')
        image2 = request.POST.get('fabrictype')
        image3 = request.POST.get('fabrictype')
        image4 = request.POST.get('fabrictype')
        image5 = request.POST.get('fabrictype')
        image6 = request.POST.get('fabrictype')
        image7 = request.POST.get('fabrictype')
        image8 = request.POST.get('fabrictype')
        fabrictype = request.POST.get('fabrictype')
        height = request.POST.get('height')
        waist = request.POST.get('waist')
        pattern = request.POST.get('pattern')
        armtype = request.POST.get('armtype')
        collartype = request.POST.get('collartype')
        weavingtype = request.POST.get('weavingtype')
        material = request.POST.get('material')
        age_group = request.POST.get('age_group')
        sex = request.POST.get('sex')
        detail = request.POST.get('detail')
        description = request.POST.get('description')
        heeltype = request.POST.get('heeltype')
        heelsize = request.POST.get('heelsize')
        environment = request.POST.get('environment')
        legtype = request.POST.get('legtype')
        pocket = request.POST.get('pocket')

        for v in variants:
            if fabrictype:
                fabric_type = FabricType.objects.get(id=fabrictype)
                v.fabrictype = fabric_type
            if height:
                heights = Height.objects.get(id=height)
                v.height = heights
            if waist:
                waist_type = Waist.objects.get(id=waist)
                v.waist = waist_type
            if pattern:
                patterns = Pattern.objects.get(id=pattern)
                v.pattern = patterns
            if armtype:
                arm_type = ArmType.objects.get(id=armtype)
                v.armtype = arm_type
            if collartype:
                collar_type = CollerType.objects.get(id=collartype)
                v.collartype = collar_type
            if weavingtype:
                weaving_type = WeavingType.objects.get(id=weavingtype)
                v.weavingtype = weaving_type
            if material:
                material_type = MaterialType.objects.get(id=material)
                v.material = material_type
            if heeltype:
                heel_type = HeelType.objects.get(id=heeltype)
                v.heeltype = heel_type
            if heeltype:
                heel_size = HeelSize.objects.get(id=heelsize)
                v.heelsize = heel_size
            if environment:
                environment_type = EnvironmentType.objects.get(id=environment)
                v.environment = environment_type
            if legtype:
                leg_type = LegType.objects.get(id=legtype)
                v.legtype = leg_type
            if pocket:
                pocket_type = Pocket.objects.get(id=pocket)
                v.pocket = pocket_type
            if age_group:
                v.age_group = age_group
            if sex:
                sex = Sex.objects.get(id=sex)
                v.sex = sex
            if detail:
                v.detail = detail
            if description:
                v.description = description
            if kapak:
                v.kapak = kapak
            if image1:
                v.image_url1 = image1
            if image2:
                v.image_url2 = image2
            if image3:
                v.image_url3 = image3
            if image4:
                v.image_url4 = image4
            if image5:
                v.image_url5 = image5
            if image6:
                v.image_url6 = image6
            if image7:
                v.image_url7 = image7
            if image8:
                v.image_url8 = image8
            v.save()
        messages.success(request, 'Tüm variantlar güncellendi.')
        return redirect('product_detail', id)
    return render(request, 'backend/adminpage/pages/urun_yonetimi/product_detay.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kampanyali_urunler(request):
    context = {}
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    products = ApiProduct.objects.filter(is_discountprice=True)

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'products': products,
    })
    return render(request, 'backend/adminpage/pages/urun_yonetimi/kampanyali_urunler.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def urun_ozellik_guncelleme(request):
    context = {}

    if 'kalip_guncelle' in request.POST:
        kalip()
        messages.success(request, 'Kalıp güncellendi.')
        return redirect('urun_ozellik_guncelleme')
    if 'kumas_guncelle' in request.POST:
        kumas()
        messages.success(request, 'Kumaş güncellendi.')
        return redirect('urun_ozellik_guncelleme')
    if 'ortam_guncelle' in request.POST:
        ortam()
        messages.success(request, 'Ortam güncellendi.')
        return redirect('urun_ozellik_guncelleme')
    if 'yaka_guncelle' in request.POST:
        yaka()
        messages.success(request, 'Yaka tipi güncellendi.')
        return redirect('urun_ozellik_guncelleme')
    if 'cinsiyet_guncelle' in request.POST:
        cinsiyet()
        messages.success(request, 'Cinsiyet güncellendi.')
        return redirect('urun_ozellik_guncelleme')
    if 'bel_guncelle' in request.POST:
        bel()
        messages.success(request, 'Bel güncellendi.')
        return redirect('urun_ozellik_guncelleme')
    if 'boy_guncelle' in request.POST:
        boy()
        messages.success(request, 'Boy güncellendi.')
        return redirect('urun_ozellik_guncelleme')
    if 'paca_guncelle' in request.POST:
        paca()
        messages.success(request, 'Paça Tipi güncellendi.')
        return redirect('urun_ozellik_guncelleme')
    if 'kategori_guncelle' in request.POST:
        kategori()
        messages.success(request, 'Kategori bilgisi güncellendi.')
        return redirect('urun_ozellik_guncelleme')
    return render(request, 'backend/adminpage/pages/urun_yonetimi/urun_ozellik_guncelleme.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def beden_tablosu(request):
    context = {}

    kadin_ust_beden_tablosu = KadinUstBedenTablosu.objects.all()
    kadin_ust_buyuk_beden_tablosu = KadinUstBuyukBedenTablosu.objects.all()
    kadin_alt_beden_tablosu = KadinAltBedenTablosu.objects.all()
    kadin_alt_buyuk_beden_tablosu = KadinAltBuyukBedenTablosu.objects.all()
    kadin_jean_beden_tablosu = KadinJeanBedenTablosu.objects.all()

    context.update({
        'kadin_ust_beden_tablosu': kadin_ust_beden_tablosu,
        'kadin_ust_buyuk_beden_tablosu': kadin_ust_buyuk_beden_tablosu,
        'kadin_alt_beden_tablosu': kadin_alt_beden_tablosu,
        'kadin_alt_buyuk_beden_tablosu': kadin_alt_buyuk_beden_tablosu,
        'kadin_jean_beden_tablosu': kadin_jean_beden_tablosu,
    })

    if 'add_kadin_ust_beden' in request.POST:
        kadin_ust_beden_adi = request.POST.get('kadin_ust_beden_adi')
        kadin_ust_eu_tr = request.POST.get('kadin_ust_eu_tr')
        kadin_ust_boyun = request.POST.get('kadin_ust_boyun', None)
        kadin_ust_gogus = request.POST.get('kadin_ust_gogus', None)
        kadin_ust_bel = request.POST.get('kadin_ust_bel', None)

        KadinUstBedenTablosu.objects.create(beden_adi=kadin_ust_beden_adi, eu_tr=kadin_ust_eu_tr, boyun=kadin_ust_boyun,
                                            bel=kadin_ust_bel, gogus=kadin_ust_gogus)
        messages.success(request, 'Kadın üst beden başarıyla eklendi')
        return redirect('beden_tablosu')

    if 'add_kadin_ust_buyuk_beden' in request.POST:
        kadin_ust_beden_adi = request.POST.get('kadin_ust_buyuk_beden_adi')
        kadin_ust_eu_tr = request.POST.get('kadin_ust_buyuk_eu_tr')
        kadin_ust_boyun = request.POST.get('kadin_ust_buyuk_boyun', None)
        kadin_ust_gogus = request.POST.get('kadin_ust_buyuk_gogus', None)
        kadin_ust_bel = request.POST.get('kadin_ust_buyuk_bel', None)

        KadinUstBuyukBedenTablosu.objects.create(beden_adi=kadin_ust_beden_adi, eu_tr=kadin_ust_eu_tr,
                                                 boyun=kadin_ust_boyun, bel=kadin_ust_bel, gogus=kadin_ust_gogus)
        messages.success(request, 'Kadın üst büyük beden başarıyla eklendi')
        return redirect('beden_tablosu')

    if 'add_kadin_alt_beden' in request.POST:
        kadin_alt_beden_adi = request.POST.get('kadin_alt_beden_adi')
        kadin_alt_eu_tr = request.POST.get('kadin_alt_eu_tr')
        kadin_alt_bel = request.POST.get('kadin_alt_bel', None)
        kadin_alt_basen = request.POST.get('kadin_alt_basen', None)

        KadinAltBedenTablosu.objects.create(beden_adi=kadin_alt_beden_adi, eu_tr=kadin_alt_eu_tr, bel=kadin_alt_bel,
                                            basen=kadin_alt_basen)
        messages.success(request, 'Kadın alt beden başarıyla eklendi')
        return redirect('beden_tablosu')

    if 'add_kadin_alt_buyuk_beden' in request.POST:
        kadin_alt_buyuk_beden_adi = request.POST.get('kadin_alt_buyuk_beden_adi')
        kadin_alt_buyuk_eu_tr = request.POST.get('kadin_alt_buyuk_eu_tr')
        kadin_alt_buyuk_bel = request.POST.get('kadin_alt_buyuk_bel', None)
        kadin_alt_buyuk_basen = request.POST.get('kadin_alt_buyuk_basen', None)

        KadinAltBuyukBedenTablosu.objects.create(beden_adi=kadin_alt_buyuk_beden_adi, eu_tr=kadin_alt_buyuk_eu_tr,
                                                 bel=kadin_alt_buyuk_bel,
                                                 basen=kadin_alt_buyuk_basen)
        messages.success(request, 'Kadın alt büyük beden başarıyla eklendi')
        return redirect('beden_tablosu')

    if 'add_kadin_jean_beden' in request.POST:
        kadin_jean_beden_adi = request.POST.get('kadin_jean_beden_adi')
        kadin_jean_eu_tr = request.POST.get('kadin_jean_eu_tr')
        kadin_jean_bel = request.POST.get('kadin_jean_bel', None)
        kadin_jean_basen = request.POST.get('kadin_jean_basen', None)

        KadinJeanBedenTablosu.objects.create(beden_adi=kadin_jean_beden_adi, eu_tr=kadin_jean_eu_tr, bel=kadin_jean_bel,
                                             basen=kadin_jean_basen)
        messages.success(request, 'Kadın jean beden başarıyla eklendi')
        return redirect('beden_tablosu')

    return render(request, 'backend/adminpage/pages/urun_yonetimi/beden_tablosu.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kadin_ust_beden_sil(request, id):
    kadin_ust_beden = get_object_or_404(KadinUstBedenTablosu, id=id)
    kadin_ust_beden.delete()
    messages.success(request, 'Kadın üst beden başarıyla silindi.')
    return redirect('beden_tablosu')


@login_required(login_url="/yonetim/giris-yap/")
def kadin_ust_buyuk_beden_sil(request, id):
    kadin_ust_beden = get_object_or_404(KadinUstBuyukBedenTablosu, id=id)
    kadin_ust_beden.delete()
    messages.success(request, 'Kadın üst büyük beden başarıyla silindi.')
    return redirect('beden_tablosu')


@login_required(login_url="/yonetim/giris-yap/")
def kadin_alt_beden_sil(request, id):
    kadin_alt_beden = get_object_or_404(KadinAltBedenTablosu, id=id)
    kadin_alt_beden.delete()
    messages.success(request, 'Kadın alt beden başarıyla silindi.')
    return redirect('beden_tablosu')


@login_required(login_url="/yonetim/giris-yap/")
def kadin_alt_buyuk_beden_sil(request, id):
    kadin_alt_beden = get_object_or_404(KadinAltBuyukBedenTablosu, id=id)
    kadin_alt_beden.delete()
    messages.success(request, 'Kadın alt büyük beden başarıyla silindi.')
    return redirect('beden_tablosu')


@login_required(login_url="/yonetim/giris-yap/")
def kadin_jean_beden_sil(request, id):
    kadin_jean_beden = get_object_or_404(KadinJeanBedenTablosu, id=id)
    kadin_jean_beden.delete()
    messages.success(request, 'Kadın jean beden başarıyla silindi.')
    return redirect('beden_tablosu')


@login_required(login_url="/yonetim/giris-yap/")
def all_delete_product(request):
    products = ApiProduct.objects.all().delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/yonetim/giris-yap/")
def ajax_select_delete_product(request):
    product_id = request.GET.getlist('product[]')

    ApiProduct.objects.filter(id__in=product_id).delete()

    data = 'success'
    return JsonResponse(data=data, safe=False)


def product_export_excel(request):
    deneme_product = ApiProduct.objects.filter(is_publish_trendyol=True, is_publish=False)
    trendyol_list = []

    columns = ['Başlık', 'Barkod']

    rows = ApiProduct.objects.filter(is_publish_trendyol=True).values_list('title', 'barcode')

    return exportExcel('products', 'Ürünler', columns=columns, rows=rows)


@login_required(login_url="/yonetim/giris-yap/")
def orders(request):
    context = {}
    order = Order.objects.all()
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    p = Paginator(order, 20)
    page = request.GET.get('page')
    orders = p.get_page(page)

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'orders': orders,
    })

    return render(request, 'backend/adminpage/pages/siparis_yonetimi/orders.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_add_order(request):
    context = {}
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    form = TrendyolOrderForm(data=request.POST or None,
                             files=request.FILES or None)

    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Trendyol sipariş eklendi.')
            return redirect('trendyol_add_order')

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'form': form
    })

    return render(request, 'backend/adminpage/pages/trendyol/add_orders.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_orders(request):
    context = {}
    order = TrendyolOrders.objects.all().order_by("-id")
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    p = Paginator(order, 50)
    page = request.GET.get('page')
    orders = p.get_page(page)

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'orders': orders,
    })

    return render(request, 'backend/adminpage/pages/trendyol/orders.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def get_trendyol_orders(request):
    context = {}
    trendyol = Trendyol.objects.all().last()
    trendyol_orders = TrendyolOrders.objects.all()
    filter_params = None
    color = '-'
    komisyon_tutari = 0

    api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                            supplier_id=trendyol.saticiid)
    service = OrderIntegrationService(api)
    response = service.get_shipment_packages(filter_params=filter_params)
    status = None
    for r in response['content']:
        customerName = r['customerFirstName'] + ' ' + r['customerLastName']
        orderNumber = r['orderNumber']
        packetNumber = r['id']
        orderDate = r['orderDate']
        datetime_obj_with_tz = datetime.utcfromtimestamp(orderDate / 1000)

        if TrendyolOrders.objects.filter(packet_number__contains=str(packetNumber)).count() > 0:
            order = TrendyolOrders.objects.get(packet_number=str(packetNumber))
            if len(r['lines']) == 1:
                order.shippment_city = r['shipmentAddress']['city']
                for l in r['lines']:
                    orderStatus = l['orderLineItemStatusName']
                    if orderStatus == 'UnDeliveredAndReturned':
                        status = "İade Edildi"
                    elif orderStatus == 'Picking':
                        status = "Hazırlanıyor"
                    elif orderStatus == "Deliverd":
                        status = "Tamamlandı"
                    elif orderStatus == "Cancelled":
                        status = "İptal Edildi"
                        order.commission_price = 0.0
                        order.delivery_price = 0.0
                        order.service_price = 3.59
                    elif orderStatus == "Created" or orderStatus == "ReadyToShip":
                        status = "Yeni"
                    elif orderStatus == "Shipped":
                        status = "Kargolandı"
                    else:
                        status = "Kargolandı"

                order.status = status
                order.save()
            elif len(r['lines']) > 1:
                order.shippment_city = r['shipmentAddress']['city']
                for l in r['lines']:
                    for product in TrendyolMoreProductOrder.objects.filter(order_number=orderNumber,
                                                                           packet_number=packetNumber):
                        orderStatus = l['orderLineItemStatusName']
                        if orderStatus == 'UnDeliveredAndReturned':
                            status = "İade Edildi"
                        elif orderStatus == 'Picking':
                            status = "Hazırlanıyor"
                        elif orderStatus == "Deliverd":
                            status = "Tamamlandı"
                        elif orderStatus == "Cancelled":
                            status = "İptal Edildi"
                            order.commission_price = 0.0
                            order.delivery_price = 0.0
                            order.service_price = 3.59
                        elif orderStatus == "Created" or orderStatus == "ReadyToShip":
                            status = "Yeni"
                        elif orderStatus == "Shipped":
                            status = "Kargolandı"
                        else:
                            status = "Kargolandı"
                        product.status = status
                        product.save()
                order.save()
        else:
            if len(r['lines']) == 1:
                for l in r['lines']:
                    quantity = l['quantity']
                    size = l['productSize']
                    sku = l['merchantSku']
                    title = l['productName']
                    barcode = l['barcode']
                    try:
                        seller_product = get_object_or_404(ApiProduct, barcode=str(l['barcode']))
                        if seller_product.subcategory == "Üst Giyim":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Üst Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.subcategory == "Alt Giyim":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Alt Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.subcategory == "Dış Giyim":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Dış Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.subcategory == "İç Giyim":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="İç Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.subcategory == "Ayakkabı":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Ayakkabı").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.subcategory == "Aksesuar":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Çanta").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        else:
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Alt Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                    except:
                        komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Alt Giyim").komisyon_tutari
                        komisyon_tutari = l['amount'] * komisyon_orani / 100

                    orderStatus = l['orderLineItemStatusName']
                    if orderStatus == 'UnDeliveredAndReturned':
                        status = "İade Edildi"
                    elif orderStatus == 'Picking':
                        status = "Hazırlanıyor"
                    elif orderStatus == "Deliverd":
                        status = "Tamamlandı"
                    elif orderStatus == "Cancelled":
                        status = "İptal Edildi"
                    elif orderStatus == "Created" or orderStatus == "ReadyToShip":
                        status = "Yeni"
                    elif orderStatus == "Shipped":
                        status = "Kargolandı"
                    else:
                        status = "Kargolandı"
                    discount = l['discount']
                    unitPrice = l['amount']
                    salesAmount = l['price']
                    data = TrendyolOrders.objects.create(order_number=orderNumber, packet_number=packetNumber,
                                                  buyer=customerName, quantity=quantity, title=title,
                                                  barcode=barcode, color=l['productColor'], size=size, stock_code=sku,
                                                  unit_price=unitPrice, sales_amount=salesAmount,
                                                  discount_amount=discount, status=status,
                                                  shippment_city=r['shipmentAddress']['city'],
                                                  order_date=datetime_obj_with_tz, commission_price=komisyon_tutari,
                                                  service_price=trendyol.hizmet_bedeli)
                    sendOrderInfoEmail(request=request, platform="Trendyol", email="atmacaahmet5261@hotmail.com", order=data)
            elif len(r['lines']) > 1:
                for l in r['lines']:
                    quantity = l['quantity']
                    size = l['productSize']
                    sku = l['merchantSku']
                    title = l['productName']
                    barcode = l['barcode']
                    try:
                        seller_product = get_object_or_404(ApiProduct, barcode=str(l['barcode']))
                        if seller_product.subcategory == "Üst Giyim":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Üst Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.subcategory == "Alt Giyim":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Alt Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.subcategory == "Dış Giyim":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Dış Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.subcategory == "İç Giyim":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="İç Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.subcategory == "Ayakkabı":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Ayakkabı").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        elif seller_product.subcategory == "Aksesuar":
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Çanta").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                        else:
                            komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Alt Giyim").komisyon_tutari
                            komisyon_tutari = l['amount'] * komisyon_orani / 100
                    except:
                        komisyon_orani = TrendyolCommission.objects.get(kategori_adi="Alt Giyim").komisyon_tutari
                        komisyon_tutari = l['amount'] * komisyon_orani / 100

                    orderStatus = l['orderLineItemStatusName']
                    if orderStatus == 'UnDeliveredAndReturned':
                        status = "İade Edildi"
                    elif orderStatus == 'Picking':
                        status = "Hazırlanıyor"
                    elif orderStatus == "Deliverd":
                        status = "Tamamlandı"
                    elif orderStatus == "Cancelled":
                        status = "İptal Edildi"
                    elif orderStatus == "Created" or orderStatus == "ReadyToShip":
                        status = "Yeni"
                    elif orderStatus == "Shipped":
                        status = "Kargolandı"
                    else:
                        status = "Kargolandı"
                    discount = l['discount']
                    unitPrice = l['amount']
                    salesAmount = l['price']
                    TrendyolMoreProductOrder.objects.create(order_number=orderNumber, barcode=barcode, title=title, packet_number=packetNumber, color=l['productColor'], quantity=quantity,  size=size, stock_code=sku,
                                              unit_price=unitPrice, sales_amount=salesAmount,
                                              discount_amount=discount, status=status)
                birim_fiyat = 0
                satis_fiyat = 0
                indirim = 0
                miktar = 0
                for product in TrendyolMoreProductOrder.objects.filter(order_number=orderNumber, packet_number=packetNumber):
                    birim_fiyat += product.unit_price
                    satis_fiyat += product.sales_amount
                    indirim += product.discount_amount
                    miktar += product.quantity


                data = TrendyolOrders.objects.create(order_number=orderNumber, packet_number=packetNumber,
                                              buyer=customerName, quantity=miktar, title="Birden Fazla Ürün",
                                              barcode="Birden Fazla Barkod", color="Birden Fazla Ürün", size="Birden Fazla Ürün", stock_code="Birden Fazla STK",
                                              unit_price=birim_fiyat, sales_amount=satis_fiyat,
                                              discount_amount=indirim, status="Birden Fazla",
                                              shippment_city=r['shipmentAddress']['city'],
                                              order_date=datetime_obj_with_tz, commission_price=komisyon_tutari,
                                              service_price=trendyol.hizmet_bedeli)
                sendOrderInfoEmail(request=request, platform="Trendyol", email="atmacaahmet5261@hotmail.com", order=data)
    messages.success(request, "Siparişler getirildi.")
    return redirect('trendyol_orders')


@login_required(login_url="/yonetim/giris-yap/")
def order_detail(request, order_number):
    context = {}
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    order = get_object_or_404(Order, order_number=order_number)

    sorgu_durum = paytr_sorgu(order_number=order_number)

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'order': order,
        'sorgu_durum': sorgu_durum
    })

    if 'uploadFaturaBtn' in request.POST:
        file = request.FILES['bill']
        order.bill = file
        order.save()
        messages.success(request, 'Fatura yüklendi.')
        return redirect('admin_order_detail', order_number)
    return render(request, 'backend/adminpage/pages/siparis_yonetimi/order_detail.html', context)

@login_required(login_url="/yonetim/giris-yap/")
def order_isleme_al(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    order.status = "Hazırlanıyor"
    order.save()
    messages.success(request, 'Sipariş hazırlanma aşamasına geçildi.')
    return redirect('admin_order_detail', order_number)

@login_required(login_url="/yonetim/giris-yap/")
def order_kargo_bildir(request, order_number):

    kargo_firmasi = request.POST.get("kargo_firmasi")
    takip_numarasi = request.POST.get("takip_numarasi")
    takip_linki = request.POST.get("takip_linki")

    order = get_object_or_404(Order, order_number=order_number)
    order.delivery_name = kargo_firmasi
    order.delivery_track = takip_numarasi
    order.track_link = takip_linki
    order.status = "Kargolandı"
    order.save()

    data = "success"
    return JsonResponse(data=data, safe=False)

@login_required(login_url="/yonetim/giris-yap/")
def order_mail_gonder(request, order_number):

    order = get_object_or_404(Order, order_number=order_number)
    total = 0
    order_list = OrderProduct.objects.filter(order=order)

    for p in order_list:
        total += (float(p.quantity * p.product_price))

    customerTredyShopDeliveryOrder(request=request, order=order, order_list=order_list, total=total, email=order.user.email, grand_total=order.order_total, address=order.address.address)

    messages.success(request, 'E-Posta gönderildi.')
    return redirect('admin_order_detail', order_number)

@login_required(login_url="/yonetim/giris-yap/")
def trendyol_order_detail(request, id):
    context = {}
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    order = get_object_or_404(TrendyolOrders, id=id)

    order_products = TrendyolMoreProductOrder.objects.filter(order_number=order.order_number, packet_number=order.packet_number)
    harcamalar = Harcamalar.objects.filter(siparis_numarasi=order.order_number)

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'order': order,
        'order_products':order_products,
        'harcamalar':harcamalar
    })

    if 'addTrendyolCost' in request.POST:
        delivery_price = request.POST.get('delivery_price',0.0)
        commission_price = request.POST.get('commission_price',0.0)
        service_price = request.POST.get('service_price',0.0)

        order.delivery_price = delivery_price
        order.commission_price = commission_price
        order.service_price = service_price
        order.save()
        messages.success(request, 'Sipariş güncellendi.')
        return redirect('trendyol_order_detail', id)

    if 'returnStatusBtn' in request.POST:
        is_return = request.POST.get('is_return')

        if is_return == None or is_return == "None":
            order.is_return = False
        else:
            order.is_return = True
            created_at = datetime.now()
            for harcama in Harcamalar.objects.filter(siparis_numarasi=order.order_number):
                Harcamalar.objects.create(siparis_numarasi=order.order_number, harcama_adi=harcama.harcama_adi, harcama_tutari=harcama.harcama_tutari, harcama_notu=harcama.harcama_notu, harcama_tipi="Ürün Alımı", durum="İade Yapıldı", created_at=created_at)
        order.save()
        messages.success(request, 'Sipariş iade edildi.')
        return redirect('trendyol_order_detail', id)

    return render(request, 'backend/adminpage/pages/trendyol/order_detail.html', context)

@login_required(login_url="/yonetim/giris-yap/")
def urun_maliyeti_ekle(request):
    siparis_no = request.POST.get('siparis_no')
    harcama_adi = request.POST.get('harcama_adi')
    harcama_tutari = request.POST.get('harcama_tutari')
    harcama_not = request.POST.get('harcama_not')

    created_at = datetime.now()

    Harcamalar.objects.create(siparis_numarasi=siparis_no, harcama_adi=harcama_adi, harcama_tutari=harcama_tutari, harcama_notu=harcama_not, harcama_tipi="Ürün Alımı", durum="Ödeme Yapıldı", created_at=created_at)
    data = 'success'
    return JsonResponse(data=data, safe=False)

@login_required(login_url="/yonetim/giris-yap/")
def order_delete(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order.delete()
    messages.success(request, 'Sipariş silindi.')
    return redirect('admin_orders')


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_order_delete(request, id):
    order = TrendyolOrders.objects.get(id=id)
    order.delete()
    messages.success(request, 'Sipariş silindi.')
    return redirect('trendyol_orders')


@login_required(login_url="/yonetim/giris-yap/")
def iptal_talepleri(request):
    context = {}
    cancelling = CancellationRequest.objects.all()
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    p = Paginator(cancelling, 20)
    page = request.GET.get('page')
    cancellings = p.get_page(page)

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'cancellings': cancellings,
    })

    return render(request, 'backend/adminpage/pages/siparis_yonetimi/iptal_talepleri.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def iade_talepleri(request):
    context = {}
    extradition = ExtraditionRequest.objects.all()
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    p = Paginator(extradition, 20)
    page = request.GET.get('page')
    extraditions = p.get_page(page)

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'extraditions': extraditions,
    })

    return render(request, 'backend/adminpage/pages/siparis_yonetimi/iade_talepleri.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def iade_talepleri_detay(request, order_number, product_id):
    context = {}
    product = ApiProduct.objects.get(id=product_id)
    extradition = ExtraditionRequest.objects.get(order__order_number=order_number, product=product)
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()
    orderproduct = OrderProduct.objects.filter(order__order_number=order_number)

    form = ExtraditionRequestResultForm(data=request.POST, files=request.FILES)
    if ExtraditionRequestResult.objects.filter(extraditionrequest=extradition).exists():
        form = ExtraditionRequestResultForm(
            instance=ExtraditionRequestResult.objects.filter(extraditionrequest=extradition).last(), data=request.POST,
            files=request.FILES)

    if 'updateBtn' in request.POST:
        if form.is_valid():
            data = form.save(commit=False)
            data.extraditionrequest = extradition
            data.save()
            messages.success(request, 'İade talebi güncellendi.')
            return redirect('iptal_talepleri_detay', order_number)

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'extradition': extradition,
        'form': form,
        'orderproduct': orderproduct,
    })

    return render(request, 'backend/adminpage/pages/siparis_yonetimi/iade_talepleri_detay.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def tahtakale_product(request):
    return render(request, "backend/adminpage/pages/xml_yonetimi/tahtakale.html")


@login_required(login_url="/yonetim/giris-yap/")
def tahtakale_product_load(request):
    try:
        tahtakaleSaveXML2db()
        messages.success(request, 'Veriler yüklendi!')
        return redirect("tahtakale_product")
    except:
        return redirect("tahtakale_product")


@login_required(login_url="/yonetim/giris-yap/")
def tahtakale_product_update(request):
    try:
        updateTahtakaleSaveXML2db()
        createNotification(type="2", title="Tahtakale ürünlerinin güncellemesi yapıldı.",
                           detail="Tahtakale ürünlerinin güncellemesi yapıldı.")
        messages.success(request, 'Veriler güncelledi!')
        return redirect("tahtakale_product")
    except:
        return redirect("tahtakale_product")


@login_required(login_url="/yonetim/giris-yap/")
def haydigiy_product(request):
    context = {}
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
    })

    return render(request, "backend/adminpage/pages/xml_yonetimi/haydigiy.html", context)


@login_required(login_url="/yonetim/giris-yap/")
def haydigiy_product_load(request):
    try:
        modaymissaveXML2db()
        messages.success(request, 'Veriler yüklendi!')
        return redirect("haydigiy_product")
    except Exception as e:
        return redirect("haydigiy_product")


@login_required(login_url="/yonetim/giris-yap/")
def haydigiy_product_update(request):
    updateModaymisSaveXML2db()
    createNotification(type="2", title="Modaymış ürünlerinin güncellemesi yapıldı.",
                       detail="Modaymış ürünlerinin güncellemesi yapıldı.")
    messages.success(request, 'Veriler güncelledi!')
    return redirect("haydigiy_product")


@login_required(login_url="/yonetim/giris-yap/")
def haydigiy_find_not_active_product_page(request):
    context = {}
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
    })

    return render(request, "backend/adminpage/pages/xml_yonetimi/haydigiy_not_active.html", context)


@login_required(login_url="/yonetim/giris-yap/")
def haydigiy_find_not_active_product(request):
    notActiveModaymisProduct()
    createNotification(type="2", title="Modaymış ürünlerde aktif olmayanlar bulundu.",
                       detail="Modaymış ürünlerinde aktif olmayan ürünler aktif değildir olarak güncellendi.")
    messages.success(request, 'Modaymış ürünlerde aktif olmayanlar bulundu')
    return redirect("haydigiy_find_not_active_product_page")


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_hesap_bilgileri_ekle(request):
    context = {}
    trendyol = Trendyol.objects.all()
    if trendyol.count() > 0:
        form = TrendyolUpdateForm(instance=trendyol.last(), data=request.POST or None,
                                  files=request.FILES or None)
        context.update({'form': form})
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'Trendyol hesap bilgileri başarıyla güncellendi!')
                return redirect("trendyol_hesap_bilgileri_ekle")
    else:
        form = TrendyolAddForm(data=request.POST, files=request.FILES)
        context.update({'form': form})
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'Trendyol hesap bilgileri başarıyla eklendi!')
                return redirect("trendyol_hesap_bilgileri_ekle")

    return render(request, 'backend/adminpage/pages/trendyol/trendyol.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_add_product(request):
    return render(request, 'backend/adminpage/pages/trendyol/urun_girisi.html')


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_add_product_giyim(request):
    return render(request, 'backend/adminpage/pages/trendyol/urun_girisi_giyim.html')


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_add_product_giyim_category1(request, category_no):
    context = {}
    subcategory = SubCategory.objects.get(category_no=category_no)
    categories = SubBottomCategory.objects.filter(subcategory__category_no=category_no)
    context.update({'categories': categories, 'subcategory': subcategory})
    return render(request, 'backend/adminpage/pages/trendyol/urun_girisi_giyim_category1.html', context)


def trendyolProductData(barcode, title, model_code, brandid, categoryid, quantity, stock_code, desi, description,
                        list_price, sale_price, vatRate, deliveryDuration, cargoid, shipmentid, returningid, images,
                        data_attributes):
    data = {
        "barcode": str(barcode),
        "title": str(title),
        "productMainId": str(model_code),
        "brandId": int(brandid),
        "categoryId": int(categoryid),
        "quantity": int(quantity),
        "stockCode": str(stock_code),
        "dimensionalWeight": int(desi),
        "description": description,
        "currencyType": "TRY",
        "listPrice": float(list_price),
        "salePrice": float(sale_price),
        "vatRate": int(vatRate),
        "deliveryDuration": int(deliveryDuration),
        "cargoCompanyId": int(cargoid),
        "shipmentAddressId": int(shipmentid),
        "returningAddressId": int(returningid),
        "images": images,
        "attributes": data_attributes
    }

    return data


def trendyolUpdateProductData(barcode, title, model_code, brandid, categoryid, stock_code, description, vatRate,
                              deliveryDuration, cargoid, shipmentid, returningid, images,
                              data_attributes):
    data = {
        "barcode": str(barcode),
        "title": str(title),
        "productMainId": str(model_code),
        "brandId": int(brandid),
        "categoryId": int(categoryid),
        "stockCode": str(stock_code),
        "description": description,
        "currencyType": "TRY",
        "vatRate": int(vatRate),
        "deliveryDuration": int(deliveryDuration),
        "images": images,
        "attributes": data_attributes,
        "cargoCompanyId": int(cargoid),
        "shipmentAddressId": int(shipmentid),
        "returningAddressId": int(returningid),
    }

    return data


def trendyolUpdateData(barcode, quantity, list_price, sale_price):
    data = {
        "barcode": str(barcode),
        "quantity": int(quantity),
        "listPrice": float(list_price),
        "salePrice": float(sale_price)
    }

    return data


def trendyolDeleteData(products):
    data = []

    for p in products:
        data.append(
            {
                "barcode": str(p.barcode)
            }
        )

    return data


def callingProduct(category, title):
    products = ApiProduct.objects.filter(subbottomcategory=category, title__icontains=title, is_publish=True,
                                         is_publish_trendyol=False)
    return products


def updateCallingProduct(category, title):
    products = ApiProduct.objects.filter(subbottomcategory=category, title__icontains=title, is_publish=True,
                                         is_publish_trendyol=True)
    return products


def trendyolAttributes(trendyol_category):
    attributes_url = f"https://api.trendyol.com/sapigw/product-categories/{trendyol_category}/attributes"
    product_attributes = requests.request("GET", attributes_url)
    product_attributes = product_attributes.json()
    return product_attributes


def trendyolCategory(category_title):
    categories = requests.get("https://api.trendyol.com/sapigw/product-categories")

    trendyol_category = None

    for c in categories.json()['categories']:
        for c1 in c['subCategories']:
            if c1['subCategories'] != []:
                for c2 in c1['subCategories']:
                    if c2['subCategories'] != []:
                        for c3 in c2['subCategories']:
                            if c3['subCategories'] != []:
                                for c4 in c3['subCategories']:
                                    if c4['subCategories'] != []:
                                        for c5 in c4['subCategories']:
                                            if category_title.lower() == str(c5['name']).lower():
                                                trendyol_category = c5['id']
                                    else:
                                        if category_title.lower() == str(c4['name']).lower():
                                            trendyol_category = c4['id']
                            else:
                                if category_title.lower() == str(c3['name']).lower():
                                    trendyol_category = c3['id']
                    else:
                        if category_title.lower() == str(c2['name']).lower():
                            trendyol_category = c2['id']
            else:
                if category_title.lower() == str(c1['name']).lower():
                    trendyol_category = c1['id']

    return trendyol_category


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_add_product_giyim_send_trendyol(request, id):
    context = {}
    trendyol = Trendyol.objects.all().last()
    category = SubBottomCategory.objects.get(id=id)
    log_record = LogRecords.objects.filter(log_type="1")
    if log_record.count() > 20:
        log_record = log_record[:20]
    context.update({'category': category, 'log_record': log_record})
    product_data = []
    items = []
    data_attributes = []
    trendyol_category = None

    attributes = []

    if 'sendTrendyol' in request.POST:
        category_title = request.POST.get('category_title')
        product_title = request.POST.get('product_title')

        if category_title == "Triko":
            category_title = "Atlet"

        trendyol_category = trendyolCategory(category_title)

        ##Attributes
        product_attributes = trendyolAttributes(trendyol_category)

        ##Calling Product
        products = callingProduct(category, product_title)

        if trendyol_category:
            for a in product_attributes['categoryAttributes']:
                attributes.append(a)

            for p in products:
                title = p.title
                detail = p.detail
                if detail == '' or detail == None:
                    detail = title
                images = []
                if p.image_url1:
                    images.append({'url': p.image_url1})
                if p.image_url2:
                    images.append({'url': p.image_url2})
                if p.image_url3:
                    images.append({'url': p.image_url3})
                if p.image_url4:
                    images.append({'url': p.image_url4})
                if p.image_url5:
                    images.append({'url': p.image_url5})
                if p.image_url6:
                    images.append({'url': p.image_url6})
                if p.image_url7:
                    images.append({'url': p.image_url7})
                if p.image_url8:
                    images.append({'url': p.image_url8})

                for a in attributes:
                    if a['attribute']['name'] == 'Beden':
                        if p.size:
                            for s in a['attributeValues']:
                                if p.size.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Yaş Grubu':
                        if p.age_group:
                            for s in a['attributeValues']:
                                if p.age_group == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Cinsiyet':
                        if p.sextype:
                            for s in a['attributeValues']:
                                if p.sextype.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == "Kumaş Tipi":
                        if p.fabrictype:
                            for s in a['attributeValues']:
                                if p.fabrictype.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Boy':
                        if p.height:
                            for s in a['attributeValues']:
                                if p.height.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Bel':
                        if p.waist:
                            for s in a['attributeValues']:
                                if p.waist.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Kalıp':
                        if p.pattern:
                            for s in a['attributeValues']:
                                if p.pattern.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Kol Tipi':
                        if p.armtype:
                            for s in a['attributeValues']:
                                if p.armtype.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Yaka Tipi':
                        if p.collartype:
                            for s in a['attributeValues']:
                                if p.collartype.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Dokuma Tipi':
                        if p.weavingtype:
                            for s in a['attributeValues']:
                                if p.weavingtype.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Materyal':
                        if p.material:
                            for s in a['attributeValues']:
                                if p.material.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Ortam':
                        if p.environment:
                            for s in a['attributeValues']:
                                if p.environment.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Paça Tipi':
                        if p.legtype:
                            for s in a['attributeValues']:
                                if p.legtype.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                    if a['attribute']['name'] == 'Cep':
                        if p.pocket:
                            for s in a['attributeValues']:
                                if p.pocket.name == s['name']:
                                    data_attributes.append(
                                        {
                                            "attributeId": a['attribute']['id'],
                                            "attributeValueId": s['id']
                                        }
                                    )
                if p.color is not None:
                    data_attributes.append(
                        {
                            "attributeId": 47,
                            "customAttributeValue": str(p.color.name).upper()
                        }
                    )

                items.append(
                    trendyolProductData(barcode=p.barcode, title=title, model_code=p.stock_code, brandid=996771,
                                        categoryid=trendyol_category, quantity=p.quantity, stock_code=p.stock_code,
                                        desi=1,
                                        list_price=p.trendyol_price, sale_price=p.trendyol_price, cargoid=10,
                                        description=detail, vatRate=10, deliveryDuration=2,
                                        shipmentid=trendyol.sevkiyatadresid_1,
                                        returningid=trendyol.iadeadresid_1, images=images,
                                        data_attributes=data_attributes))

                product_data = items
                data_attributes = []
                p.trendyol_category_id = int(trendyol_category)
                p.save()

        try:
            api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                                    supplier_id=trendyol.saticiid)
            service = ProductIntegrationService(api)
            response = service.create_products(items=product_data)
            messages.success(request, f"{response}")
            log_record = LogRecords.objects.create(log_type="1", batch_id=str(response['batchRequestId']))
            return redirect('trendyol_batch_request_detail', str(log_record.batch_id))
        except Exception as e:
            messages.error(request, f"{e}")
        return redirect('trendyol_add_product_giyim_send_trendyol', id)
    return render(request, 'backend/adminpage/pages/trendyol/urun_girisi_giyim_send_trendyol.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_update_function(request, products):
    items = []
    product_data = []
    trendyol = Trendyol.objects.all().last()
    result = 'success'

    if products.count() > 0:
        for p in products:
            listprice = p.trendyol_price
            saleprice = p.trendyol_price
            if saleprice > trendyol.firstbarem and saleprice <= 102:
                saleprice = trendyol.firstbarem

            if saleprice > trendyol.secondbarem and saleprice <= 151:
                saleprice = trendyol.secondbarem

            if p.quantity > 2:
                items.append(
                    trendyolUpdateData(barcode=p.barcode, quantity=p.quantity, list_price=listprice,
                                       sale_price=saleprice)
                )
            else:
                items.append(
                    trendyolUpdateData(barcode=p.barcode, quantity=0, list_price=listprice,
                                       sale_price=saleprice)
                )

            product_data = items
        try:
            api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                                    supplier_id=trendyol.saticiid)
            service = ProductIntegrationService(api)
            response = service.update_price_and_stock(items=product_data)
            log_record = LogRecords.objects.create(log_type="2", batch_id=response['batchRequestId'])
            UpdateHistory.objects.create(history_type="Trendyol Stok&Fiyat Güncelleme")
        except:
            result = 'failed'
        return result


def trendyol_schedule_update_price_stok(request):
    total_product = ApiProduct.objects.all().filter(is_publish_trendyol=True).count()
    result = total_product / 999
    i = 0

    while (i < result):
        j = 0
        if i == 0:
            j = 0
            products = ApiProduct.objects.filter(is_publish_trendyol=True)[j:999]
            trendyol_update_function(request, products=products)
        else:
            j = i * 1000
            products = ApiProduct.objects.filter(is_publish_trendyol=True)[j - 1:j + 999]
            trendyol_update_function(request, products=products)
        i = i + 1


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_update_price_stok(request):
    context = {}
    log_records = LogRecords.objects.filter(log_type="2")
    if log_records.count() > 20:
        log_records = log_records[:20]
    context.update({
        'log_records': log_records
    })

    total_product = ApiProduct.objects.all().filter(is_publish_trendyol=True).count()
    messages.success(request, f"Toplam Ürün Sayısı: {total_product}")
    trendyol = Trendyol.objects.all().last()

    if 'updateBtn' in request.POST:
        result = ceil(total_product / 999)
        i = 0

        while i < result:
            if i == 0:
                j = 0
                products = ApiProduct.objects.filter(is_publish_trendyol=True)[j:999]
                trendyol_update_function(request, products=products)
            else:
                j = i * 1000
                products = ApiProduct.objects.filter(is_publish_trendyol=True)[j - 1:j + 999]
                trendyol_update_function(request, products=products)
            i = i + 1
        return redirect('trendyol_update_price_stok')
    return render(request, 'backend/adminpage/pages/trendyol/stok_fiyat_guncelleme.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_update_product(request):
    context = {}
    return render(request, 'backend/adminpage/pages/trendyol/bilgi_guncelleme.html', context)


def trendyolDeleteData(barcode):
    data = {
        "barcode": str(barcode),
    }

    return data


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_delete_api(request, products):
    trendyol = Trendyol.objects.all().last()
    items = []
    if products.count() > 0:
        for p in products:
            items.append(
                {'barcode': str(p.barcode)}
            )

    api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                            supplier_id=trendyol.saticiid)
    service = ProductIntegrationService(api)
    response = service.deleted_products(items=items)
    messages.success(request, f"{response}")
    log_record = LogRecords.objects.create(log_type="4", batch_id=response['batchRequestId'])
    return str(log_record.batch_id)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_delete_product(request):
    context = {}
    log_records = LogRecords.objects.filter(log_type="4")
    products = ApiProduct.objects.filter(is_publish_trendyol=True, is_publish=False)
    products_count = ApiProduct.objects.filter(is_publish_trendyol=True, is_publish=False).count()
    if 'inactiveDeleteBtn' in request.POST:
        if products_count == 0 and products_count <= 999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
        elif products_count > 999 and products_count <= 1999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
            products2 = products[999:1999]
            trendyol_delete_api(request, products=products2)
        elif products_count > 1999 and products_count <= 2999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
            products2 = products[999:1999]
            trendyol_delete_api(request, products=products2)
            products3 = products[1999:2999]
            trendyol_delete_api(request, products=products3)
        elif products_count > 2999 and products_count <= 3999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
            products2 = products[999:1999]
            trendyol_delete_api(request, products=products2)
            products3 = products[1999:2999]
            trendyol_delete_api(request, products=products3)
            products4 = products[2999:3999]
            trendyol_delete_api(request, products=products4)
        elif products_count > 3999 and products_count <= 4999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
            products2 = products[999:1999]
            trendyol_delete_api(request, products=products2)
            products3 = products[1999:2999]
            trendyol_delete_api(request, products=products3)
            products4 = products[2999:3999]
            trendyol_delete_api(request, products=products4)
            products5 = products[3999:4999]
            trendyol_delete_api(request, products=products5)
        elif products_count > 4999 and products_count <= 5999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
            products2 = products[999:1999]
            trendyol_delete_api(request, products=products2)
            products3 = products[1999:2999]
            trendyol_delete_api(request, products=products3)
            products4 = products[2999:3999]
            trendyol_delete_api(request, products=products4)
            products5 = products[3999:4999]
            trendyol_delete_api(request, products=products5)
            products6 = products[4999:5999]
            trendyol_delete_api(request, products=products6)
        elif products_count > 5999 and products_count <= 6999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
            products2 = products[999:1999]
            trendyol_delete_api(request, products=products2)
            products3 = products[1999:2999]
            trendyol_delete_api(request, products=products3)
            products4 = products[2999:3999]
            trendyol_delete_api(request, products=products4)
            products5 = products[3999:4999]
            trendyol_delete_api(request, products=products5)
            products6 = products[4999:5999]
            trendyol_delete_api(request, products=products6)
            products7 = products[5999:6999]
            trendyol_delete_api(request, products=products7)
        elif products_count > 6999 and products_count <= 7999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
            products2 = products[999:1999]
            trendyol_delete_api(request, products=products2)
            products3 = products[1999:2999]
            trendyol_delete_api(request, products=products3)
            products4 = products[2999:3999]
            trendyol_delete_api(request, products=products4)
            products5 = products[3999:4999]
            trendyol_delete_api(request, products=products5)
            products6 = products[4999:5999]
            trendyol_delete_api(request, products=products6)
            products7 = products[5999:6999]
            trendyol_delete_api(request, products=products7)
            products8 = products[6999:7999]
            trendyol_delete_api(request, products=products8)
        elif products_count > 7999 and products_count <= 8999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
            products2 = products[999:1999]
            trendyol_delete_api(request, products=products2)
            products3 = products[1999:2999]
            trendyol_delete_api(request, products=products3)
            products4 = products[2999:3999]
            trendyol_delete_api(request, products=products4)
            products5 = products[3999:4999]
            trendyol_delete_api(request, products=products5)
            products6 = products[4999:5999]
            trendyol_delete_api(request, products=products6)
            products7 = products[5999:6999]
            trendyol_delete_api(request, products=products7)
            products8 = products[6999:7999]
            trendyol_delete_api(request, products=products8)
            products9 = products[7999:8999]
            trendyol_delete_api(request, products=products9)
        elif products_count > 8999 and products_count <= 9999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
            products2 = products[999:1999]
            trendyol_delete_api(request, products=products2)
            products3 = products[1999:2999]
            trendyol_delete_api(request, products=products3)
            products4 = products[2999:3999]
            trendyol_delete_api(request, products=products4)
            products5 = products[3999:4999]
            trendyol_delete_api(request, products=products5)
            products6 = products[4999:5999]
            trendyol_delete_api(request, products=products6)
            products7 = products[5999:6999]
            trendyol_delete_api(request, products=products7)
            products8 = products[6999:7999]
            trendyol_delete_api(request, products=products8)
            products9 = products[7999:8999]
            trendyol_delete_api(request, products=products9)
            products10 = products[8999:9999]
            trendyol_update_function(request, products=products10)
        elif products_count > 9999 and products_count <= 10999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
            products2 = products[999:1999]
            trendyol_delete_api(request, products=products2)
            products3 = products[1999:2999]
            trendyol_delete_api(request, products=products3)
            products4 = products[2999:3999]
            trendyol_delete_api(request, products=products4)
            products5 = products[3999:4999]
            trendyol_delete_api(request, products=products5)
            products6 = products[4999:5999]
            trendyol_delete_api(request, products=products6)
            products7 = products[5999:6999]
            trendyol_delete_api(request, products=products7)
            products8 = products[6999:7999]
            trendyol_delete_api(request, products=products8)
            products9 = products[7999:8999]
            trendyol_delete_api(request, products=products9)
            products10 = products[8999:9999]
            trendyol_delete_api(request, products=products10)
            products11 = products[9999:10999]
            trendyol_delete_api(request, products=products11)
        elif products_count > 10999 and products_count <= 11999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
            products2 = products[999:1999]
            trendyol_delete_api(request, products=products2)
            products3 = products[1999:2999]
            trendyol_delete_api(request, products=products3)
            products4 = products[2999:3999]
            trendyol_delete_api(request, products=products4)
            products5 = products[3999:4999]
            trendyol_delete_api(request, products=products5)
            products6 = products[4999:5999]
            trendyol_delete_api(request, products=products6)
            products7 = products[5999:6999]
            trendyol_delete_api(request, products=products7)
            products8 = products[6999:7999]
            trendyol_delete_api(request, products=products8)
            products9 = products[7999:8999]
            trendyol_delete_api(request, products=products9)
            products10 = products[8999:9999]
            trendyol_delete_api(request, products=products10)
            products11 = products[9999:10999]
            trendyol_delete_api(request, products=products11)
            products12 = products[10999:11999]
            trendyol_delete_api(request, products=products12)
        elif products_count > 11999 and products_count <= 12999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
            products2 = products[999:1999]
            trendyol_delete_api(request, products=products2)
            products3 = products[1999:2999]
            trendyol_delete_api(request, products=products3)
            products4 = products[2999:3999]
            trendyol_delete_api(request, products=products4)
            products5 = products[3999:4999]
            trendyol_delete_api(request, products=products5)
            products6 = products[4999:5999]
            trendyol_delete_api(request, products=products6)
            products7 = products[5999:6999]
            trendyol_delete_api(request, products=products7)
            products8 = products[6999:7999]
            trendyol_delete_api(request, products=products8)
            products9 = products[7999:8999]
            trendyol_delete_api(request, products=products9)
            products10 = products[8999:9999]
            trendyol_delete_api(request, products=products10)
            products11 = products[9999:10999]
            trendyol_delete_api(request, products=products11)
            products12 = products[10999:11999]
            trendyol_delete_api(request, products=products12)
            products13 = products[11999:12999]
            trendyol_delete_api(request, products=products13)
        elif products_count > 12999 and products_count <= 13999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
            products2 = products[999:1999]
            trendyol_delete_api(request, products=products2)
            products3 = products[1999:2999]
            trendyol_delete_api(request, products=products3)
            products4 = products[2999:3999]
            trendyol_delete_api(request, products=products4)
            products5 = products[3999:4999]
            trendyol_delete_api(request, products=products5)
            products6 = products[4999:5999]
            trendyol_delete_api(request, products=products6)
            products7 = products[5999:6999]
            trendyol_delete_api(request, products=products7)
            products8 = products[6999:7999]
            trendyol_delete_api(request, products=products8)
            products9 = products[7999:8999]
            trendyol_delete_api(request, products=products9)
            products10 = products[8999:9999]
            trendyol_delete_api(request, products=products10)
            products11 = products[9999:10999]
            trendyol_delete_api(request, products=products11)
            products12 = products[10999:11999]
            trendyol_delete_api(request, products=products12)
            products13 = products[11999:12999]
            trendyol_delete_api(request, products=products13)
            products14 = products[12999:13999]
            trendyol_delete_api(request, products=products14)
        elif products_count > 13999 and products_count <= 14999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
            products2 = products[999:1999]
            trendyol_delete_api(request, products=products2)
            products3 = products[1999:2999]
            trendyol_delete_api(request, products=products3)
            products4 = products[2999:3999]
            trendyol_delete_api(request, products=products4)
            products5 = products[3999:4999]
            trendyol_delete_api(request, products=products5)
            products6 = products[4999:5999]
            trendyol_delete_api(request, products=products6)
            products7 = products[5999:6999]
            trendyol_delete_api(request, products=products7)
            products8 = products[6999:7999]
            trendyol_delete_api(request, products=products8)
            products9 = products[7999:8999]
            trendyol_delete_api(request, products=products9)
            products10 = products[8999:9999]
            trendyol_delete_api(request, products=products10)
            products11 = products[9999:10999]
            trendyol_delete_api(request, products=products11)
            products12 = products[10999:11999]
            trendyol_delete_api(request, products=products12)
            products13 = products[11999:12999]
            trendyol_delete_api(request, products=products13)
            products14 = products[12999:13999]
            trendyol_delete_api(request, products=products14)
            products15 = products[13999:14999]
            trendyol_delete_api(request, products=products15)
        elif products_count > 14999 and products_count <= 15999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
            products2 = products[999:1999]
            trendyol_delete_api(request, products=products2)
            products3 = products[1999:2999]
            trendyol_delete_api(request, products=products3)
            products4 = products[2999:3999]
            trendyol_delete_api(request, products=products4)
            products5 = products[3999:4999]
            trendyol_delete_api(request, products=products5)
            products6 = products[4999:5999]
            trendyol_delete_api(request, products=products6)
            products7 = products[5999:6999]
            trendyol_delete_api(request, products=products7)
            products8 = products[6999:7999]
            trendyol_delete_api(request, products=products8)
            products9 = products[7999:8999]
            trendyol_delete_api(request, products=products9)
            products10 = products[8999:9999]
            trendyol_delete_api(request, products=products10)
            products11 = products[9999:10999]
            trendyol_delete_api(request, products=products11)
            products12 = products[10999:11999]
            trendyol_delete_api(request, products=products12)
            products13 = products[11999:12999]
            trendyol_delete_api(request, products=products13)
            products14 = products[12999:13999]
            trendyol_delete_api(request, products=products14)
            products15 = products[13999:14999]
            trendyol_delete_api(request, products=products15)
            products16 = products[14999:15999]
            trendyol_delete_api(request, products=products16)
        elif products_count > 15999 and products_count <= 16999:
            products = products[:999]
            trendyol_delete_api(request, products=products)
            products2 = products[999:1999]
            trendyol_delete_api(request, products=products2)
            products3 = products[1999:2999]
            trendyol_delete_api(request, products=products3)
            products4 = products[2999:3999]
            trendyol_delete_api(request, products=products4)
            products5 = products[3999:4999]
            trendyol_delete_api(request, products=products5)
            products6 = products[4999:5999]
            trendyol_delete_api(request, products=products6)
            products7 = products[5999:6999]
            trendyol_delete_api(request, products=products7)
            products8 = products[6999:7999]
            trendyol_delete_api(request, products=products8)
            products9 = products[7999:8999]
            trendyol_delete_api(request, products=products9)
            products10 = products[8999:9999]
            trendyol_delete_api(request, products=products10)
            products11 = products[9999:10999]
            trendyol_delete_api(request, products=products11)
            products12 = products[10999:11999]
            trendyol_delete_api(request, products=products12)
            products13 = products[11999:12999]
            trendyol_delete_api(request, products=products13)
            products14 = products[12999:13999]
            trendyol_delete_api(request, products=products14)
            products15 = products[13999:14999]
            trendyol_delete_api(request, products=products15)
            products16 = products[14999:15999]
            trendyol_delete_api(request, products=products16)
            products17 = products[15999:16999]
            trendyol_delete_api(request, products=products17)
        return redirect('trendyol_delete_product')

    context.update({
        'log_records': log_records,
    })
    return render(request, 'backend/adminpage/pages/trendyol/silme.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_add_order(request):
    context = {}
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    form = TrendyolOrderForm(data=request.POST or None,
                             files=request.FILES or None)

    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, "Sipariş kaydı başarıyla girildi.")
            return redirect('trendyol_add_order')

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'form': form
    })

    return render(request, 'backend/adminpage/pages/trendyol/add_orders.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_batch_request(request):
    context = {}
    trendyol = Trendyol.objects.all().last()

    all_batch_request = LogRecords.objects.all()

    paginator = Paginator(all_batch_request, 50)
    page = request.GET.get('page')

    try:
        all_batch_requests = paginator.page(page)
    except PageNotAnInteger:
        all_batch_requests = paginator.page(1)
    except EmptyPage:
        all_batch_requests = paginator.page(paginator.num_pages)

    context.update({
        'all_batch_request': all_batch_requests
    })

    return render(request, 'backend/adminpage/pages/trendyol/batch_request.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_batch_request_detail(request, batch_request):
    context = {}
    trendyol = Trendyol.objects.all().last()

    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    all_batch_request = get_object_or_404(LogRecords, batch_id=batch_request)

    try:
        api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                                supplier_id=trendyol.saticiid)
        service = ProductIntegrationService(api)
        response = service.get_batch_requests(batch_request_id=batch_request)
        request_id = response['batchRequestId']

        if all_batch_request.log_type == "1":
            for i in response['items']:
                if i['status'] == 'SUCCESS':
                    product = ApiProduct.objects.get(barcode=i['requestItem']['product']['barcode'])
                    product.is_publish_trendyol = True
                    product.save()
            context.update({
                'response': response,
                'all_batch_request': all_batch_request
            })

        if all_batch_request.log_type == "4":
            for i in response['items']:
                if i['status'] == 'SUCCESS':
                    product = ApiProduct.objects.get(barcode=i['requestItem']['product']['barcode'])
                    product.is_publish_trendyol = False
                    product.save()
            context.update({
                'response': response,
                'all_batch_request': all_batch_request
            })
    except:
        pass

    return render(request, 'backend/adminpage/pages/trendyol/batch_request_detail.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_batch_request_delete(request, id):
    all_batch_request = LogRecords.objects.get(id=id)
    all_batch_request.delete()
    messages.success(request, 'Batch Request başarıyla silindi!')
    return redirect('trendyol_batch_request')


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_batch_request_delete_all(request):
    all_batch_request = LogRecords.objects.all()
    for br in all_batch_request:
        br.delete()
    messages.success(request, 'Batch Request başarıyla silindi!')
    return redirect('trendyol_batch_request')


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_products(request):
    context = {}
    trendyol = Trendyol.objects.all().last()

    approved = request.GET.get('approved', None)
    barcode = request.GET.get('barcode', None)
    startDate = request.GET.get('startDate', None)
    endDate = request.GET.get('endDate', None)
    page = request.GET.get('page', None)
    dateQueryType = request.GET.get('dateQueryType', None)
    size = request.GET.get('size', 100)

    data = {
        'approved': approved or None,
        'barcode': barcode or None,
        'startDate': startDate or None,
        'endDate': endDate or None,
        'page': page or None,
        'dateQueryType': dateQueryType or None,
        'size': size
    }

    try:
        api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                                supplier_id=trendyol.saticiid)
        service = ProductIntegrationService(api)
        response = service.get_products(filter_params=data)
        context.update({
            'response': response,
        })

        product_data = []

        for p in response['content']:
            product_data.append(p)

        context.update({
            'total_elements': response['totalElements'],
            'product_data': product_data
        })
    except:
        pass

    return render(request, 'backend/adminpage/pages/trendyol/urunler.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_hatali_urunler(request):
    context = {}
    trendyol = Trendyol.objects.all().last()

    approved = request.GET.get('approved', None)
    barcode = request.GET.get('barcode', None)
    startDate = request.GET.get('startDate', None)
    endDate = request.GET.get('endDate', None)
    page = request.GET.get('page', None)
    dateQueryType = request.GET.get('dateQueryType', None)
    size = request.GET.get('size', 100)

    data = {
        'approved': approved or None,
        'barcode': barcode or None,
        'startDate': startDate or None,
        'endDate': endDate or None,
        'page': page or None,
        'dateQueryType': dateQueryType or None,
        'size': size
    }

    api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                            supplier_id=trendyol.saticiid)
    service = ProductIntegrationService(api)
    response = service.get_products(filter_params=data)
    context.update({
        'response': response,
    })
    product_data = []
    trendyol_product_data = []
    all_data = []
    equal_data = []

    tredyshop_product = ApiProduct.objects.filter(is_publish_trendyol=True)

    for p in response['content']:
        trendyol_product_data.append(p)
    for tp in trendyol_product_data:
        all_data.append(tp['barcode'])
        for p in tredyshop_product:
            if tp['barcode'] == p.barcode:
                equal_data.append(tp['barcode'])

    difference = list(set(all_data) - set(equal_data))

    for p in trendyol_product_data:
        for d in difference:
            if p['barcode'] == d:
                product_data.append(p)

    context.update({
        'total_elements': len(product_data),
        'product_data': product_data,
    })

    return render(request, 'backend/adminpage/pages/trendyol/hatali_urunler.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_komisyon(request):
    context = {}

    komisyonlar = TrendyolCommission.objects.all()
    form = TrendyolCommissionForm(data=request.POST, files=request.FILES)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Komisyon başarıyla eklendi!')
            return redirect("trendyol_komisyon")

    context.update({
        'form': form,
        'komisyonlar': komisyonlar,
    })

    return render(request, 'backend/adminpage/pages/trendyol/komisyon.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_komisyon_detay(request, id):
    context = {}

    komisyon = get_object_or_404(TrendyolCommission, id=id)
    form = TrendyolCommissionForm(instance=komisyon, data=request.POST or None, files=request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Güncelleme başarıyla yapıldı!')
            return redirect('trendyol_komisyon_detay', id)

    context.update({
        'komisyon': komisyon,
        'form': form,
    })
    return render(request, 'backend/adminpage/pages/trendyol/komisyon_guncelle.html', context)


def trendyol_komisyon_export_excel(request):
    columns = ['Kategori Adı', 'Komisyon Tutarı', 'Oluşturulma Tarihi', 'Güncellenme Tarihi']

    rows = TrendyolCommission.objects.all().values_list('kategori_adi', 'komisyon_tutari', 'create_at', 'update_at')
    return exportExcel('Harcamalar', 'Harcamalar', columns=columns, rows=rows)


def trendyol_komisyon_export_pdf(request):
    columns = ['Kategori Adı', 'Komisyon Tutarı', 'Oluşturulma Tarihi', 'Güncellenme Tarihi']
    rows = []
    row = Harcamalar.objects.all().values_list('kategori_adi', 'komisyon_tutari', 'create_at', 'update_at')
    for r in row:
        rows.append(r)

    dict = {
        'columns': columns,
        'rows': rows
    }

    pdf = exportPdf(f"{str(settings.BASE_DIR)}" + "/templates/backend/adminpage/partials/table_pdf.html", dict)
    response = HttpResponse(pdf, content_type='application/pdf')
    content = f'attachment; filename=KomisyonOranlari' + '.pdf'
    response['Content-Disposition'] = content

    return response


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_komisyon_hepsini_sil(request):
    komisyon = TrendyolCommission.objects.all().delete()
    messages.success(request, 'Tüm komisyonlar silindi.')
    return redirect("trendyol_komisyon")


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_komisyon_secilileri_sil(request):
    komisyon_id = request.GET.getlist('komisyon[]')

    TrendyolCommission.objects.filter(id__in=komisyon_id).delete()
    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def hepsiburada_hesap_bilgileri(request):
    context = {}
    hepsiburada = Hepsiburada.objects.all()

    if hepsiburada.count() > 0:
        form = HepsiburadaForm(instance=hepsiburada.last(), data=request.POST or None,
                               files=request.FILES or None)
        context.update({'form': form})
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'Hepsiburada hesap bilgileri başarıyla güncellendi!')
                return redirect("hepsiburada_hesap_bilgileri")
    else:
        form = HepsiburadaForm(data=request.POST, files=request.FILES)
        context.update({'form': form})
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'Hepsiburada hesap bilgileri başarıyla eklendi!')
                return redirect("hepsiburada_hesap_bilgileri")

    return render(request, 'backend/adminpage/pages/hepsiburada/hepsiburada.html', context)


def hepsiburadaCategory(category_title):
    hepsiburada_category = None

    hepsiburada = Hepsiburada.objects.all().last()
    api = HepsiburadaApiClient(username=hepsiburada.username, password=hepsiburada.password,
                               mercant_id=hepsiburada.merchantID)
    service = HepsiburadaProductIntegrationService(api)
    max = service.get_categories(page=0)
    max_page = max['totalPages']

    i = 0
    while (i <= max_page):
        response = service.get_categories(page=i)
        for r in response['data']:
            if category_title.lower() == str(r['displayName']).lower():
                hepsiburada_category = r['categoryId']
                break
        i += 1

    return hepsiburada_category


@login_required(login_url="/yonetim/giris-yap/")
def hepsiburada_add_product(request):
    return render(request, 'backend/adminpage/pages/hepsiburada/urun_girisi.html')


@login_required(login_url="/yonetim/giris-yap/")
def hepsiburada_add_product_giyim(request):
    return render(request, 'backend/adminpage/pages/hepsiburada/urun_girisi_giyim.html')


@login_required(login_url="/yonetim/giris-yap/")
def hepsiburada_add_product_giyim_category(request, category_no):
    context = {}
    subcategory = SubCategory.objects.get(category_no=category_no)
    categories = SubBottomCategory.objects.filter(subcategory__category_no=category_no)
    context.update({'categories': categories, 'subcategory': subcategory})
    return render(request, 'backend/adminpage/pages/hepsiburada/urun_girisi_giyim_category.html', context)


def hepsiburadaProductData(categoryId, merchant, merchantSku, VaryantGroupID, barcode, title, detail, brand, price,
                           quantity, image1, image2, image3, image4, image5, color, size):
    data = {
        "categoryId": categoryId,
        "merchant": str(merchant),
        "attributes": {
            "merchantSku": merchantSku,
            "VaryantGroupID": str(VaryantGroupID),
            "Barcode": barcode,
            "UrunAdi": title,
            "UrunAciklamasi": detail,
            "Marka": brand,
            "GarantiSuresi": 0,
            "kg": "1",
            "tax_vat_rate": "10",
            "price": price,
            "stock": str(quantity),
            "Image1": image1,
            "Image2": image2,
            "Image3": image3,
            "Image4": image4,
            "Image5": image5,
            "Video1": "",
            "renk_variant_property": str(color),
            "ebatlar_variant_property": str(size)
        }
    }

    return data


def hepsiburadaUpdateProductData(categoryId, merchant, merchantSku, VaryantGroupID, barcode, title, detail, brand,
                                 price, quantity, image1, image2, image3, image4, image5, color, size):
    data = {
        "categoryId": categoryId,
        "merchant": str(merchant),
        "attributes": {
            "merchantSku": merchantSku,
            "VaryantGroupID": str(VaryantGroupID),
            "Barcode": barcode,
            "UrunAdi": title,
            "UrunAciklamasi": detail,
            "Marka": brand,
            "GarantiSuresi": 0,
            "kg": "1",
            "tax_vat_rate": "10",
            "price": price,
            "stock": str(quantity),
            "Image1": image1,
            "Image2": image2,
            "Image3": image3,
            "Image4": image4,
            "Image5": image5,
            "Video1": "",
            "renk_variant_property": str(color),
            "ebatlar_variant_property": str(size)
        }
    }

    return data


def hepsiburadaUpdateData(barcode, quantity, list_price, sale_price):
    data = {
        "barcode": str(barcode),
        "quantity": int(quantity),
        "listPrice": float(list_price),
        "salePrice": float(sale_price)
    }

    return data


def hepsiburadaDeleteData(products):
    data = []

    for p in products:
        data.append(
            {
                "barcode": str(p.barcode)
            }
        )

    return data


def hepsiburadaCallingProduct(category, title):
    products = ApiProduct.objects.filter(subbottomcategory=category, title__icontains=title, is_publish=True,
                                         is_publish_trendyol=False)
    return products


def hepsiburadaUpdateCallingProduct(category, title):
    products = ApiProduct.objects.filter(subbottomcategory=category, title__icontains=title, is_publish=True,
                                         is_publish_trendyol=True)
    return products


@login_required(login_url="/yonetim/giris-yap/")
def hepsiburada_add_product_giyim_send(request, id):
    context = {}
    hepsiburada = Hepsiburada.objects.all().last()
    category = SubBottomCategory.objects.get(id=id)

    context.update({'category': category, 'log_record': ""})
    product_data = []
    items = []

    hepsiburada_category = None

    if 'sendHepsiburada' in request.POST:

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'integrator.json')
        os.remove(file_path)

        category_title = request.POST.get('category_title')
        product_title = request.POST.get('product_title')

        if category_title == "Triko":
            category_title = "Atlet"

        hepsiburada_category = hepsiburadaCategory(category_title)

        ##Calling Product
        products = hepsiburadaCallingProduct(category, product_title)

        if hepsiburada_category:
            for p in products:
                title = p.title
                detail = p.detail
                if detail == '' or detail == None:
                    detail = title
                images = []
                if p.image_url1:
                    images.append({'url': p.image_url1})
                if p.image_url2:
                    images.append({'url': p.image_url2})
                if p.image_url3:
                    images.append({'url': p.image_url3})
                if p.image_url4:
                    images.append({'url': p.image_url4})
                if p.image_url5:
                    images.append({'url': p.image_url5})

                items.append(hepsiburadaProductData(categoryId=hepsiburada_category, merchant=hepsiburada.merchantID, merchantSku=p.stock_code.upper(), VaryantGroupID=p.model_code, barcode=p.barcode, title=title, detail=detail, brand=p.brand.title, price=float(p.price),
                           quantity=p.quantity, image1=p.image_url1, image2=p.image_url2, image3=p.image_url3, image4=p.image_url4, image5=p.image_url5, color=p.color, size=p.size))

                product_data = items
                p.hepsiburada_category_id = int(hepsiburada_category)
                p.save()

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'integrator.json')
        with open(file_path , 'w', encoding='utf8') as out_file:
            json.dump(product_data, out_file, sort_keys=True, indent=4,
                      ensure_ascii=False)

        files = {"file": ("integrator.json", open(file_path, "rb"), "application/json")}

        headers = {
            "accept": "application/json",
            "authorization": "Basic dHJlZHlzaG9wX2RldjpIYjEyMzQ1IQ=="
        }

        url = "https://mpop-sit.hepsiburada.com/product/api/products/import"

        response = requests.post(url, files=files, headers=headers)

        #api = HepsiburadaApiClient(username=hepsiburada.username, password=hepsiburada.password,
        #                           mercant_id=hepsiburada.merchantID)
        #service = HepsiburadaProductIntegrationService(api)
        #response = service.create_products(files=files)
        print(response.text)

        # messages.success(request, f"{response}")
        # log_record = LogRecords.objects.create(log_type="1", batch_id=str(response['batchRequestId']))
        return redirect('hepsiburada_add_product_giyim_send', id)
    return render(request, 'backend/adminpage/pages/hepsiburada/urun_girisi_giyim_send_hepsiburada.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kesilen_fatura_ekle(request):
    context = {}
    form = IssuedInvoicesAddForm(data=request.POST, files=request.FILES)
    context.update({'form': form})
    if request.method == "POST":
        if form.is_valid():
            data = form.save()
            kdv_tutari = data.price * (data.tax_rate / 100)
            toplam_tutar = kdv_tutari + data.price
            fatura = IssuedInvoices.objects.get(id=data.id)
            fatura.tax_amount = kdv_tutari
            fatura.price_amount = toplam_tutar
            fatura.save()
            messages.success(request, 'Fatura başarıyla eklendi!')
            return redirect("kesilen_fatura_ekle")
    return render(request, 'backend/adminpage/pages/finans_yonetimi/kesilen_fatura_ekle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kesilen_faturalar(request):
    context = {}

    fatura_adi = request.GET.get("fatura_adi", '')
    unvan = request.GET.get("unvan", '')
    vergi_no = request.GET.get("vergi_no", '')
    vergi_dairesi = request.GET.get("vergi_dairesi", '')
    ay = request.GET.get("ay", '')
    yil = request.GET.get("yil", '')
    desc = request.GET.get("desc", '')

    query = f"?fatura_adi={fatura_adi}&unvan={unvan}&vergi_no={vergi_no}&vergi_dairesi={vergi_dairesi}&ay={ay}&yil={yil}&desc={desc}"

    faturalar = IssuedInvoices.objects.all()

    if desc:
        faturalar = faturalar.order_by(desc)

    if fatura_adi:
        faturalar = faturalar.filter(Q(bill_number__icontains=fatura_adi))

    if unvan:
        faturalar = faturalar.filter(Q(name__icontains=unvan))

    if vergi_no:
        faturalar = faturalar.filter(tax_number=vergi_no)

    if vergi_dairesi:
        faturalar = faturalar.filter(Q(tax_administration__icontains=vergi_dairesi))

    if ay:
        faturalar = faturalar.filter(month=ay)

    if yil:
        faturalar = faturalar.filter(year=yil)

    paginator = Paginator(faturalar, 50)
    page = request.GET.get('page')

    try:
        fatura = paginator.page(page)
    except PageNotAnInteger:
        fatura = paginator.page(1)
    except EmptyPage:
        fatura = paginator.page(paginator.num_pages)

    context.update({
        'faturalar': fatura,
        'query': query,
    })
    return render(request, 'backend/adminpage/pages/finans_yonetimi/kesilen_faturalar.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def update_kesilen_fatura(request, id):
    context = {}
    fatura = IssuedInvoices.objects.get(id=id)
    form = IssuedInvoicesUpdateForm(instance=fatura, data=request.POST or None,
                                    files=request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Fatura başarıyla güncellendi!')
            return redirect("update_kesilen_fatura", id)

    context.update({
        'fatura': fatura,
        'form': form
    })
    return render(request, 'backend/adminpage/pages/finans_yonetimi/kesilen_fatura_guncelle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def delete_kesilen_fatura(request, id):
    fatura = IssuedInvoices.objects.get(id=id)
    fatura.delete()
    messages.success(request, 'Fatura başarıyla silindi!')
    return redirect('kesilen_faturalar')


def kesilen_faturalar_export_excel(request):
    columns = ['Ad/Soyad/Ünvan', 'Vergi Numarası', 'Vergi Dairesi', 'Yıl', 'Ay', 'KDV Hariç Tutar (TL)',
               'KDV Oranı', 'Fatura Düzenlenme Tarihi']

    rows = IssuedInvoices.objects.all().values_list('name', 'tax_number', 'tax_administration', 'year', 'month',
                                                    'price', 'tax_rate', 'edited_date')

    return exportExcel('kesilen-faturalar', 'Ödemeler', columns=columns, rows=rows)


@login_required(login_url="/yonetim/giris-yap/")
def alinan_fatura_ekle(request):
    context = {}
    form = InvoicesReceivedAddForm(data=request.POST, files=request.FILES)
    context.update({'form': form})
    if request.method == "POST":
        if form.is_valid():
            data = form.save()
            kdv_tutari = data.price * (data.tax_rate / 100)
            toplam_tutar = kdv_tutari + data.price
            fatura = InvoicesReceived.objects.get(id=data.id)
            fatura.tax_amount = kdv_tutari
            fatura.price_amount = toplam_tutar
            fatura.save()
            messages.success(request, 'Fatura başarıyla eklendi!')
            return redirect("alinan_fatura_ekle")
    return render(request, 'backend/adminpage/pages/finans_yonetimi/alinan_fatura_ekle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def alinan_faturalar(request):
    context = {}
    fatura_adi = request.GET.get("fatura_adi", '')
    ay = request.GET.get("ay", '')
    yil = request.GET.get("yil", '')
    desc = request.GET.get("desc", '')

    query = f"?fatura_adi={fatura_adi}&ay={ay}&yil={yil}&desc={desc}"

    faturalar = InvoicesReceived.objects.all()

    if desc:
        faturalar = faturalar.order_by(desc)

    if fatura_adi:
        faturalar = faturalar.filter(Q(bill_number__icontains=fatura_adi))

    if ay:
        faturalar = faturalar.filter(month=ay)

    if yil:
        faturalar = faturalar.filter(year=yil)

    paginator = Paginator(faturalar, 50)
    page = request.GET.get('page')

    try:
        fatura = paginator.page(page)
    except PageNotAnInteger:
        fatura = paginator.page(1)
    except EmptyPage:
        fatura = paginator.page(paginator.num_pages)

    context.update({
        'faturalar': fatura,
        'query': query,
    })
    return render(request, 'backend/adminpage/pages/finans_yonetimi/alinan_faturalar.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def update_alinan_fatura(request, id):
    context = {}
    fatura = InvoicesReceived.objects.get(id=id)
    form = InvoicesReceivedUpdateForm(instance=fatura, data=request.POST or None,
                                      files=request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Fatura başarıyla güncellendi!')
            return redirect("update_alinan_fatura", id)

    context.update({
        'fatura': fatura,
        'form': form
    })
    return render(request, 'backend/adminpage/pages/finans_yonetimi/alinan_fatura_guncelle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def delete_alinan_fatura(request, id):
    fatura = InvoicesReceived.objects.get(id=id)
    fatura.delete()
    messages.success(request, 'Fatura başarıyla silindi!')
    return redirect('alinan_faturalar')


def alinan_faturalar_export_excel(request):
    columns = ['Yıl', 'Ay', 'KDV Hariç Tutar (TL)',
               'KDV Oranı', 'Oluşturulma Tarihi']

    rows = InvoicesReceived.objects.all().values_list('year', 'month', 'price', 'tax_rate', 'created_at')
    return exportExcel('alinan-faturalar', 'Ödemeler', columns=columns, rows=rows)


@login_required(login_url="/yonetim/giris-yap/")
def harcamalar(request):
    context = {}

    tip = request.GET.get("tip", '')
    status = request.GET.get("status", '')
    harcama_adi = request.GET.get("harcama_adi", '')
    yil = request.GET.get("yil", '')
    ay = request.GET.get("ay", '')

    query = f"?tip={tip}&status={status}&harcama_adi={harcama_adi}&yil={yil}&ay={ay}"

    yapilan_harcamalar = Harcamalar.objects.all()

    total_harcama = 0
    iade_tutari = 0

    if tip:
        if tip == "None" or tip == None:
            yapilan_harcamalar = yapilan_harcamalar
        else:
            yapilan_harcamalar = yapilan_harcamalar.filter(harcama_tipi=tip)

    if status:
        if status == "None" or status == None:
            yapilan_harcamalar = yapilan_harcamalar
        else:
            yapilan_harcamalar = yapilan_harcamalar.filter(durum=status)

    if harcama_adi:
        yapilan_harcamalar = yapilan_harcamalar.filter(Q(harcama_adi__icontains=harcama_adi))

    if yil:
        yapilan_harcamalar = yapilan_harcamalar.filter(created_at__year=yil)

    if ay:
        yapilan_harcamalar = yapilan_harcamalar.filter(created_at__month=ay)

    for h in yapilan_harcamalar.filter(durum="Ödeme Yapıldı"):
        total_harcama += h.harcama_tutari

    for i in yapilan_harcamalar.filter(durum="İade Yapıldı"):
        iade_tutari += i.harcama_tutari

    p = Paginator(yapilan_harcamalar, 20)
    page = request.GET.get('page')
    tum_harcamalar = p.get_page(page)

    harcama_sayisi = yapilan_harcamalar.filter(durum="Ödeme Yapıldı").count()
    iade_sayisi = yapilan_harcamalar.filter(durum="İade Yapıldı").count()

    form = HarcamalarForm(data=request.POST, files=request.FILES)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Harcama başarıyla eklendi!')
            return redirect("harcamalar")

    context.update({
        'harcamalar': tum_harcamalar,
        'harcama_sayisi': harcama_sayisi,
        'form': form,
        'total_harcama': total_harcama,
        'query': query,
        'tip': tip,
        'status': status,
        'harcama_adi': harcama_adi,
        'yil': yil,
        'ay': ay,
        'iade_sayisi': iade_sayisi,
        'iade_tutari': iade_tutari,
    })

    return render(request, 'backend/adminpage/pages/finans_yonetimi/harcamalar.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def harcama_detay(request, id):
    context = {}

    harcama = get_object_or_404(Harcamalar, id=id)
    form = HarcamalarForm(instance=harcama, data=request.POST or None, files=request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Güncelleme başarıyla yapıldı!')
            return redirect('harcama_detay', id)

    context.update({
        'harcama': harcama,
        'form': form,
    })
    return render(request, 'backend/adminpage/pages/finans_yonetimi/harcamalar_guncelle.html', context)


def harcamalar_export_excel(request):
    columns = ['Harcama Tipi', 'Harcama Adı', 'Harcama Tutarı', 'Harcama Tarihi']

    rows = Harcamalar.objects.all().values_list('harcama_tipi', 'harcama_adi', 'harcama_tutari', 'created_at')
    return exportExcel('Harcamalar', 'Harcamalar', columns=columns, rows=rows)


def harcamalar_export_pdf(request):
    columns = ['Harcama Tipi', 'Harcama Adı', 'Harcama Tutarı', 'Harcama Tarihi']
    rows = []
    row = Harcamalar.objects.all().values_list('harcama_tipi', 'harcama_adi', 'harcama_tutari', 'created_at')
    for r in row:
        rows.append(r)

    dict = {
        'columns': columns,
        'rows': rows
    }

    pdf = exportPdf(f"{str(settings.BASE_DIR)}" + "/templates/backend/adminpage/partials/table_pdf.html", dict)
    response = HttpResponse(pdf, content_type='application/pdf')
    content = f'attachment; filename=Harcamalar' + '.pdf'
    response['Content-Disposition'] = content

    return response


@login_required(login_url="/yonetim/giris-yap/")
def harcamalar_hepsini_sil(request):
    context = {}
    harcamalar = Harcamalar.objects.all().delete()
    messages.success(request, 'Tüm harcamalar silindi.')
    return redirect("harcamalar")


@login_required(login_url="/yonetim/giris-yap/")
def harcamalar_secilileri_sil(request):
    harcama_id = request.GET.getlist('harcama[]')

    Harcamalar.objects.filter(id__in=harcama_id).delete()
    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def satislar_api(request):
    bugun = datetime.today().day
    oncekigun = (datetime.today() - timedelta(days=1)).day
    ay = datetime.today().month
    oncekiay = (datetime.today().month - 1)
    yil = datetime.today().year
    oncekiyil = (datetime.today().year - 1)

    daily_order_list = []
    daily_order_total = 0
    onceki_gun_satis = 0
    mountly_order_list = []
    mountly_order_total = 0
    onceki_ay_satis = 0
    yearly_order_list = []
    yearly_order_total = 0
    onceki_yil_satis = 0

    for o in Order.objects.all():
        if o.updated_at.day == bugun:
            daily_order_list.append(o.order_total)
        if o.updated_at.month == ay:
            mountly_order_list.append(o.order_total)
        if o.updated_at.year == yil:
            yearly_order_list.append(o.order_total)

    for o in TrendyolOrders.objects.all().exclude(status="İptal Edildi"):
        if o.order_date.month == ay:
            if (o.order_date + timedelta(hours=1)).day == bugun:
                daily_order_list.append(o.sales_amount)
            if (o.order_date + timedelta(hours=1)).day == oncekigun:
                if o:
                    onceki_gun_satis += o.sales_amount
        if o.order_date.month == ay:
            mountly_order_list.append(o.sales_amount)
        if (o.order_date + timedelta(hours=1)).month == oncekiay:
            if o:
                onceki_ay_satis += o.sales_amount
        if o.order_date.year == yil:
            yearly_order_list.append(o.sales_amount)
        if (o.order_date + timedelta(hours=1)).year == oncekiyil:
            if o:
                onceki_yil_satis += o.sales_amount

    for d in daily_order_list:
        daily_order_total += d

    for m in mountly_order_list:
        mountly_order_total += m

    for y in yearly_order_list:
        yearly_order_total += y

    if onceki_gun_satis == 0:
        gunluk_degisim = ((daily_order_total * 100) / 1) - 100
    else:
        gunluk_degisim = ((daily_order_total * 100) / onceki_gun_satis) - 100

    if onceki_ay_satis == 0:
        aylik_degisim = ((mountly_order_total * 100) / 1) - 100
    else:
        aylik_degisim = ((mountly_order_total * 100) / onceki_ay_satis) - 100

    if onceki_yil_satis == 0:
        yillik_degisim = 0
    else:
        yillik_degisim = ((yearly_order_total * 100) / onceki_yil_satis) - 100

    data = [daily_order_total, mountly_order_total, yearly_order_total, ay, yil, gunluk_degisim, aylik_degisim,
            yillik_degisim]
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def kar_api(request):
    harcamalar = Harcamalar.objects.all()
    kesintiler = 0

    total_cash_list = []
    total_cash = 0
    toplam_harcamalar = 0
    iade_harcamalar = 0
    iade_list = []
    iade_tutari = 0
    komisyon_ucreti = 0

    for o in Order.objects.all():
        total_cash_list.append(o.order_total)

    for o in TrendyolOrders.objects.all().exclude(status="İptal Edildi"):
        total_cash_list.append(o.sales_amount)

    for o in TrendyolOrders.objects.all().exclude(status="İptal Edildi"):
        kargo_ucreti = o.delivery_price
        if o.is_return == True:
            komisyon_ucreti = 0
        else:
            if o.commission_price:
                komisyon_ucreti = o.commission_price
            else:
                komisyon_ucreti = 0

        hizmet_bedeli = o.service_price

        if o.delivery_price is None:
            kargo_ucreti = 0.0

        if o.service_price is None:
            hizmet_bedeli = 0.0

        kesintiler += kargo_ucreti + komisyon_ucreti + hizmet_bedeli

    for tc in total_cash_list:
        total_cash += tc

    for h in harcamalar.filter(durum="Ödeme Yapıldı"):
        toplam_harcamalar += h.harcama_tutari

    for h in harcamalar.filter(durum="İade Yapıldı"):
        iade_harcamalar += h.harcama_tutari

    for o in Order.objects.filter(status="İptal Edildi"):
        iade_list.append(o.order_total)

    for o in TrendyolOrders.objects.filter(is_return=True):
        iade_list.append(o.sales_amount)

    for i in iade_list:
        iade_tutari += i

    toplam_kar = total_cash - toplam_harcamalar - kesintiler - iade_tutari + iade_harcamalar

    data = [toplam_kar, total_cash, toplam_harcamalar, kesintiler, iade_tutari]
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def yedi_gunluk_kar(request):
    yedigunonce = datetime.today() - timedelta(days=6)
    son_yedi_gun = []

    ilgili_gun_satislar_list = []
    ilgili_gun_harcamalar_list = []
    ilgili_gun_iade_harcamalar_list = []
    ilgili_gun_kesintiler_list = []
    ilgili_gun_iadeler_list = []

    while yedigunonce <= datetime.today():
        son_yedi_gun.append(yedigunonce.strftime("%d-%m-%Y"))

        ilgili_gun_satislar = 0
        ilgili_gun_kesintiler = 0
        ilgili_gun_harcamalar = 0
        ilgili_gun_iade_harcamalar = 0
        ilgili_gun_iadeler = 0

        for o in Order.objects.filter(created_at__year=yedigunonce.year, created_at__month=yedigunonce.month,
                                      created_at__day=yedigunonce.day):
            ilgili_gun_satislar += o.order_total

        for o in TrendyolOrders.objects.all().exclude(status="İptal Edildi"):
            if (o.order_date + timedelta(hours=1)).month == yedigunonce.month:
                if (o.order_date + timedelta(hours=1)).day == yedigunonce.day:
                    ilgili_gun_satislar += o.sales_amount

                    kargo_ucreti = o.delivery_price

                    if o.is_return == True:
                        komisyon_ucreti = 0.0
                    else:
                        if o.commission_price:
                            komisyon_ucreti = o.commission_price
                        else:
                            komisyon_ucreti = 0

                    hizmet_bedeli = o.service_price

                    if o.delivery_price is None:
                        kargo_ucreti = 0.0

                    if o.service_price is None:
                        hizmet_bedeli = 0.0

                    ilgili_gun_kesintiler += kargo_ucreti + komisyon_ucreti + hizmet_bedeli

        ilgili_gun_satislar_list.append(ilgili_gun_satislar)
        ilgili_gun_kesintiler_list.append(ilgili_gun_kesintiler)

        for h in Harcamalar.objects.filter(durum="Ödeme Yapıldı", created_at__day=yedigunonce.day,
                                           created_at__month=yedigunonce.month, created_at__year=yedigunonce.year):
            ilgili_gun_harcamalar += h.harcama_tutari

        ilgili_gun_harcamalar_list.append(ilgili_gun_harcamalar)

        for h in Harcamalar.objects.filter(durum="İade Yapıldı", created_at__day=yedigunonce.day,
                                           created_at__month=yedigunonce.month, created_at__year=yedigunonce.year):
            ilgili_gun_iade_harcamalar += h.harcama_tutari

        ilgili_gun_iade_harcamalar_list.append(ilgili_gun_iade_harcamalar)

        for o in Order.objects.filter(status="İptal Edildi", updated_at__day=yedigunonce.day,
                                      updated_at__month=yedigunonce.month, updated_at__year=yedigunonce.year):
            ilgili_gun_iadeler += o.order_total

        for o in TrendyolOrders.objects.filter(is_return=True):
            if o.order_date.month == yedigunonce.month:
                if (o.order_date + timedelta(hours=1)).day == yedigunonce.day:
                    ilgili_gun_iadeler += o.sales_amount

        ilgili_gun_iadeler_list.append(ilgili_gun_iadeler)

        yedigunonce += timedelta(days=1)

    k = 0
    kar_list = []
    while k < 7:
        kar_list.append((ilgili_gun_satislar_list[k] - ilgili_gun_kesintiler_list[k] - ilgili_gun_harcamalar_list[k] -
                         ilgili_gun_iadeler_list[k] + ilgili_gun_iade_harcamalar_list[k]))
        k += 1

    data = [son_yedi_gun, kar_list, ilgili_gun_harcamalar_list, ilgili_gun_kesintiler_list, ilgili_gun_iadeler_list,
            ilgili_gun_satislar_list]
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def en_cok_siparis_gelen_10_sehir(request):
    from collections import Counter
    tum_sehirler_list = []
    alisveris_sayisi_list = []

    for o in TrendyolOrders.objects.all():
        if o.shippment_city != None:
            tum_sehirler_list.append(o.shippment_city)

    for v in Counter(tum_sehirler_list).values():
        alisveris_sayisi_list.append(v)

    sehirler = sorted(Counter(tum_sehirler_list), key=Counter(tum_sehirler_list).get, reverse=True)[:10]
    alısveris_sayisi = sorted(alisveris_sayisi_list, reverse=True)[:10]
    data = [sehirler, alısveris_sayisi]
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def update_history(request):
    context = {}
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    history = UpdateHistory.objects.all()

    p = Paginator(history, 50)
    page = request.GET.get('page')
    histories = p.get_page(page)

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'histories': histories,
    })
    return render(request, 'backend/adminpage/pages/update_history.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def update_history_all_delete(request):
    history = UpdateHistory.objects.all()

    for h in history:
        h.delete()
    messages.success(request, 'Tüm kayıtlar silindi!')
    return redirect('update_history')


@login_required(login_url="/yonetim/giris-yap/")
def update_history_delete(request, id):
    history = UpdateHistory.objects.get(id=id)
    history.delete()
    messages.success(request, 'İlgili kayıt silindi!')
    return redirect('update_history')


@login_required(login_url="/yonetim/giris-yap/")
def ajax_search(request):
    res = None
    series = request.GET.get('series', '')

    products = ApiProduct.objects.filter(title__icontains=series) | ApiProduct.objects.filter(
        barcode__icontains=series) | ApiProduct.objects.filter(
        stock_code__icontains=series) | ApiProduct.objects.filter(model_code__icontains=series)

    if len(products) > 0:
        data = []
        for r in products:
            item = {
                'id': r.id,
                'p_title': r.title,
                'slug': r.slug,
            }
            data.append(item)

        res = data
    else:
        res = "Herhangi bir kayıt bulunamadı!"
    return JsonResponse({'data': res})


@login_required(login_url="/yonetim/giris-yap/")
def pazaryerleri_istatistikler(request):
    tredyshop_siparis_sayisi = Order.objects.all().exclude(status="İptal Edildi").count()
    trendyol_siparis_sayisi = TrendyolOrders.objects.all().exclude(status="İptal Edildi").count()
    hepsiburada_siparis_sayisi = HepsiburadaSiparisler.objects.all().exclude(status="İptal Edildi").count()
    amazon_siparis_sayisi = AmazonSiparisler.objects.all().exclude(status="İptal Edildi").count()

    data = [tredyshop_siparis_sayisi, trendyol_siparis_sayisi, hepsiburada_siparis_sayisi, amazon_siparis_sayisi]

    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def email_pazarlama(request):
    context = {}
    tum_kullanicilar = User.objects.all()

    p = Paginator(tum_kullanicilar, 50)
    page = request.GET.get('page')
    kullanicilar = p.get_page(page)

    context.update({
        'kullanicilar':kullanicilar
    })

    if 'single_send_mail' in request.POST:
        email = request.POST.get('single_email')


    return render(request, 'backend/adminpage/pages/pazarlama_yonetimi/email_pazarlama.html', context)