import json
import os
import calendar
from math import ceil
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone, timedelta
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from blog.models import BlogCategory, BlogKeywords
from carts.helpers import paytr_sorgu
from hepsiburada.api import HepsiburadaApiClient
from hepsiburada.models import HepsiburadaSiparisler, HepsiburadaMoreProductOrder
from hepsiburada.services import HepsiburadaProductIntegrationService
from trendyol.api import TrendyolApiClient
from amazon.models import AmazonSiparisler
from trendyol.models import LogRecords, TrendyolMoreProductOrder
from trendyol.services import ProductIntegrationService, OrderIntegrationService
from adminpage.custom import *
from adminpage.forms import *
from categorymodel.models import SubCategory, SubBottomCategory, MainCategory
from customer.models import CustomerAddress, Coupon
from ecommerce import settings
from orders.models import Order, ExtraditionRequest, OrderProduct, CancellationRequest
from product.models import Color, Product, ReviewRating, Favorite, FabricType, Height, Pattern, \
    ArmType, CollerType, WeavingType, MaterialType, HeelType, HeelSize, Pocket
from product.read_xml import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
import requests
from user_accounts.models import User
from product.update import *
from PIL import Image
from io import BytesIO
from django.core.files.images import ImageFile
from django.views.generic.edit import (CreateView, UpdateView)


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

    return render(request, 'backend/yonetim/sayfalar/hesap_yonetimi/giris_yap.html')


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
    return render(request, 'backend/yonetim/sayfalar/hesap_yonetimi/hesap_bilgileri.html')


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
    return render(request, 'backend/yonetim/sayfalar/hesap_yonetimi/sifre_degistirme.html')


@login_required(login_url="/yonetim/giris-yap/")
def mainpage(request):
    context = {}
    bu_yil = datetime.today().year
    bu_ay = datetime.today().month
    ay = ''

    if bu_ay == 1:
        ay = "Ocak"
    elif bu_ay == 2:
        ay = "Şubat"
    elif bu_ay == 3:
        ay = "Mart"
    elif bu_ay == 4:
        ay = "Nisan"
    elif bu_ay == 5:
        ay = "Mayıs"
    elif bu_ay == 6:
        ay = "Haziran"
    elif bu_ay == 7:
        ay = "Temmuz"
    elif bu_ay == 8:
        ay = "Ağustos"
    elif bu_ay == 9:
        ay = "Eylül"
    elif bu_ay == 10:
        ay = "Ekim"
    elif bu_ay == 11:
        ay = "Kasım"
    else:
        ay = "Aralık"

    yeni_siparis_sayisi = 0
    kargolanmis_siparis_sayisi = 0
    tamamlanmis_siparis_sayisi = 0
    toplam_siparis_sayisi = Order.objects.filter(created_at__year=bu_yil).exclude(
        status="İptal Edildi").count() + TrendyolOrders.objects.filter(order_date__year=bu_yil).exclude(
        status="İptal Edildi").count() + HepsiburadaSiparisler.objects.filter(order_date__year=bu_yil).exclude(
        status="İptal Edildi").count()
    tredyshop_satis_sayisi = 0
    pazaryeri_satis_sayisi = 0
    ilgili_ay_satis_sayisi = 0

    son_on_tredyshop_siparisi = []
    son_on_trendyol_siparisi = []
    son_on_hepsiburada_siparisi = []

    top_five_products = []
    for p in ProductSellStatistic.objects.all().order_by('-sell_count')[:5]:
        try:
            Product.objects.get(barcode=p.barcode)
            top_five_products.append({
                'image': Product.objects.get(barcode=p.barcode).image_url1,
                'title': p.name,
                'satis': p.satis,
                'maliyet': p.maliyet,
                'satis_sayisi': p.sell_count,
                'satisOrani': p.satisOrani,
                'maliyetOrani': p.maliyetOrani,
            })
        except:
            top_five_products.append({
                'image': '',
                'title': p.name,
                'satis': p.satis,
                'maliyet': p.maliyet,
                'satis_sayisi': p.sell_count,
                'satisOrani': p.satisOrani,
                'maliyetOrani': p.maliyetOrani,
            })

    for t in Order.objects.filter(created_at__year=bu_yil):
        if t.created_at.month == bu_ay and t.status != "İptal Edildi":
            tredyshop_satis_sayisi += 1
        if t.status == "Yeni" and t.created_at.month == bu_ay:
            yeni_siparis_sayisi += 1
        if t.status == "Kargolandı" and t.created_at.month == bu_ay:
            kargolanmis_siparis_sayisi += 1
        if t.status == "Tamamlandı" and t.created_at.month == bu_ay:
            tamamlanmis_siparis_sayisi += 1

    for t in TrendyolOrders.objects.filter(order_date__year=bu_yil):
        if t.order_date.month == bu_ay and t.status != "İptal Edildi":
            pazaryeri_satis_sayisi += 1
        if t.status == "Yeni" and t.order_date.month == bu_ay:
            yeni_siparis_sayisi += 1
        if t.status == "Kargolandı" and t.order_date.month == bu_ay:
            kargolanmis_siparis_sayisi += 1
        if t.status == "Tamamlandı" and t.order_date.month == bu_ay:
            tamamlanmis_siparis_sayisi += 1

    for t in HepsiburadaSiparisler.objects.filter(order_date__year=bu_yil):
        if t.order_date.month == bu_ay and t.status != "İptal Edildi":
            pazaryeri_satis_sayisi += 1
        if t.status == "Yeni" and t.order_date.month == bu_ay:
            yeni_siparis_sayisi += 1
        if t.status == "Kargolandı" and t.order_date.month == bu_ay:
            kargolanmis_siparis_sayisi += 1
        if t.status == "Tamamlandı" and t.order_date.month == bu_ay:
            tamamlanmis_siparis_sayisi += 1

    ilgili_ay_satis_sayisi = tredyshop_satis_sayisi + pazaryeri_satis_sayisi

    for o in Order.objects.all().order_by('-created_at')[:10]:
        son_on_tredyshop_siparisi.append(
            {
                'id': o.id,
                'siparis_no': o.order_number,
                'müsteri': o.user,
                'durum': o.status,
                'siparis_tarihi': o.created_at,
                'platform': "tredyshop",
            }
        )

    for t in TrendyolOrders.objects.all().order_by('-order_date')[:10]:
        son_on_tredyshop_siparisi.append(
            {
                'id': t.id,
                'siparis_no': t.order_number,
                'müsteri': t.buyer,
                'durum': t.status,
                'siparis_tarihi': t.order_date,
                'platform': "trendyol",
            }
        )

    for t in HepsiburadaSiparisler.objects.all().order_by('-order_date')[:10]:
        son_on_hepsiburada_siparisi.append(
            {
                'id': t.id,
                'siparis_no': t.order_number,
                'müsteri': t.buyer,
                'durum': t.status,
                'siparis_tarihi': t.order_date,
                'platform': "hepsiburada",
            }
        )

    son_siparisler = son_on_tredyshop_siparisi + son_on_trendyol_siparisi + son_on_hepsiburada_siparisi
    son_siparisler.sort(key=lambda x: x['siparis_tarihi'], reverse=True)

    cevaplanmamis_soru = Question.objects.filter(answer__isnull=True).count()
    sorular = Question.objects.filter(answer__isnull=True)
    if sorular.count() > 3:
        sorular = sorular[:3]

    takvim = calendar.month(bu_yil, bu_ay)

    tasks = Task.objects.filter(usertask__user=request.user)

    context.update({
        'bu_yil': bu_yil,
        'ay': ay,
        'yeni_siparis_sayisi': yeni_siparis_sayisi,
        'kargolanmis_siparis_sayisi': kargolanmis_siparis_sayisi,
        'tamamlanmis_siparis_sayisi': tamamlanmis_siparis_sayisi,
        'toplam_siparis_sayisi': toplam_siparis_sayisi,
        'tredyshop_satis_sayisi': tredyshop_satis_sayisi,
        'pazaryeri_satis_sayisi': pazaryeri_satis_sayisi,
        'ilgili_ay_satis_sayisi': ilgili_ay_satis_sayisi,
        'top_five_products': top_five_products,
        'son_siparisler': son_siparisler,
        'cevaplanmamis_soru': cevaplanmamis_soru,
        'sorular': sorular,
        'takvim': takvim,
        'tasks': tasks,
    })
    return render(request, 'backend/yonetim/sayfalar/anasayfa.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def siparis_istatistikleri(request):
    ay = int(request.GET.get("ay"), 0)
    bu_yil = datetime.today().year
    yeni_siparis_sayisi = 0
    kargolanmis_siparis_sayisi = 0
    tamamlanmis_siparis_sayisi = 0

    for t in Order.objects.filter(status="Yeni"):
        if t.created_at.year == bu_yil and t.created_at.month == ay:
            yeni_siparis_sayisi += 1

    for t in TrendyolOrders.objects.filter(status="Yeni"):
        if t.order_date.year == bu_yil and t.order_date.month == ay:
            yeni_siparis_sayisi += 1

    for t in HepsiburadaSiparisler.objects.filter(status="Yeni"):
        if t.order_date.year == bu_yil and t.order_date.month == ay:
            yeni_siparis_sayisi += 1
    for t in Order.objects.filter(status="Kargolandı"):
        if t.created_at.year == bu_yil and t.created_at.month == ay:
            kargolanmis_siparis_sayisi += 1

    for t in TrendyolOrders.objects.filter(status="Kargolandı"):
        if t.order_date.year == bu_yil and t.order_date.month == ay:
            kargolanmis_siparis_sayisi += 1

    for t in HepsiburadaSiparisler.objects.filter(status="Kargolandı"):
        if t.order_date.year == bu_yil and t.order_date.month == ay:
            kargolanmis_siparis_sayisi += 1

    for t in Order.objects.filter(status="Tamamlandı"):
        if t.created_at.year == bu_yil and t.created_at.month == ay:
            tamamlanmis_siparis_sayisi += 1

    for t in TrendyolOrders.objects.filter(status="Tamamlandı"):
        if t.order_date.year == bu_yil and t.order_date.month == ay:
            tamamlanmis_siparis_sayisi += 1

    for t in HepsiburadaSiparisler.objects.filter(status="Tamamlandı"):
        if t.order_date.year == bu_yil and t.order_date.month == ay:
            tamamlanmis_siparis_sayisi += 1

    data = [yeni_siparis_sayisi, kargolanmis_siparis_sayisi, tamamlanmis_siparis_sayisi]
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def platform_istatistikleri(request):
    ay = int(request.GET.get("ay"), 0)
    bu_yil = datetime.today().year
    tredyshop_satis_sayisi = 0
    pazaryeri_satis_sayisi = 0
    ilgili_ay_satis_sayisi = 0

    for t in Order.objects.all().exclude(status="İptal Edildi"):
        if t.created_at.year == bu_yil and t.created_at.month == ay:
            tredyshop_satis_sayisi += 1

    for t in TrendyolOrders.objects.all().exclude(status="İptal Edildi"):
        if t.order_date.year == bu_yil and t.order_date.month == ay:
            pazaryeri_satis_sayisi += 1

    for t in HepsiburadaSiparisler.objects.all().exclude(status="İptal Edildi"):
        if t.order_date.year == bu_yil and t.order_date.month == ay:
            pazaryeri_satis_sayisi += 1

    ilgili_ay_satis_sayisi = tredyshop_satis_sayisi + pazaryeri_satis_sayisi

    data = [ilgili_ay_satis_sayisi, tredyshop_satis_sayisi, pazaryeri_satis_sayisi]
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def fatura_istatistikleri(request):
    kesilen_faturalar = IssuedInvoices.objects.all()
    kesilen_faturalar_toplam = 0
    for fatura in kesilen_faturalar:
        if fatura.price_amount:
            kesilen_faturalar_toplam += fatura.price_amount

    alinan_faturalar = InvoicesReceived.objects.all()
    alinan_faturalar_toplam = 0
    for fatura in alinan_faturalar:
        if fatura.price_amount:
            alinan_faturalar_toplam += fatura.price_amount

    data = [kesilen_faturalar_toplam, alinan_faturalar_toplam]
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def kullanicilar(request):
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
        return redirect('kullanicilar')

    context.update({
        'users': kullanici,
        'query': query,
    })

    return render(request, 'backend/yonetim/sayfalar/kullanici_yonetimi/kullanicilar.html', context)


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
    return render(request, 'backend/yonetim/sayfalar/kullanici_yonetimi/kullanici_goruntule.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kullanici_sil(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, 'Kullanıcı silindi.')
    return redirect('kullanicilar')


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

    return render(request, 'backend/yonetim/sayfalar/kullanici_yonetimi/kullanici_izinleri.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def gorevler(request):
    context = {}
    task = None
    if request.user.is_superuser == True:
        task = Task.objects.all()
    else:
        task = Task.objects.filter(usertask__user=request.user)
    users = User.objects.filter(is_customer=False)
    p = Paginator(task, 20)
    page = request.GET.get('page')
    tasks = p.get_page(page)
    context.update({
        'tasks': tasks,
        'task': task,
        'users': users,
    })
    return render(request, 'backend/yonetim/sayfalar/kullanici_yonetimi/gorevler.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def gorev_ekle(request):
    task_name = request.POST.get("task_name")
    tasktime = request.POST.get("tasktime")
    task_date = request.POST.get("task_date")
    print(task_date)
    data = "error"
    if task_name and tasktime:
        if tasktime == "Belirli Gün" or tasktime == "Son Gün":
            if task_date:
                Task.objects.create(name=task_name, task_time=tasktime, task_date=task_date)
                data = "success"
            else:
                data = "error"
        else:
            Task.objects.create(name=task_name, task_time=tasktime)
            data = "success"

    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def kullanici_gorevlendir(request):
    task_id = request.POST.get("task_id")
    user_id = request.POST.get("user_id")
    data = "error"
    if task_id and user_id:
        task = get_object_or_404(Task, id=task_id)
        user = get_object_or_404(User, id=user_id)

        if UserTask.objects.filter(task=task, user=user):
            data = "existing"
        else:
            UserTask.objects.create(user=user, task=task)
            Notification.objects.create(user=user, noti_type="9", task_id=task_id, title="Yeni görev ataması yapıldı.")
            data = "success"
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def gorev_detay(request, id):
    context = {}
    task = get_object_or_404(Task, id=id)
    form = TaskDetailForm(instance=task, data=request.POST or None, files=request.FILES or None)
    try:
        notitfy = Notification.objects.get(user=request.user, task_id=id)
        notitfy.is_read = True
        notitfy.save()
    except:
        pass

    if 'saveBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Görev güncellemesi başarıyla yapıldı.')
            return redirect('gorev_detay', id)

    context.update({
        'task': task,
        'form': form,
    })
    return render(request, 'backend/yonetim/sayfalar/kullanici_yonetimi/gorev_detay.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def gorev_sil(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    messages.info(request, 'Görev başarıyla silidi.')
    return redirect("gorevler")


@login_required(login_url="/yonetim/giris-yap/")
def gorev_yapilma_durumu(request):
    task_id = request.GET.get("task_id")
    durum = request.GET.get("durum")
    task = get_object_or_404(Task, id=task_id)
    if durum == "true":
        task.is_completed = True
        task.save()
        user_task = UserTask.objects.get(user=request.user, task=task)
        user_task.all_completed = True
        user_task.save()
    else:
        task.is_completed = False
        task.save()
        user_task = UserTask.objects.get(user=request.user, task=task)
        user_task.all_completed = False
        user_task.save()
    data = "success"
    return JsonResponse(data=data, safe=False)


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

    context.update({
        'form': form,
    })

    aboutus = Hakkimizda.objects.all()
    if aboutus.count() > 0:
        form = AboutUsForm(instance=aboutus.last(), data=request.POST or None, files=request.FILES or None)
        context.update({'form': form})

    categories_count = MainCategory.objects.all().count()
    product_count = Product.objects.all().count()

    if 'addBtn' in request.POST:
        if form.is_valid():
            data = form.save(commit=False)
            data.category_count = categories_count
            data.product_count = product_count
            data.save()
            messages.info(request, 'Hakkımızda sayfası bilgiler güncellendi.')
            return redirect("admin_aboutus")

    return render(request, 'backend/yonetim/sayfalar/site_yonetimi/hakkimizda.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def site_ayarlari(request):
    context = {}
    form = SiteSettingsForm(data=request.POST or None, files=request.FILES or None)

    context.update({
        'form': form,

    })

    site_ayari = SiteSetting.objects.all()
    if site_ayari.count() > 0:
        form = SiteSettingsForm(instance=site_ayari.last(), data=request.POST or None, files=request.FILES or None)
        context.update({'form': form})

    if 'addBtn' in request.POST:
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            messages.info(request, 'Site ayarları bilgiler güncellendi.')
            return redirect("site_ayarlari")

    return render(request, 'backend/yonetim/sayfalar/site_yonetimi/genel_bilgiler.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def page_mainpage(request):
    context = {}

    all_banners = Banner.objects.all()
    all_category = FrontentHeaderCategory.objects.all()
    status = request.GET.get("status", '')
    query = f"?status={status}"

    if status:
        if status == "None" or status == None:
            all_banners = all_banners
            all_category = all_category
        else:
            if status == "Yayında":
                all_banners = all_banners.filter(is_publish=True)
                all_category = all_category.filter(is_publish=True)
            else:
                all_banners = all_banners.filter(is_publish=False)
                all_category = all_category.filter(is_publish=False)

    p = Paginator(all_banners, 50)
    page = request.GET.get('page')
    banners = p.get_page(page)

    p2 = Paginator(all_category, 50)
    page = request.GET.get('page')
    categories = p2.get_page(page)

    context.update({
        'banners': banners,
        'query': query,
        'categories': categories,
    })

    if 'addBtn' in request.POST:
        banner_type = request.POST.get('banner_type')
        banner_title = request.POST.get('bannerTitle')
        image = request.FILES['image']
        max_price = request.POST.get('maxPrice')
        discountrate = request.POST.get('discountRate')
        category_id = request.POST.get('selectCategory')
        banner_url = request.POST.get('banner_url')
        is_publish = request.POST.get('isPublish')

        category = None

        if is_publish == 'on':
            is_publish = True
        else:
            is_publish = False

        if category_id:
            category = get_object_or_404(SubBottomCategory, id=category_id)

        Banner.objects.create(banner_type=banner_type, banner_title=banner_title, banner_maxprice=max_price,
                              image=image, banner_discountrate=discountrate, banner_category=category,
                              is_publish=is_publish, url=banner_url)

        messages.success(request, 'Banner eklendi!')
        return redirect('page_mainpage')

    if 'categoryAddBtn' in request.POST:
        cat_title = request.POST.get('cat_title')
        cat_url = request.POST.get('cat_url')
        is_publish = request.POST.get('cat_status')
        cat_order = request.POST.get('cat_order')

        category = None

        if is_publish == 'on':
            is_publish = True
        else:
            is_publish = False

        FrontentHeaderCategory.objects.create(title=cat_title, url=cat_url, is_publish=is_publish, order=cat_order)

        messages.success(request, 'Banner eklendi!')
        return redirect('page_mainpage')

    return render(request, 'backend/yonetim/sayfalar/site_yonetimi/mainpage.html', context)


def banner_plus_view(request, id):
    banner = get_object_or_404(Banner, id=id)
    banner.viewd_count += 1
    banner.save()
    return JsonResponse(data='success', safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def banner_order(request, id):
    order = request.GET.get('order')
    banner = get_object_or_404(Banner, id=id)
    banner.order = order
    banner.save()
    return JsonResponse(data='success', safe=False)


def banner_publish(request, id):
    banner = get_object_or_404(Banner, id=id)

    if banner.is_publish == True:
        banner.is_publish = False
    else:
        banner.is_publish = True
    banner.save()
    messages.success(request, 'Yayın durumu güncellendi!')
    return redirect('page_mainpage')


def banner_export_excel(request):
    columns = ['Banner Tipi', 'Banner Adı', 'Yayında mı', 'Gösterim Sayısı', 'Oluşturulma Tarihi']

    rows = Banner.objects.all().values_list('banner_type', 'banner_title', 'is_publish', 'viewd_count', 'created_at')
    return exportExcel('Harcamalar', 'Harcamalar', columns=columns, rows=rows)


@login_required(login_url="/yonetim/giris-yap/")
def banner_hepsini_sil(request):
    context = {}
    banner = Banner.objects.all().delete()
    messages.success(request, 'Tüm harcamalar silindi.')
    return redirect("page_mainpage")


@login_required(login_url="/yonetim/giris-yap/")
def banner_secilileri_sil(request):
    banner_id = request.GET.getlist('banner[]')

    Banner.objects.filter(id__in=banner_id).delete()
    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def banner_url(request, id):
    url = request.GET.get('banner_url')
    banner = get_object_or_404(Banner, id=id)
    banner.url = url
    banner.save()
    return JsonResponse(data='success', safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def headercat_order(request, id):
    order = request.GET.get('cat_ajax_order')
    cat = get_object_or_404(FrontentHeaderCategory, id=id)
    cat.order = order
    cat.save()
    return JsonResponse(data='success', safe=False)


def headercat_publish(request, id):
    cat = get_object_or_404(FrontentHeaderCategory, id=id)

    if cat.is_publish == True:
        cat.is_publish = False
    else:
        cat.is_publish = True
    cat.save()
    messages.success(request, 'Yayın durumu güncellendi!')
    return redirect('page_mainpage')


@login_required(login_url="/yonetim/giris-yap/")
def headercat_hepsini_sil(request):
    context = {}
    cat = FrontentHeaderCategory.objects.all().delete()
    messages.success(request, 'Tüm frontend header kategorileri silindi.')
    return redirect("page_mainpage")


@login_required(login_url="/yonetim/giris-yap/")
def headercat_secilileri_sil(request):
    cat_id = request.GET.getlist('catID[]')

    FrontentHeaderCategory.objects.filter(id__in=cat_id).delete()
    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def cat_url(request, id):
    url = request.GET.get('cat_url')
    cat = get_object_or_404(FrontentHeaderCategory, id=id)
    cat.url = url
    cat.save()
    return JsonResponse(data='success', safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def musteri_sorulari(request):
    context = {}
    sorular = Question.objects.all()
    context.update({
        'sorular': sorular,
    })
    return render(request, 'backend/yonetim/sayfalar/site_yonetimi/musteri_sorulari.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def musteri_sorulari_cevapla(request, id):
    context = {}
    sorular = Question.objects.all()
    ilgili_soru = Question.objects.get(id=id)

    if 'answerBtn' in request.POST:
        answer = request.POST.get('answer')
        ilgili_soru.answer = answer
        ilgili_soru.save()
        notification = Notification.objects.get(question=ilgili_soru)
        notification.is_read = True
        notification.save()
        messages.success(request, 'Soru başarıyla cevaplandı.')
        return redirect('musteri_sorulari_cevapla', id)

    context.update({
        'sorular': sorular,
        'ilgili_soru': ilgili_soru,
    })
    return render(request, 'backend/yonetim/sayfalar/site_yonetimi/muster_sorusu_cevaplama.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye1(request):
    context = {}
    category = MainCategory.objects.all()

    kategori_adi = request.GET.get('kategori_adi', '')
    if kategori_adi:
        category = category.filter(title__icontains=kategori_adi)

    query = f"?kategori_adi={kategori_adi}"

    subcategory = SubCategory.objects.all()
    form = MainCategoryForm(data=request.POST or None, files=request.FILES or None)
    context.update({
        'category': category,
        'form': form,
        'subcategory': subcategory,
        'query': query,
    })

    if 'addBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori eklendi.')
            return redirect("kategoriler_seviye1")

    return render(request, 'backend/yonetim/sayfalar/kategori_yonetimi/kategoriler_seviye_1.html', context)


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

    return render(request, 'backend/yonetim/sayfalar/kategori_yonetimi/kategoriler_seviye_1_guncelle.html', context)


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
            return redirect("kategoriler_seviye2", slug)

    return render(request, 'backend/yonetim/sayfalar/kategori_yonetimi/kategoriler_seviye_2.html', context)


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

    return render(request, 'backend/yonetim/sayfalar/kategori_yonetimi/kategoriler_seviye_2_guncelle.html', context)


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
        'main_slug': main_slug,
        'sub_slug': sub_slug,
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

    return render(request, 'backend/yonetim/sayfalar/kategori_yonetimi/kategoriler_seviye_3.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kategoriler_seviye3_guncelle(request, main_slug, sub_slug, id):
    context = {}
    category = SubBottomCategory.objects.get(id=id)
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

    return render(request, 'backend/yonetim/sayfalar/kategori_yonetimi/kategoriler_seviye_3_guncelle.html', context)


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
    selected_kategori = None
    baslik = request.GET.get("baslik", '')
    barkod = request.GET.get("barkod", '')
    modelKodu = request.GET.get("modelKodu", '')
    stokKodu = request.GET.get("stokKodu", '')
    kategori = request.GET.get("kategori", '')
    dropshipping = request.GET.get("dropshipping", '')
    publish = request.GET.get("publish", '')
    stock = request.GET.get("stock", '')
    desc = request.GET.get('desc', '?')

    query = f"?baslik={baslik}&barkod={barkod}&modelKodu={modelKodu}&stokKodu={stokKodu}&kategori={kategori}&dropshipping={dropshipping}&publish={publish}&stock={stock}&desc={desc}"

    product = ProductVariant.objects.all()

    if desc != '':
        product = product.order_by(desc)

    if baslik != '':
        product = product.objects.filter(Q(title__icontains=baslik))

    if barkod != '':
        product = product.filter(Q(barcode__icontains=barkod))

    if modelKodu != '':
        product = product.filter(Q(model_code__icontains=modelKodu))

    if stokKodu != '':
        product = product.filter(Q(stock_code__icontains=stokKodu))

    if kategori != '':
        selected_kategori = int(kategori)
        if kategori == "None":
            product = product.filter(product__subbottomcategory__isnull=True)
        else:
            product = product.filter(product__subbottomcategory_id=kategori)

    if dropshipping != '':
        product = product.filter(Q(product__dropshipping__icontains=dropshipping))

    if publish != '':
        product = product.filter(is_publish=publish)

    if stock != '':
        if stock == "True":
            product = product.filter(quantity__gte=1)
        else:
            product = product.filter(quantity=0)


    paginator = Paginator(product, 20)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    categories = SubBottomCategory.objects.all()

    product_count = product.count()

    upload_trendyol_count = ProductVariant.objects.filter(is_publish_trendyol=True).count()
    active_product_count = product.filter(is_publish=True).count()
    not_active_product_count = ProductVariant.objects.filter(is_publish=False).count()
    insufficient_count = product.filter(quantity=0).count()

    context.update({
        'products': products,
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'product_count': product_count,
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
        'kategori': selected_kategori,
        'dropshipping': dropshipping,
        'publish': publish,
        'stock': stock,
        'desc': desc,
    })

    return render(request, 'backend/yonetim/sayfalar/urun_yonetimi/tum_urunler.html', context)


def clean_filters(filters):
    filters = {k: v for k, v in filters.items() if v}
    return filters


@login_required(login_url="/yonetim/giris-yap/")
def product_detail(request, barkod):
    context = {}

    try:
        product = Product.objects.get(productvariant=ProductVariant.objects.get(barcode=barkod))
    except:
        product = Product.objects.get(barcode=barkod)

    try:
        form = ProductForm(instance=product, data=request.POST or None, files=request.FILES or None)
    except:
        form = ErrorProductForm(instance=product, data=request.POST or None, files=request.FILES or None)
    variants = ProductVariant.objects.filter(model_code=product.model_code)

    sizes = Size.objects.all()
    colors = Color.objects.all()

    context.update({
        'product': product,
        'form': form,
        'variants': variants,
        'sizes': sizes,
        'colors': colors,
    })

    if 'updateBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Ürün güncellendi.')
            return redirect('product_detail', barkod)
    if 'updateAndCloseBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Ürün güncellendi.')
            return redirect('admin_product')

    if 'variantUpdateBtn' in request.POST:
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
        return redirect('product_detail', barkod)
    return render(request, 'backend/yonetim/sayfalar/urun_yonetimi/urun_detay.html', context)

def urun_sil(request,barcode):
    product = get_object_or_404(ProductVariant, barcode=barcode)
    product_title = product.title
    product.delete()
    messages.info(request, f'{product_title} ürünü silindi.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def urun_trendyol_yayina_al_kaldir(request, barcode):
    product = ProductVariant.objects.get(barcode=barcode)
    if product.is_publish_trendyol == True:
        product.is_publish_trendyol = False
        product.save()
    else:
        product.is_publish_trendyol = True
        product.save()
    messages.success(request, f'{product.title} Trendyol yayın durumu güncellendi.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def urun_varyant_islemleri(request, barcode):
    size = request.GET.get('size')
    color = request.GET.get('color')

    sizes = Size.objects.get(id=size)
    colors = Color.objects.get(id=color)

    product = ProductVariant.objects.get(barcode=barcode)
    product.size = sizes
    product.color = colors
    product.save()

    data = 'success'

    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def urun_islemleri(request):
    context = {}

    if 'pasif-urunleri-kaldir-btn' in request.POST:
        urunler = Product.objects.filter(is_publish=False)
        for urun in urunler:

            try:
                ProductVariant.objects.get(product__barcode=urun.barcode).delete()
            except:
                pass
            urun.delete()
        messages.success(request, 'Pasif ürünler kaldırıldı!')
        return redirect('urun_islemleri')

    return render(request, 'backend/yonetim/sayfalar/urun_yonetimi/urun_islemleri.html', context)


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
    if 'yas_grubu' in request.POST:
        yas_grubu()
        messages.success(request, 'Yaş grubu bilgisi güncellendi.')
        return redirect('urun_ozellik_guncelleme')
    if 'beden' in request.POST:
        beden()
        messages.success(request, 'Beden bilgisi güncellendi.')
        return redirect('urun_ozellik_guncelleme')
    return render(request, 'backend/yonetim/sayfalar/urun_yonetimi/ozellik_guncelleme.html', context)


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

    return render(request, 'backend/yonetim/sayfalar/urun_yonetimi/beden_tablosu.html', context)


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
    products = Product.objects.all().delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/yonetim/giris-yap/")
def ajax_select_delete_product(request):
    product_id = request.GET.getlist('product[]')

    Product.objects.filter(id__in=product_id).delete()

    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def not_active_product_delete(request):
    product = Product.objects.filter(is_publish=False)
    for p in product:
        if ProductVariant.objects.filter(modae_code=p.model_code):
            ProductVariant.objects.get(model_code=p.model_code).delete()

        p.delete()
    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def kategori_degistir(request):
    context = {}
    urunler = Product.objects.all().order_by("-create_at")

    kategori = request.GET.get('kategori', '')
    barkod = request.GET.get('barkod', '')
    yayin_durumu = request.GET.get('yayin_durumu', '')
    keyword = request.GET.get('keyword', '')

    if kategori:
        kategori = int(kategori)
        urunler = urunler.filter(subbottomcategory_id=kategori)

    if barkod:
        urunler = urunler.filter(barcode=barkod)

    if keyword:
        urunler = urunler.filter(Q(title__icontains=keyword))

    if yayin_durumu:
        if yayin_durumu == "True":
            urunler = urunler.filter(is_publish=True)
        else:
            urunler = urunler.filter(is_publish=False)

    if kategori and yayin_durumu:
        if yayin_durumu == "True":
            urunler = urunler.filter(is_publish=True, subbottomcategory_id=kategori)
        else:
            urunler = urunler.filter(is_publish=False, subbottomcategory_id=kategori)

    if kategori and yayin_durumu:
        if yayin_durumu == "True":
            urunler = urunler.filter(is_publish=True, subbottomcategory_id=kategori)
        else:
            urunler = urunler.filter(is_publish=False, subbottomcategory_id=kategori)

    if barkod and yayin_durumu:
        if yayin_durumu == "True":
            urunler = urunler.filter(is_publish=True, barcode=barkod)
        else:
            urunler = urunler.filter(is_publish=False, barcode=barkod)

    if barkod and kategori:
        urunler = urunler.filter(barcode=barkod, subbottomcategory_id=kategori)

    if keyword and kategori:
        urunler = urunler.filter(Q(title__icontains=keyword), subbottomcategory_id=kategori)

    query = f"?kategori={kategori}&barkod={barkod}&yayin_durumu={yayin_durumu}&keyword={keyword}"

    seviye_1 = MainCategory.objects.all()
    seviye_2 = SubCategory.objects.all()
    seviye_3 = SubBottomCategory.objects.all()

    paginator = Paginator(urunler, 50)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context.update({
        'products': products,
        'seviye_1': seviye_1,
        'seviye_2': seviye_2,
        'seviye_3': seviye_3,
        'query': query,
        'kategori': kategori,
        'barkod': barkod,
        'yayin_durumu': yayin_durumu,
        'keyword': keyword,
    })

    return render(request, "backend/yonetim/sayfalar/urun_yonetimi/kategori_degistir.html", context)


@login_required(login_url="/yonetim/giris-yap/")
def kategori_hatasi_bulunan_urunler(request):
    context = {}
    urunler = []
    birinci_kategorisi_hatali_urunler = Product.objects.filter(category__isnull=True)
    ikinci_kategorisi_hatali_urunler = Product.objects.filter(subcategory__isnull=True)
    ucuncu_kategorisi_hatali_urunler = Product.objects.filter(subbottomcategory__isnull=True)

    seviye_1 = MainCategory.objects.all()
    seviye_2 = SubCategory.objects.all()
    seviye_3 = SubBottomCategory.objects.all()

    for k in birinci_kategorisi_hatali_urunler:
        urunler.append(k)

    for k in ikinci_kategorisi_hatali_urunler:
        urunler.append(k)

    for k in ucuncu_kategorisi_hatali_urunler:
        urunler.append(k)

    paginator = Paginator(urunler, 30)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context.update({
        'products': products,
        'seviye_1': seviye_1,
        'seviye_2': seviye_2,
        'seviye_3': seviye_3
    })

    return render(request, "backend/yonetim/sayfalar/urun_yonetimi/kategorisi_hatali_urunler.html", context)


@login_required(login_url="/yonetim/giris-yap/")
def kategori_guncelle(request):
    product_id = request.GET.get('productID')
    kategori3 = request.GET.get("kategori3")

    product = get_object_or_404(Product, id=product_id)
    subbottomcategory = get_object_or_404(SubBottomCategory, id=kategori3)
    product.category = subbottomcategory.maincategory
    product.subcategory = subbottomcategory.subcategory
    product.subbottomcategory = subbottomcategory

    product.save()

    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def product_export_excel(request):
    data = 'success'
    columns = ['Başlık', 'Kategori', 'Barkod', 'Model Kodu', 'Stok Kodu', 'Stok', 'Beden', 'Renk', 'Fiyat',
               'İndirimli Fiyat', 'Yayında mı?']
    rows = Product.objects.all().values_list('title', 'subbottomcategory__title',
                                             'barcode',
                                             'model_code',
                                             'stock_code',
                                             'quantity',
                                             'size__name',
                                             'color__name',
                                             'price',
                                             'discountprice',
                                             'is_publish')

    yayin_durumu = request.GET.get('publish', '')
    kategori = request.GET.get('kategori', '')
    stok = request.GET.get('stock', '')

    if yayin_durumu != '' and kategori != '' and stok != '':
        if stok == True:
            rows = rows.filter(is_publish=yayin_durumu, subbottomcategory_id=kategori,
                               quantity__gte=1).values_list('title', 'subbottomcategory__title',
                                                            'barcode',
                                                            'model_code',
                                                            'stock_code',
                                                            'quantity',
                                                            'size__name',
                                                            'color__name',
                                                            'price',
                                                            'discountprice',
                                                            'is_publish')
        else:
            rows = rows.filter(is_publish=yayin_durumu, subbottomcategory_id=kategori,
                               quantity=0).values_list('title', 'subbottomcategory__title',
                                                       'barcode',
                                                       'model_code',
                                                       'stock_code',
                                                       'quantity',
                                                       'size__name',
                                                       'color__name',
                                                       'price',
                                                       'discountprice',
                                                       'is_publish')
    if yayin_durumu and stok != '':
        if stok == True:
            rows = rows.filter(is_publish=yayin_durumu,
                               quantity__gte=1).values_list('title', 'subbottomcategory__title',
                                                            'barcode',
                                                            'model_code',
                                                            'stock_code',
                                                            'quantity',
                                                            'size__name',
                                                            'color__name',
                                                            'price',
                                                            'discountprice',
                                                            'is_publish')
        else:
            rows = rows.filter(is_publish=yayin_durumu, quantity=0)
    if kategori and stok != '':
        if stok == True:
            rows = rows.filter(is_publish=yayin_durumu, subbottomcategory_id=kategori,
                               quantity__gte=1).values_list('title', 'subbottomcategory__title',
                                                            'barcode',
                                                            'model_code',
                                                            'stock_code',
                                                            'quantity',
                                                            'size__name',
                                                            'color__name',
                                                            'price',
                                                            'discountprice',
                                                            'is_publish')
        else:
            rows = rows.filter(is_publish=yayin_durumu, subbottomcategory_id=kategori,
                               quantity=0).values_list('title', 'subbottomcategory__title',
                                                       'barcode',
                                                       'model_code',
                                                       'stock_code',
                                                       'quantity',
                                                       'size__name',
                                                       'color__name',
                                                       'price',
                                                       'discountprice',
                                                       'is_publish')
    if kategori:
        rows = rows.filter(subbottomcategory_id=kategori).values_list('title', 'subbottomcategory__title',
                                                                      'barcode',
                                                                      'model_code',
                                                                      'stock_code',
                                                                      'quantity',
                                                                      'size__name',
                                                                      'color__name',
                                                                      'price',
                                                                      'discountprice',
                                                                      'is_publish')
    if yayin_durumu != '':
        rows = rows.filter(is_publish=yayin_durumu).values_list('title', 'subbottomcategory__title',
                                                                'barcode',
                                                                'model_code',
                                                                'stock_code',
                                                                'quantity',
                                                                'size__name',
                                                                'color__name',
                                                                'price',
                                                                'discountprice',
                                                                'is_publish')
    if kategori and yayin_durumu:
        rows = rows.filter(is_publish=yayin_durumu, subbottomcategory_id=kategori).values_list('title',
                                                                                               'subbottomcategory__title',
                                                                                               'barcode',
                                                                                               'model_code',
                                                                                               'stock_code',
                                                                                               'quantity',
                                                                                               'size__name',
                                                                                               'color__name',
                                                                                               'price',
                                                                                               'discountprice',
                                                                                               'is_publish')

    if stok != None:
        if stok == True:
            rows = rows.filter(quantity__gte=1).values_list('title', 'subbottomcategory__title',
                                                            'barcode',
                                                            'model_code',
                                                            'stock_code',
                                                            'quantity',
                                                            'size__name',
                                                            'color__name',
                                                            'price',
                                                            'discountprice',
                                                            'is_publish')
        else:
            rows = rows.filter(quantity=0).values_list('title', 'subbottomcategory__title',
                                                       'barcode',
                                                       'model_code',
                                                       'stock_code',
                                                       'quantity',
                                                       'size__name',
                                                       'color__name',
                                                       'price',
                                                       'discountprice',
                                                       'is_publish')

    return exportExcel('products', 'Ürünler', columns=columns, rows=rows)


@login_required(login_url="/yonetim/giris-yap/")
def siparisler(request):
    context = {}
    tredyshop_siparisi = []
    trendyol_siparisi = []
    hepsiburada_siparisi = []

    tredyshop_orders = Order.objects.all().order_by('-created_at')
    trendyol_orders = TrendyolOrders.objects.all().order_by('-order_date')
    hepsiburada_orders = HepsiburadaSiparisler.objects.all().order_by('-order_date')

    query_musteri_adi = request.GET.get('musteri_adi', '')
    query_siparis_no = request.GET.get('siparis_no', '')
    query_barkod = request.GET.get('barkod', '')
    query_urun_adi = request.GET.get('urun_adi', '')
    query_platform = request.GET.get('platform', '')

    query = f"?musteri_adi={query_musteri_adi}&siparis_no={query_siparis_no}&barkod={query_barkod}&urun_adi={query_urun_adi}&platform={query_platform}"

    if query_musteri_adi:
        tredyshop_orders = tredyshop_orders.filter(Q(user__first_name=query_musteri_adi))
        trendyol_orders = trendyol_orders.filter(Q(buyer__icontains=query_musteri_adi))

    if query_siparis_no:
        tredyshop_orders = tredyshop_orders.filter(order_number=query_siparis_no)
        trendyol_orders = trendyol_orders.filter(order_number=query_siparis_no)

    if query_barkod:
        tredyshop_orders = tredyshop_orders.filter(orderproduct__product__barcode=query_barkod)
        trendyol_orders = trendyol_orders.filter(barcode=query_barkod)

    if query_urun_adi:
        tredyshop_orders = tredyshop_orders.filter(orderproduct__title=query_urun_adi)
        trendyol_orders = trendyol_orders.filter(title__icontains=query_urun_adi)

    if query_platform:
        if query_platform == "tredyshop":
            tredyshop_orders = tredyshop_orders
            trendyol_orders = []
        if query_platform == "trendyol":
            tredyshop_orders = []
            trendyol_orders = trendyol_orders
        else:
            tredyshop_orders = []
            trendyol_orders = []

    for o in tredyshop_orders:
        product_list = []
        for product in OrderProduct.objects.filter(order=o):
            product_list.append({
                'urun_adi': product.title,
                'barcode': product.product.barcode,
                'color': product.color,
                'size': product.size,
                'sku': product.product.stock_code,
                'miktar': product.quantity,
            })
        tredyshop_siparisi.append(
            {
                'id': o.id,
                'siparis_no': o.order_number,
                'product_list': product_list,
                'müsteri': o.user,
                'durum': o.status,
                'siparis_tarihi': o.created_at,
                'siparis_tutari': o.order_total,
                'indirim': o.used_coupon,
                'platform': 'tredyshop',
                'query_musteri_adi': query_musteri_adi,
                'query_siparis_no': query_siparis_no,
                'query_barkod': query_barkod,
                'query_urun_adi': query_urun_adi,
                'query_platform': query_platform,
            }
        )

    for t in trendyol_orders:
        product_list = []
        if TrendyolMoreProductOrder.objects.filter(order_number=t.order_number).count() > 1:
            for product in TrendyolMoreProductOrder.objects.filter(order_number=t.order_number):
                product_list.append({
                    'urun_adi': product.title,
                    'barcode': product.barcode,
                    'color': product.color,
                    'size': product.size,
                    'sku': product.stock_code,
                    'miktar': product.quantity,
                })
        else:
            product_list.append({
                'urun_adi': t.title,
                'barcode': t.barcode,
                'color': t.color,
                'size': t.size,
                'sku': t.stock_code,
                'miktar': t.quantity,
            })
        trendyol_siparisi.append(
            {
                'id': t.id,
                'siparis_no': t.order_number,
                'product_list': product_list,
                'müsteri': t.buyer,
                'durum': t.status,
                'siparis_tarihi': t.order_date,
                'siparis_tutari': t.sales_amount,
                'indirim': t.discount_amount,
                'platform': 'trendyol',
            }
        )

    for t in hepsiburada_orders:
        product_list = []
        if HepsiburadaMoreProductOrder.objects.filter(order_number=t.order_number).count() > 1:
            for product in HepsiburadaMoreProductOrder.objects.filter(order_number=t.order_number):
                product_list.append({
                    'urun_adi': product.title,
                    'barcode': product.barcode,
                    'color': product.color,
                    'size': product.size,
                    'sku': product.stock_code,
                    'miktar': product.quantity,
                })
        else:
            product_list.append({
                'urun_adi': t.title,
                'barcode': t.barcode,
                'color': t.color,
                'size': t.size,
                'sku': t.stock_code,
                'miktar': t.quantity,
            })
        hepsiburada_siparisi.append(
            {
                'id': t.id,
                'siparis_no': t.order_number,
                'product_list': product_list,
                'müsteri': t.buyer,
                'durum': t.status,
                'siparis_tarihi': t.order_date,
                'siparis_tutari': t.sales_amount,
                'indirim': t.discount_amount,
                'platform': 'hepsiburada',
            }
        )

    siparisler = tredyshop_siparisi + trendyol_siparisi + hepsiburada_siparisi
    siparisler.sort(key=lambda x: x['siparis_tarihi'], reverse=True)

    p = Paginator(siparisler, 20)
    page = request.GET.get('page')
    siparis = p.get_page(page)

    context.update({
        'siparisler': siparis,
        'query': query,
    })
    return render(request, 'backend/yonetim/sayfalar/siparis_yonetimi/siparisler.html', context)


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
                        seller_product = get_object_or_404(Product, barcode=str(l['barcode']))
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
                    try:
                        color = l['productColor']
                    except:
                        color = None
                    data = TrendyolOrders.objects.create(order_number=orderNumber, packet_number=packetNumber,
                                                         buyer=customerName, quantity=quantity, title=title,
                                                         barcode=barcode, color=color, size=size,
                                                         stock_code=sku,
                                                         unit_price=unitPrice, sales_amount=salesAmount,
                                                         discount_amount=discount, status=status,
                                                         shippment_city=r['shipmentAddress']['city'],
                                                         order_date=datetime_obj_with_tz,
                                                         commission_price=komisyon_tutari,
                                                         service_price=trendyol.hizmet_bedeli)

                    productStatistic(barcode=barcode, title=title, quantity=quantity,
                                     satis=salesAmount)

                    for user in User.objects.filter(is_superuser=True):
                        Notification.objects.create(noti_type="4", title="Yeni Trendyol siparişi alındı.",
                                                    trendyol_orders=data, user=user)
                    sendOrderInfoEmail(platform="Trendyol", email="atmacaahmet5261@hotmail.com", order=data)
            elif len(r['lines']) > 1:
                for l in r['lines']:
                    quantity = l['quantity']
                    size = l['productSize']
                    sku = l['merchantSku']
                    title = l['productName']
                    barcode = l['barcode']
                    try:
                        seller_product = get_object_or_404(Product, barcode=str(l['barcode']))
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
                    TrendyolMoreProductOrder.objects.create(order_number=orderNumber, barcode=barcode, title=title,
                                                            packet_number=packetNumber, color=l['productColor'],
                                                            quantity=quantity, size=size, stock_code=sku,
                                                            unit_price=unitPrice, sales_amount=salesAmount,
                                                            discount_amount=discount, status=status)
                    productStatistic(barcode=barcode, title=title, quantity=quantity,
                                     satis=salesAmount)
                birim_fiyat = 0
                satis_fiyat = 0
                indirim = 0
                miktar = 0
                for product in TrendyolMoreProductOrder.objects.filter(order_number=orderNumber,
                                                                       packet_number=packetNumber):
                    birim_fiyat += product.unit_price
                    satis_fiyat += product.sales_amount
                    indirim += product.discount_amount
                    miktar += product.quantity

                data = TrendyolOrders.objects.create(order_number=orderNumber, packet_number=packetNumber,
                                                     buyer=customerName, quantity=miktar, title="Birden Fazla Ürün",
                                                     barcode="Birden Fazla Barkod", color="Birden Fazla Ürün",
                                                     size="Birden Fazla Ürün", stock_code="Birden Fazla STK",
                                                     unit_price=birim_fiyat, sales_amount=satis_fiyat,
                                                     discount_amount=indirim, status="Birden Fazla",
                                                     shippment_city=r['shipmentAddress']['city'],
                                                     order_date=datetime_obj_with_tz, commission_price=komisyon_tutari,
                                                     service_price=trendyol.hizmet_bedeli)

                for user in User.objects.filter(is_superuser=True):
                    Notification.objects.create(noti_type="4", title="Yeni Trendyol siparişi alındı.",
                                                trendyol_orders=data, user=user)
                sendOrderInfoEmail(platform="Trendyol", email="atmacaahmet5261@hotmail.com", order=data)
    messages.success(request, "Siparişler getirildi.")
    return redirect('admin_siparisler')


@login_required(login_url="/yonetim/giris-yap/")
def order_detail(request, order_number):
    context = {}
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    order = get_object_or_404(Order, order_number=order_number)
    orderproducts = OrderProduct.objects.filter(order=order)
    harcamalar = Harcamalar.objects.filter(siparis_numarasi=order.order_number)

    sorgu_durum = paytr_sorgu(order_number=order_number)

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'order': order,
        'sorgu_durum': sorgu_durum,
        'orderproducts': orderproducts,
        'harcamalar': harcamalar,
    })

    if 'uploadFaturaBtn' in request.POST:
        file = request.FILES['bill']
        order.bill = file
        order.save()
        messages.success(request, 'Fatura yüklendi.')
        return redirect('admin_order_detail', order_number)
    return render(request, 'backend/yonetim/sayfalar/siparis_yonetimi/tredyshop_siparis_detaylari.html', context)


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
def order_tamamla(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    order.status = "Tamamlandı"
    order.save()

    messages.success(request, 'Sipariş tamamlandı.')
    return redirect('admin_order_detail', order_number)


@login_required(login_url="/yonetim/giris-yap/")
def order_mail_gonder(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    total = 0
    order_list = OrderProduct.objects.filter(order=order)

    for p in order_list:
        total += (float(p.quantity * p.product_price))

    customerTredyShopDeliveryOrder(request=request, order=order, order_list=order_list, total=total,
                                   email=order.user.email, grand_total=order.order_total, address=order.address.address)

    messages.success(request, 'E-Posta gönderildi.')
    return redirect('admin_order_detail', order_number)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_order_detail(request, id):
    context = {}
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    order = get_object_or_404(TrendyolOrders, id=id)

    order_products = TrendyolMoreProductOrder.objects.filter(order_number=order.order_number,
                                                             packet_number=order.packet_number)
    harcamalar = Harcamalar.objects.filter(siparis_numarasi=order.order_number)

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'order': order,
        'order_products': order_products,
        'harcamalar': harcamalar
    })

    if 'addTrendyolCost' in request.POST:
        delivery_price = request.POST.get('delivery_price', 0.0)
        commission_price = request.POST.get('commission_price', 0.0)
        service_price = request.POST.get('service_price', 0.0)

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
                Harcamalar.objects.create(siparis_numarasi=order.order_number, harcama_adi=harcama.harcama_adi,
                                          harcama_tutari=harcama.harcama_tutari, harcama_notu=harcama.harcama_notu,
                                          harcama_tipi="Ürün Alımı", durum="İade Yapıldı", created_at=created_at)
        order.save()
        messages.success(request, 'Sipariş iade edildi.')
        return redirect('trendyol_order_detail', id)

    return render(request, 'backend/yonetim/sayfalar/siparis_yonetimi/trendyol_siparis_detaylari.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def urun_maliyeti_ekle(request):
    barcode = request.POST.get('statisticBarcode')
    siparis_no = request.POST.get('siparis_no')
    harcama_adi = request.POST.get('harcama_adi')
    harcama_tutari = request.POST.get('harcama_tutari')
    harcama_not = request.POST.get('harcama_not')

    created_at = datetime.now()

    harcama = Harcamalar.objects.create(siparis_numarasi=siparis_no, harcama_adi=harcama_adi,
                                        harcama_tutari=harcama_tutari,
                                        harcama_notu=harcama_not, harcama_tipi="Ürün Alımı", durum="Ödeme Yapıldı",
                                        created_at=created_at)
    try:
        product_statistic = get_object_or_404(ProductSellStatistic, barcode=barcode)
        product_statistic.maliyet += harcama_tutari
    except:
        pass
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

    musteri_adi = request.GET.get('musteri_adi', '')
    siparis_no = request.GET.get('siparis_no', '')
    urun_adi = request.GET.get('urun_adi', '')

    query = f"?musteri_adi={musteri_adi}&siparis_no={siparis_no}&urun_adi={urun_adi}"

    if musteri_adi:
        cancelling = cancelling.filter(user__first_name=musteri_adi)

    if siparis_no:
        cancelling = cancelling.filter(order__order_number=siparis_no)

    if urun_adi:
        cancelling = cancelling.filter(product__title__icontains=urun_adi)

    p = Paginator(cancelling, 20)
    page = request.GET.get('page')
    cancellings = p.get_page(page)

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'cancellings': cancellings,
        'query': query,
    })

    return render(request, 'backend/yonetim/sayfalar/siparis_yonetimi/iptal_talepleri.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def iade_talepleri(request):
    context = {}
    extradition = ExtraditionRequest.objects.all()
    navbar_notify = readNotification()
    navbar_notify_count = notReadNotification()

    musteri_adi = request.GET.get('musteri_adi', '')
    siparis_no = request.GET.get('siparis_no', '')
    urun_adi = request.GET.get('urun_adi', '')
    iade_nedeni = request.GET.get('iade_nedeni', '')

    query = f"?musteri_adi={musteri_adi}&siparis_no={siparis_no}&urun_adi={urun_adi}&iade_nedeni={iade_nedeni}"

    if musteri_adi:
        extradition = extradition.filter(user__first_name=musteri_adi)

    if siparis_no:
        extradition = extradition.filter(order__order_number=siparis_no)

    if urun_adi:
        extradition = extradition.filter(product__title__icontains=urun_adi)

    if iade_nedeni:
        extradition = extradition.filter(extradition_type=iade_nedeni)

    p = Paginator(extradition, 20)
    page = request.GET.get('page')
    extraditions = p.get_page(page)

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'extraditions': extraditions,
        'query': query
    })

    return render(request, 'backend/yonetim/sayfalar/siparis_yonetimi/iade_talepleri.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def iade_talepleri_detay(request, order_number, product_id):
    context = {}
    product = Product.objects.get(id=product_id)
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
            return redirect('iade_talepleri_detay', order_number, product_id)

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'extradition': extradition,
        'form': form,
        'orderproduct': orderproduct,
    })

    return render(request, 'backend/yonetim/sayfalar/siparis_yonetimi/iade_talepleri_detay.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def haydigiy_product(request):
    context = {}
    return render(request, "backend/yonetim/sayfalar/xml_yonetimi/haydigiy.html", context)


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
def haydigiy_find_not_active_product(request):
    notActiveModaymisProduct()
    createNotification(type="2", title="Modaymış ürünlerde aktif olmayanlar bulundu.",
                       detail="Modaymış ürünlerinde aktif olmayan ürünler aktif değildir olarak güncellendi.")
    messages.success(request, 'Modaymış ürünlerde aktif olmayanlar bulundu')
    return redirect("haydigiy_product")


@login_required(login_url="/yonetim/giris-yap/")
def gecelik_dolabi(request):
    context = {}
    return render(request, "backend/yonetim/sayfalar/xml_yonetimi/gecelik_dolabi.html", context)


@login_required(login_url="/yonetim/giris-yap/")
def gecelikdolabi_product_load(request):
    try:
        addGecelikDolabi()
        messages.success(request, 'Veriler yüklendi!')
        return redirect("gecelik_dolabi")
    except Exception as e:
        return redirect("gecelik_dolabi")


@login_required(login_url="/yonetim/giris-yap/")
def gecelikdolabi_product_update(request):
    updateGecelikDolabi()
    createNotification(type="2", title="Gecelik dolabı ürünlerinin güncellemesi yapıldı.",
                       detail="Gecelik dolabı ürünlerinin güncellemesi yapıldı.")
    messages.success(request, 'Veriler güncelledi!')
    return redirect("gecelik_dolabi")


@login_required(login_url="/yonetim/giris-yap/")
def gecelikdolabi_find_not_active_product(request):
    notActiveGecelikDolabi()
    createNotification(type="2", title="Bella Notte ürünlerde aktif olmayanlar bulundu.",
                       detail="Bella Notte ürünlerinde aktif olmayan ürünler aktif değildir olarak güncellendi.")
    messages.success(request, 'Bella Notte ürünlerde aktif olmayanlar bulundu')
    return redirect("haydigiy_product")

@login_required(login_url="/yonetim/giris-yap/")
def leyna_product(request):
    context = {}
    return render(request, "backend/yonetim/sayfalar/xml_yonetimi/leyna.html", context)


@login_required(login_url="/yonetim/giris-yap/")
def leyna_product_load(request):
    try:
        addLeyna()
        messages.success(request, 'Veriler yüklendi!')
        return redirect("leyna_product")
    except Exception as e:
        return redirect("leyna_product")


@login_required(login_url="/yonetim/giris-yap/")
def leyna_product_update(request):
    updateLeyna()
    createNotification(type="2", title="Leyna ürünlerinin güncellemesi yapıldı.",
                       detail="Leyna ürünlerinin güncellemesi yapıldı.")
    messages.success(request, 'Veriler güncelledi!')
    return redirect("leyna_product")


@login_required(login_url="/yonetim/giris-yap/")
def leyna_find_not_active_product(request):
    notActiveLeyna()
    createNotification(type="2", title="Leyna ürünlerde aktif olmayanlar bulundu.",
                       detail="Leyna ürünlerinde aktif olmayan ürünler aktif değildir olarak güncellendi.")
    messages.success(request, 'Modaymış ürünlerde aktif olmayanlar bulundu')
    return redirect("leyna_product")

@login_required(login_url="/yonetim/giris-yap/")
def xml_fiyat_ayarla(request):
    context = {}

    tredyshop = TredyShopFiyatAyarla.objects.all().last()
    trendyol = TrendyolFiyatAyarla.objects.all().last()
    hepsiburada = HepsiburadaFiyatAyarla.objects.all().last()
    pttavm = PttAvmFiyatAyarla.objects.all().last()
    ciceksepeti = CiceksepetiFiyatAyarla.objects.all().last()

    context.update({
        'tredyshop': tredyshop,
        'trendyol': trendyol,
        'hepsiburada': hepsiburada,
        'pttavm': pttavm,
        'ciceksepeti': ciceksepeti,
    })

    return render(request, "backend/yonetim/sayfalar/xml_yonetimi/fiyat_ayarla.html", context)


class TredyShopFiyatAyarlaInline():
    form_class = TredyShopFiyatAyarlaForm
    model = TredyShopFiyatAyarla
    template_name = "backend/yonetim/sayfalar/xml_yonetimi/tredyshop_fiyat_ayarla.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('tredyshop_fiyat_guncelle', TredyShopFiyatAyarla.objects.all().last().id)

    def formset_karmarji_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        karmarjlari = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for karmarji in karmarjlari:
            karmarji.tredyshop = self.object
            karmarji.save()


class TredyShopFiyatAyarlaCreate(TredyShopFiyatAyarlaInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(TredyShopFiyatAyarlaCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'karmarjlari': TredyShopKarMarjiFormSet(prefix='karmarjlari'),
            }
        else:
            return {
                'karmarjlari': TredyShopKarMarjiFormSet(self.request.POST or None, self.request.FILES or None,
                                                        prefix='karmarjlari'),
            }


class TredyShopFiyatAyarlaUpdate(TredyShopFiyatAyarlaInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(TredyShopFiyatAyarlaUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['tredyshop'] = TredyShopFiyatAyarla.objects.all().last()
        return ctx

    def get_named_formsets(self):
        return {
            'karmarjlari': TredyShopKarMarjiFormSet(self.request.POST or None, self.request.FILES or None,
                                                    instance=self.object, prefix='karmarjlari'),
        }


def delete_tredyshop_karmarji_formset(request, pk):
    try:
        karmarji = TredyShopKarMarji.objects.get(id=pk)
    except karmarji.DoesNotExist:
        messages.success(
            request, 'Bu kayıt mev'
        )
        return redirect('tredyshop_fiyat_guncelle', karmarji.tredyshop.id)

    karmarji.delete()
    messages.success(
        request, 'İlgili kar marjı başarıyla silindi.'
    )
    return redirect('tredyshop_fiyat_guncelle', karmarji.tredyshop.id)


class TrendyolFiyatAyarlaInline():
    form_class = TrendyolFiyatAyarlaForm
    model = TrendyolFiyatAyarla
    template_name = "backend/yonetim/sayfalar/xml_yonetimi/trendyol_fiyat_ayarla.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('trendyol_fiyat_guncelle', TrendyolFiyatAyarla.objects.all().last().id)

    def formset_karmarji_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        karmarjlari = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for karmarji in karmarjlari:
            karmarji.trendyol = self.object
            karmarji.save()


class TrendyolFiyatAyarlaCreate(TrendyolFiyatAyarlaInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(TrendyolFiyatAyarlaCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'karmarjlari': TrendyolKarMarjiFormSet(prefix='karmarjlari'),
            }
        else:
            return {
                'karmarjlari': TrendyolKarMarjiFormSet(self.request.POST or None, self.request.FILES or None,
                                                       prefix='karmarjlari'),
            }


class TrendyolFiyatAyarlaUpdate(TrendyolFiyatAyarlaInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(TrendyolFiyatAyarlaUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['trendyol'] = TrendyolFiyatAyarla.objects.all().last()
        return ctx

    def get_named_formsets(self):
        return {
            'karmarjlari': TrendyolKarMarjiFormSet(self.request.POST or None, self.request.FILES or None,
                                                   instance=self.object, prefix='karmarjlari'),
        }


def delete_trendyol_karmarji_formset(request, pk):
    try:
        karmarji = TrendyolKarMarji.objects.get(id=pk)
    except karmarji.DoesNotExist:
        messages.success(
            request, 'Bu kayıt mev'
        )
        return redirect('trendyol_fiyat_guncelle', karmarji.trendyol.id)

    karmarji.delete()
    messages.success(
        request, 'İlgili kar marjı başarıyla silindi.'
    )
    return redirect('trendyol_fiyat_guncelle', karmarji.trendyol.id)


class HepsiburadaFiyatAyarlaInline():
    form_class = HepsiburadaFiyatAyarlaForm
    model = HepsiburadaFiyatAyarla
    template_name = "backend/yonetim/sayfalar/xml_yonetimi/hepsiburada_fiyat_ayarla.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('hepsiburada_fiyat_guncelle', HepsiburadaFiyatAyarla.objects.all().last().id)

    def formset_karmarji_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        karmarjlari = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for karmarji in karmarjlari:
            karmarji.hepsiburada = self.object
            karmarji.save()


class HepsiburadaFiyatAyarlaCreate(HepsiburadaFiyatAyarlaInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(HepsiburadaFiyatAyarlaCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'karmarjlari': HepsiburadaKarMarjiFormSet(prefix='karmarjlari'),
            }
        else:
            return {
                'karmarjlari': HepsiburadaKarMarjiFormSet(self.request.POST or None, self.request.FILES or None,
                                                          prefix='karmarjlari'),
            }


class HepsiburadaFiyatAyarlaUpdate(HepsiburadaFiyatAyarlaInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(HepsiburadaFiyatAyarlaUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['hepsiburada'] = HepsiburadaFiyatAyarla.objects.all().last()
        return ctx

    def get_named_formsets(self):
        return {
            'karmarjlari': HepsiburadaKarMarjiFormSet(self.request.POST or None, self.request.FILES or None,
                                                      instance=self.object, prefix='karmarjlari'),
        }


def delete_hepsiburada_karmarji_formset(request, pk):
    try:
        karmarji = HepsiburadaKarMarji.objects.get(id=pk)
    except karmarji.DoesNotExist:
        messages.success(
            request, 'Bu kayıt mevcut değil'
        )
        return redirect('hepsiburada_fiyat_guncelle', karmarji.hepsiburada.id)

    karmarji.delete()
    messages.success(
        request, 'İlgili kar marjı başarıyla silindi.'
    )
    return redirect('hepsiburada_fiyat_guncelle', karmarji.hepsiburada.id)


class CiceksepetiFiyatAyarlaInline():
    form_class = CiceksepetiFiyatAyarlaForm
    model = CiceksepetiFiyatAyarla
    template_name = "backend/yonetim/sayfalar/xml_yonetimi/ciceksepeti_fiyat_ayarla.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('ciceksepeti_fiyat_guncelle', CiceksepetiFiyatAyarla.objects.all().last().id)

    def formset_karmarji_valid(self, formset):

        karmarjlari = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for karmarji in karmarjlari:
            karmarji.amazon = self.object
            karmarji.save()


class CiceksepetiFiyatAyarlaCreate(CiceksepetiFiyatAyarlaInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(CiceksepetiFiyatAyarlaCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'karmarjlari': CiceksepetiKarMarjiFormSet(prefix='karmarjlari'),
            }
        else:
            return {
                'karmarjlari': CiceksepetiKarMarjiFormSet(self.request.POST or None, self.request.FILES or None,
                                                          prefix='karmarjlari'),
            }


class CiceksepetiFiyatAyarlaUpdate(CiceksepetiFiyatAyarlaInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(CiceksepetiFiyatAyarlaUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['ciceksepeti'] = CiceksepetiFiyatAyarla.objects.all().last()
        return ctx

    def get_named_formsets(self):
        return {
            'karmarjlari': CiceksepetiKarMarjiFormSet(self.request.POST or None, self.request.FILES or None,
                                                      instance=self.object, prefix='karmarjlari'),
        }


def delete_ciceksepeti_karmarji_formset(request, pk):
    try:
        karmarji = CiceksepetiKarMarji.objects.get(id=pk)
    except karmarji.DoesNotExist:
        messages.success(
            request, 'Bu kayıt mevcut değildir.'
        )
        return redirect('amazon_fiyat_guncelle', karmarji.amazon.id)

    karmarji.delete()
    messages.success(
        request, 'İlgili kar marjı başarıyla silindi.'
    )
    return redirect('amazon_fiyat_guncelle', karmarji.amazon.id)


class PttAvmFiyatAyarlaInline():
    form_class = PttAvmFiyatAyarlaForm
    model = PttAvmFiyatAyarla
    template_name = "backend/yonetim/sayfalar/xml_yonetimi/pttavm_fiyat_ayarla.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('pttavm_fiyat_guncelle', PttAvmFiyatAyarla.objects.all().last().id)

    def formset_karmarji_valid(self, formset):

        karmarjlari = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for karmarji in karmarjlari:
            karmarji.pttavm = self.object
            karmarji.save()


class PttAvmFiyatAyarlaCreate(PttAvmFiyatAyarlaInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(PttAvmFiyatAyarlaCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'karmarjlari': PttAvmKarMarjiFormSet(prefix='karmarjlari'),
            }
        else:
            return {
                'karmarjlari': PttAvmKarMarjiFormSet(self.request.POST or None, self.request.FILES or None,
                                                     prefix='karmarjlari'),
            }


class PttAvmFiyatAyarlaUpdate(PttAvmFiyatAyarlaInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(PttAvmFiyatAyarlaUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['pttavm'] = PttAvmFiyatAyarla.objects.all().last()
        return ctx

    def get_named_formsets(self):
        return {
            'karmarjlari': PttAvmKarMarjiFormSet(self.request.POST or None, self.request.FILES or None,
                                                 instance=self.object, prefix='karmarjlari'),
        }


def delete_pttavm_karmarji_formset(request, pk):
    try:
        karmarji = PttAvmKarMarji.objects.get(id=pk)
    except karmarji.DoesNotExist:
        messages.success(
            request, 'Bu kayıt mevcut değildir.'
        )
        return redirect('pttavm_fiyat_guncelle', karmarji.pttavm.id)

    karmarji.delete()
    messages.success(
        request, 'İlgili kar marjı başarıyla silindi.'
    )
    return redirect('pttavm_fiyat_guncelle', karmarji.pttavm.id)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_indirim_olustur(request):
    context = {}
    products = None
    category = SubBottomCategory.objects.all()
    kategori = request.GET.get('kategori')
    indirim_durumu = request.GET.get('indirim_durumu')
    baslik = request.GET.get('baslik')
    barkod = request.GET.get('barkod')

    query = f"?kategori={kategori}&indirim_durumu={indirim_durumu}&baslik={baslik}&barkod={barkod}"

    products = Product.objects.filter(is_publish_trendyol=True).order_by("-create_at")

    context.update({
        'category': category,
        'query': query
    })

    if kategori:
        select_category = SubBottomCategory.objects.get(id=kategori)
        products = Product.objects.filter(subbottomcategory_id=kategori, is_publish_trendyol=True).order_by(
            "-create_at")
        context.update({
            'select_category': select_category,
        })

    if barkod:
        barcode = barkod
        products = Product.objects.filter(barcode=barkod, is_publish_trendyol=True).order_by("-create_at")
        context.update({
            'barcode': barcode,
        })

    if baslik:
        title = baslik
        products = Product.objects.filter(title__icontains=baslik, is_publish_trendyol=True).order_by("-create_at")
        context.update({
            'title': title,
        })

    if indirim_durumu:
        durum = indirim_durumu
        if kategori:
            products = Product.objects.filter(subbottomcategory_id=kategori, is_publish_trendyol=True,
                                              is_trendyol_discountprice=indirim_durumu).order_by(
                "-create_at")
        else:
            products = Product.objects.filter(is_publish_trendyol=True,
                                              is_trendyol_discountprice=indirim_durumu).order_by(
                "-create_at")
        context.update({
            'durum': durum,
        })

    if products:
        p = Paginator(products, 30)
        page = request.GET.get('page')
        product = p.get_page(page)
        context.update({
            'products': product
        })
    return render(request, 'backend/yonetim/sayfalar/trendyol/indirim_olustur.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_indirim_kaydet(request):
    product_id = request.GET.get('productID')
    discountprice = request.GET.get('discountprice', '')
    discountStatus = request.GET.get('discountStatus', '')

    trendyol_discountprice = None
    trendyol_is_discount = None

    if discountprice:
        trendyol_discountprice = float(discountprice)

    if discountStatus:
        trendyol_is_discount = discountStatus

    product = Product.objects.get(id=product_id)
    product.trendyol_discountprice = trendyol_discountprice
    product.is_trendyol_discountprice = trendyol_is_discount
    product.save()

    data = "success"
    return JsonResponse(data=data, safe=False)

@login_required(login_url="/yonetim/giris-yap/")
def trendyol_beden_eslestir(request):
    context = {}
    category = SubBottomCategory.objects.all()
    products = None

    kategori = request.GET.get('kategori')
    publish_status = request.GET.get('publish_status')

    query = f"?kategori={kategori}&publish_status={publish_status}"

    select_category = None
    is_publish = None

    colors = Color.objects.all()
    beden = Size.objects.all()

    if kategori:
        select_category = SubBottomCategory.objects.get(id=kategori)
        is_publish = publish_status
        if publish_status == "True":
            products = ProductVariant.objects.filter(product__subbottomcategory_id=kategori, is_publish=True,
                                                     is_publish_trendyol=True).order_by("-create_at")
        elif publish_status == "False":
            products = ProductVariant.objects.filter(product__subbottomcategory_id=kategori, is_publish=True,
                                                     is_publish_trendyol=False).order_by("-create_at")
        else:
            products = ProductVariant.objects.filter(product__subbottomcategory_id=kategori, is_publish=True).order_by(
                "-create_at")

    product = None

    if products:
        p = Paginator(products, 30)
        page = request.GET.get('page')
        product = p.get_page(page)

    context.update({
        'is_publish': is_publish,
        'category': category,
        'products': product,
        'query': query,
        'select_category': select_category,
        'colors': colors,
        'beden': beden,
    })
    return render(request, "backend/yonetim/sayfalar/trendyol/beden_renk_eslestir.html", context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_beden_kaydet(request):
    product_id = request.GET.get('productID')
    renk = request.GET.get('renk', '')
    beden = request.GET.get('beden', '')

    color = None
    size = None

    if renk:
        color = Color.objects.get(id=renk)

    if beden:
        size = Size.objects.get(id=beden)

    varyant = ProductVariant.objects.get(id=product_id)
    varyant.color = color
    varyant.size = size
    varyant.save()

    data = "success"
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_ozellik_eslestir(request):
    context = {}
    category = SubBottomCategory.objects.all()
    products = None

    kategori = request.GET.get('kategori')
    publish_status = request.GET.get('publish_status')

    query = f"?kategori={kategori}&publish_status={publish_status}"

    select_category = None
    is_publish = None

    colors = Color.objects.all()
    height = Height.objects.all()
    waist = Waist.objects.all()
    pattern = Pattern.objects.all()
    fabrictype = FabricType.objects.all()
    tablet_models = TabletModel.objects.all()
    case_type = TableCaseType.objects.all()
    sleep_mode = SleepMode.objects.all()
    beden = Size.objects.all()
    bag_pattern = BagPattern.objects.all()
    sex = Sex.objects.all()
    environment = EnvironmentType.objects.all()
    heel_type = HeelType.objects.all()
    heel_size = HeelSize.objects.all()
    bijuteri_tema = BijuteriTheme.objects.all()
    legtype = LegType.objects.all()
    material = MaterialType.objects.all()
    yaka_tipi = CollerType.objects.all()
    desen = Desen.objects.all()
    paket_icerigi = PaketIcerigi.objects.all()
    koleksiyon = Koleksiyon.objects.all()
    dokumaTipi = DokumaTipi.objects.all()
    ozellik = Ozellik.objects.all()
    kol_tipi = ArmType.objects.all()
    urun_detay = UrunDetay.objects.all()
    persona = Persona.objects.all()
    siluet = Siluet.objects.all()
    altsiluet = AltSiluet.objects.all()
    ustsiluet = UstSiluet.objects.all()
    paddetay = PadDetay.objects.all()

    if kategori:
        select_category = SubBottomCategory.objects.get(id=kategori)
        is_publish = publish_status
        if publish_status == "True":
            products = Product.objects.filter(subbottomcategory_id=kategori, is_publish=True).order_by("-create_at")
        elif publish_status == "False":
            products = Product.objects.filter(subbottomcategory_id=kategori, is_publish=False).order_by("-create_at")
        else:
            products = Product.objects.filter(subbottomcategory_id=kategori, is_publish=True).order_by(
                "-create_at")

    product = None

    if products:
        p = Paginator(products, 30)
        page = request.GET.get('page')
        product = p.get_page(page)

    context.update({
        'is_publish': is_publish,
        'category': category,
        'products': product,
        'query': query,
        'select_category': select_category,
        'colors': colors,
        'tablet_models': tablet_models,
        'case_type': case_type,
        'sleep_mode': sleep_mode,
        'beden': beden,
        'bag_pattern': bag_pattern,
        'sex': sex,
        'environment': environment,
        'heel_type': heel_type,
        'heel_size': heel_size,
        'height': height,
        'pattern': pattern,
        'fabrictype': fabrictype,
        'waist': waist,
        'bijuteri_tema': bijuteri_tema,
        'legtype': legtype,
        'material': material,
        'yaka_tipi':yaka_tipi,
        'desen':desen,
        'paket_icerigi':paket_icerigi,
        'koleksiyon':koleksiyon,
        'dokumaTipi':dokumaTipi,
        'ozellik':ozellik,
        'kol_tipi':kol_tipi,
        'urun_detay':urun_detay,
        'persona':persona,
        'siluet':siluet,
        'altsiluet':altsiluet,
        'ustsiluet':ustsiluet,
        'paddetay':paddetay,
    })
    return render(request, "backend/yonetim/sayfalar/trendyol/ozellik_eslestir.html", context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_ozellik_kaydet(request):
    product_id = request.GET.get('productID')
    marka = request.GET.get('marka', '')
    canta_desen = request.GET.get('canta_desen', '')
    agegroup = request.GET.get('agegroup', '')
    sex_type = request.GET.get('sex', '')
    ortam = request.GET.get('ortam', '')
    topuk_tipi = request.GET.get('topuk_tipi', '')
    topuk_boyu = request.GET.get('topuk_boyu', '')
    heighttype = request.GET.get('height', '')
    kalip = request.GET.get('pattern', '')
    kumas_tipi = request.GET.get('fabrictype', '')
    bel = request.GET.get('waist', '')
    bijuteri_tema = request.GET.get('bijuteri_tema', '')
    pacatipi = request.GET.get('pacatipi', '')
    materyal = request.GET.get('materyal', '')
    yaka_tipi = request.GET.get('yaka_tipi', '')
    desen = request.GET.get('desen', '')
    paket_icerigi = request.GET.get('paket_icerigi', '')
    koleksiyon = request.GET.get('koleksiyon', '')
    dokumaTipi = request.GET.get('dokumaTipi', '')
    ozellik = request.GET.get('ozellik', '')
    kol_tipi = request.GET.get('kol_tipi', '')
    persona = request.GET.get('persona', '')
    siluet = request.GET.get('siluet', '')
    urundetay = request.GET.get('urun_detay', '')
    altsiluet = request.GET.get('altsiluet', '')
    ustsiluet = request.GET.get('ustsiluet', '')
    paddetay = request.GET.get('paddetay', '')

    sex = None
    environment = None
    bagpattern = None
    heeltype = None
    heelsize = None
    height = None
    pattern = None
    fabrictype = None
    waist = None
    bijuteri_theme = None
    legtype = None
    material = None
    collartype = None
    desentype = None
    paketicerigi = None
    koleksyiontype = None
    dokumatype = None
    ozelliktype = None
    armtype = None
    personatype = None
    siluettype = None
    urundetaytype = None
    altsiluettype = None
    ustsiluettype = None
    paddetaytype = None

    if sex_type:
        sex = Sex.objects.get(id=sex_type)

    if ortam:
        environment = EnvironmentType.objects.get(id=ortam)

    if canta_desen:
        bagpattern = BagPattern.objects.get(id=canta_desen)

    if topuk_tipi:
        heeltype = HeelType.objects.get(id=topuk_tipi)

    if topuk_boyu:
        heelsize = HeelSize.objects.get(id=topuk_boyu)

    if heighttype:
        height = Height.objects.get(id=heighttype)

    if kalip:
        pattern = Pattern.objects.get(id=kalip)

    if kumas_tipi:
        fabrictype = FabricType.objects.get(id=kumas_tipi)

    if bel:
        waist = Waist.objects.get(id=bel)

    if bijuteri_tema:
        bijuteri_theme = BijuteriTheme.objects.get(id=bijuteri_tema)

    if pacatipi:
        legtype = LegType.objects.get(id=pacatipi)

    if materyal:
        material = MaterialType.objects.get(id=materyal)

    if yaka_tipi:
        collartype = CollerType.objects.get(id=yaka_tipi)

    if desen:
        desentype = Desen.objects.get(id=desen)

    if paket_icerigi:
        paketicerigi = PaketIcerigi.objects.get(id=paket_icerigi)

    if koleksiyon:
        koleksyiontype = Koleksiyon.objects.get(id=koleksiyon)

    if dokumaTipi:
        dokumatype = DokumaTipi.objects.get(id=koleksiyon)

    if ozellik:
        ozelliktype = Ozellik.objects.get(id=koleksiyon)

    if kol_tipi:
        armtype = ArmType.objects.get(id=kol_tipi)

    if persona:
        personatype = Persona.objects.get(id=persona)

    if siluet:
        siluettype = Siluet.objects.get(id=siluet)

    if urundetay:
        urundetaytype = UrunDetay.objects.get(id=urundetay)

    if altsiluet:
        altsiluettype = AltSiluet.objects.get(id=altsiluet)

    if ustsiluet:
        ustsiluettype = UstSiluet.objects.get(id=ustsiluet)

    if paddetay:
        paddetaytype = PadDetay.objects.get(id=paddetay)

    product = Product.objects.get(id=product_id)
    product.age_group = agegroup
    product.sextype = sex
    product.environment = environment
    product.bag_pattern = bagpattern
    product.heeltype = heeltype
    product.heelsize = heelsize
    product.height = height
    product.pattern = pattern
    product.fabrictype = fabrictype
    product.waist = waist
    product.bijuteri_theme = bijuteri_theme
    product.legtype = legtype
    product.material = material
    product.collartype = collartype
    product.desen = desentype
    product.paket_icerigi = paketicerigi
    product.koleksiyon = koleksyiontype
    product.dokuma_tipi = dokumatype
    product.ozellik = ozelliktype
    product.armtype = armtype
    product.persona = personatype
    product.siluet = siluettype
    product.urundetay = urundetaytype
    product.altsiluet = altsiluettype
    product.usttsiluet = ustsiluettype
    product.peddetay = paddetaytype
    product.save()

    data = "success"
    return JsonResponse(data=data, safe=False)


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

    return render(request, 'backend/yonetim/sayfalar/trendyol/batch_request.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_batch_request_detail(request, batch_request):
    context = {}
    trendyol = Trendyol.objects.all().last()

    all_batch_request = get_object_or_404(LogRecords, batch_id=batch_request)

    api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                            supplier_id=trendyol.saticiid)
    service = ProductIntegrationService(api)
    response = service.get_batch_requests(batch_request_id=batch_request)
    request_id = response['batchRequestId']
    if all_batch_request.log_type == "1":
        for i in response['items']:
            if i['status'] == 'SUCCESS':
                product = ProductVariant.objects.get(barcode=i['requestItem']['product']['barcode'])
                product.is_publish_trendyol = True
                product.save()
        context.update({
            'response': response,
            'all_batch_request': all_batch_request,
            "products": Product.objects.all(),
        })
    if all_batch_request.log_type == "2":
        context.update({
            'response': response,
            'all_batch_request': all_batch_request
        })
    if all_batch_request.log_type == "4":
        for i in response['items']:
            if i['status'] == 'SUCCESS':
                product = ProductVariant.objects.get(barcode=i['requestItem']['product']['barcode'])
                product.is_publish_trendyol = False
                product.save()
        context.update({
            'response': response,
            'all_batch_request': all_batch_request,

        })

    return render(request, 'backend/yonetim/sayfalar/trendyol/batch_request_detay.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_batch_request_export_excell(request, batch_request):
    column = ["Tip", "Ürün Barkodu", "Durum", "Açıklama"]
    trendyol = Trendyol.objects.all().last()

    all_batch_request = get_object_or_404(LogRecords, batch_id=batch_request)

    api = TrendyolApiClient(api_key=trendyol.apikey, api_secret=trendyol.apisecret,
                            supplier_id=trendyol.saticiid)
    service = ProductIntegrationService(api)
    response = service.get_batch_requests(batch_request_id=batch_request)
    rows = []
    for r in response['items']:
        data = [all_batch_request.get_log_type_display(), r['requestItem']["barcode"], r["status"], r["failureReasons"]]
        rows.append(data)
    return exportExcel(filename="Log", sheetname="Log Kaydı", columns=column, rows=rows)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_batch_request_delete(request, id):
    all_batch_request = LogRecords.objects.get(id=id)
    all_batch_request.delete()
    messages.info(request, 'Batch Request başarıyla silindi!')
    return redirect('trendyol_batch_request')


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_batch_request_delete_all(request):
    all_batch_request = LogRecords.objects.all()
    for br in all_batch_request:
        br.delete()
    messages.success(request, 'Batch Request başarıyla silindi!')
    return redirect('trendyol_batch_request')


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_yuklu_urunler(request):
    context = {}
    trendyol = Trendyol.objects.all().last()

    approved = request.GET.get('approved', None)
    barcode = request.GET.get('barcode', None)
    startDate = request.GET.get('startDate', None)
    endDate = request.GET.get('endDate', None)
    page = request.GET.get('page')
    dateQueryType = request.GET.get('dateQueryType', None)
    size = request.GET.get('size', 100)

    data = {
        'approved': approved or None,
        'barcode': barcode or None,
        'startDate': startDate or None,
        'endDate': endDate or None,
        'page': page,
        'dateQueryType': dateQueryType or None,
        'size': size or 100
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

    return render(request, 'backend/yonetim/sayfalar/trendyol/urunler.html', context)


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
    size = request.GET.get('size', 200)

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

    tredyshop_product = ProductVariant.objects.filter(is_publish_trendyol=True)

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
        'size': int(size),
    })

    return render(request, 'backend/yonetim/sayfalar/trendyol/hatali_urunler.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_hatali_urunler_aktif_yap(request):
    barcodes = request.GET.getlist('barcode[]')
    for barcode in barcodes:
        if ProductVariant.objects.filter(barcode=barcode).exists():
            product = ProductVariant.objects.get(barcode=barcode)
            product.is_publish_trendyol = True
            product.save()
    data = 'success'
    return JsonResponse(data=data, safe=False)


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

    return render(request, 'backend/yonetim/sayfalar/trendyol/komisyon.html', context)


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
    return render(request, 'backend/yonetim/sayfalar/trendyol/komisyon_detay.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_komisyon_sil(request, id):
    TrendyolCommission.objects.get(id=id).delete()
    messages.info(request, 'İlgili komisyon silindi.')
    return redirect('trendyol_komisyon')


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

    return render(request, 'backend/yonetim/sayfalar/hepsiburada/hesap_bilgileri.html', context)


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
    products = Product.objects.filter(subbottomcategory=category, title__icontains=title, is_publish=True,
                                      is_publish_trendyol=False)
    return products


def hepsiburadaUpdateCallingProduct(category, title):
    products = Product.objects.filter(subbottomcategory=category, title__icontains=title, is_publish=True,
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

                items.append(hepsiburadaProductData(categoryId=hepsiburada_category, merchant=hepsiburada.merchantID,
                                                    merchantSku=p.stock_code.upper(), VaryantGroupID=p.model_code,
                                                    barcode=p.barcode, title=title, detail=detail, brand=p.brand.title,
                                                    price=float(p.price),
                                                    quantity=p.quantity, image1=p.image_url1, image2=p.image_url2,
                                                    image3=p.image_url3, image4=p.image_url4, image5=p.image_url5,
                                                    color=p.color, size=p.size))

                product_data = items
                p.hepsiburada_category_id = int(hepsiburada_category)
                p.save()

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'integrator.json')
        with open(file_path, 'w', encoding='utf8') as out_file:
            json.dump(product_data, out_file, sort_keys=True, indent=4,
                      ensure_ascii=False)

        files = {"file": ("integrator.json", open(file_path, "rb"), "application/json")}

        headers = {
            "accept": "application/json",
            "authorization": "Basic dHJlZHlzaG9wX2RldjpIYjEyMzQ1IQ=="
        }

        url = "https://mpop-sit.hepsiburada.com/product/api/products/import"

        response = requests.post(url, files=files, headers=headers)

        # api = HepsiburadaApiClient(username=hepsiburada.username, password=hepsiburada.password,
        #                           mercant_id=hepsiburada.merchantID)
        # service = HepsiburadaProductIntegrationService(api)
        # response = service.create_products(files=files)
        print(response.text)

        # messages.success(request, f"{response}")
        # log_record = LogRecords.objects.create(log_type="1", batch_id=str(response['batchRequestId']))
        return redirect('hepsiburada_add_product_giyim_send', id)
    return render(request, 'backend/adminpage/pages/hepsiburada/urun_girisi_giyim_send_hepsiburada.html', context)


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

    form = IssuedInvoicesAddForm(data=request.POST, files=request.FILES)
    if 'addBtn' in request.POST:
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
                return redirect("kesilen_faturalar")

    context.update({
        'faturalar': fatura,
        'query': query,
        'form': form,
    })
    return render(request, 'backend/yonetim/sayfalar/finans_yonetimi/kesilen_faturalar.html', context)


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
    return render(request, 'backend/yonetim/sayfalar/finans_yonetimi/kesilen_fatura_guncelle.html', context)


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

    form = InvoicesReceivedAddForm(data=request.POST, files=request.FILES)
    if 'addBtn' in request.POST:
        if form.is_valid():
            data = form.save()
            kdv_tutari = data.price * (data.tax_rate / 100)
            toplam_tutar = kdv_tutari + data.price
            fatura = InvoicesReceived.objects.get(id=data.id)
            fatura.tax_amount = kdv_tutari
            fatura.price_amount = toplam_tutar
            fatura.save()
            messages.success(request, 'Fatura başarıyla eklendi!')
            return redirect("alinan_faturalar")

    context.update({
        'faturalar': fatura,
        'query': query,
        'form': form,
    })
    return render(request, 'backend/yonetim/sayfalar/finans_yonetimi/alinan_faturalar.html', context)


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
    return render(request, 'backend/yonetim/sayfalar/finans_yonetimi/alinan_fatura_guncelle.html', context)


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
        if h.harcama_tutari:
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

    return render(request, 'backend/yonetim/sayfalar/finans_yonetimi/harcamalar.html', context)


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
    return render(request, 'backend/yonetim/sayfalar/finans_yonetimi/harcama_guncelle.html', context)


def harcamalar_export_excel(request):
    columns = ['Harcama Tipi', 'Harcama Adı', 'Harcama Tutarı', 'Harcama Tarihi']

    rows = Harcamalar.objects.all().values_list('harcama_tipi', 'harcama_adi', 'harcama_tutari', 'created_at')
    return exportExcel('Harcamalar', 'Harcamalar', columns=columns, rows=rows)


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

    for o in HepsiburadaSiparisler.objects.all().exclude(status="İptal Edildi"):
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

    data = [int(daily_order_total), int(mountly_order_total), int(yearly_order_total), ay, yil, gunluk_degisim,
            aylik_degisim,
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

    for o in HepsiburadaSiparisler.objects.all().exclude(status="İptal Edildi"):
        total_cash_list.append(o.sales_amount)

    for o in HepsiburadaSiparisler.objects.all().exclude(status="İptal Edildi"):
        kargo_ucreti = o.delivery_price
        if o.is_return == True:
            komisyon_ucreti = 0
        else:
            if o.commission_price:
                komisyon_ucreti = o.commission_price
            else:
                komisyon_ucreti = 0

        hizmet_bedeli = o.service_price + o.process_price

        if o.delivery_price is None:
            kargo_ucreti = 0.0

        if o.service_price is None:
            hizmet_bedeli = 0.0

        kesintiler += kargo_ucreti + komisyon_ucreti + hizmet_bedeli

    for tc in total_cash_list:
        total_cash += tc

    for h in harcamalar.filter(durum="Ödeme Yapıldı"):
        if h.harcama_tutari:
            toplam_harcamalar += h.harcama_tutari

    for h in harcamalar.filter(durum="İade Yapıldı"):
        iade_harcamalar += h.harcama_tutari

    for o in Order.objects.filter(status="İptal Edildi"):
        iade_list.append(o.order_total)

    for o in TrendyolOrders.objects.filter(is_return=True):
        iade_list.append(o.sales_amount)

    for o in HepsiburadaSiparisler.objects.filter(is_return=True):
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

        for o in HepsiburadaSiparisler.objects.all().exclude(status="İptal Edildi"):
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

                    hizmet_bedeli = o.service_price + o.process_price

                    if o.delivery_price is None:
                        kargo_ucreti = 0.0

                    if o.service_price is None:
                        hizmet_bedeli = 0.0

                    ilgili_gun_kesintiler += kargo_ucreti + komisyon_ucreti + hizmet_bedeli

        ilgili_gun_satislar_list.append(ilgili_gun_satislar)
        ilgili_gun_kesintiler_list.append(ilgili_gun_kesintiler)

        for h in Harcamalar.objects.filter(durum="Ödeme Yapıldı", created_at__day=yedigunonce.day,
                                           created_at__month=yedigunonce.month, created_at__year=yedigunonce.year):
            if h.harcama_tutari:
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

        for o in HepsiburadaSiparisler.objects.filter(is_return=True):
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
def aylik_kar(request):
    ay = int(request.GET.get('ay', datetime.today().month))
    yil = datetime.today().year

    ilgili_ay_satislar = 0
    ilgili_ay_kesintiler = 0
    ilgili_ay_harcamalar = 0
    ilgili_ay_iade_harcamalar = 0
    ilgili_ay_iadeler = 0

    for o in Order.objects.filter(created_at__year=yil).exclude(status="İptal Edildi"):
        if o.created_at.month == ay:
            ilgili_ay_satislar += o.order_total

    for o in TrendyolOrders.objects.filter(order_date__year=yil).exclude(status="İptal Edildi"):
        if o.order_date.month == ay:
            ilgili_ay_satislar += o.sales_amount
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

            ilgili_ay_kesintiler += kargo_ucreti + komisyon_ucreti + hizmet_bedeli

    for o in HepsiburadaSiparisler.objects.filter(order_date__year=yil).exclude(status="İptal Edildi"):
        if o.order_date.month == ay:
            ilgili_ay_satislar += o.sales_amount
            kargo_ucreti = o.delivery_price

            if o.is_return == True:
                komisyon_ucreti = 0.0
            else:
                if o.commission_price:
                    komisyon_ucreti = o.commission_price
                else:
                    komisyon_ucreti = 0

            hizmet_bedeli = o.service_price + o.process_price
            if o.delivery_price is None:
                kargo_ucreti = 0.0

            if o.service_price is None:
                hizmet_bedeli = 0.0

            ilgili_ay_kesintiler += kargo_ucreti + komisyon_ucreti + hizmet_bedeli

    for h in Harcamalar.objects.filter(created_at__year=yil):
        if h.created_at.month == ay:
            if h.harcama_tutari:
                ilgili_ay_harcamalar += h.harcama_tutari

    for h in Harcamalar.objects.filter(durum="İade Yapıldı", created_at__year=yil):
        if h.created_at.month == ay:
            ilgili_ay_iade_harcamalar += h.harcama_tutari

    for o in Order.objects.filter(status="İptal Edildi", updated_at__year=yil):
        if o.updated_at.month == ay:
            ilgili_ay_iadeler += o.order_total

    for o in TrendyolOrders.objects.filter(is_return=True, order_date__year=yil):
        if o.order_date.month == ay:
            ilgili_ay_iadeler += o.sales_amount

    for o in HepsiburadaSiparisler.objects.filter(is_return=True, order_date__year=yil):
        if o.order_date.month == ay:
            ilgili_ay_iadeler += o.sales_amount

    ilgili_ay_toplam_maliyet = ilgili_ay_harcamalar + ilgili_ay_kesintiler + ilgili_ay_iadeler - ilgili_ay_iade_harcamalar
    ilgili_ay_kar = ilgili_ay_satislar - ilgili_ay_toplam_maliyet

    data = [int(ilgili_ay_kar), int(ilgili_ay_satislar), int(ilgili_ay_toplam_maliyet)]
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def en_cok_siparis_gelen_10_sehir(request):
    from collections import Counter
    tum_sehirler_list = []
    alisveris_sayisi_list = []

    for o in TrendyolOrders.objects.all():
        if o.shippment_city != None:
            tum_sehirler_list.append(o.shippment_city)

    for o in HepsiburadaSiparisler.objects.all():
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

    update_type = request.GET.get('update_type', '')

    if update_type:
        history = history.filter(history_type=update_type)

    query = f"?guncelleme_tipi={history}"

    p = Paginator(history, 20)
    page = request.GET.get('page')
    histories = p.get_page(page)

    context.update({
        'navbar_notify': navbar_notify,
        'navbar_notify_count': navbar_notify_count,
        'histories': histories,
        'query': query,
    })
    return render(request, 'backend/yonetim/sayfalar/gecmis_kayitlar/guncelleme_gecmisi.html', context)


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

    products = Product.objects.filter(title__icontains=series) | Product.objects.filter(
        barcode__icontains=series) | Product.objects.filter(
        stock_code__icontains=series) | Product.objects.filter(model_code__icontains=series)

    if len(products) > 0:
        data = []
        for r in products[:5]:
            item = {
                'id': r.id,
                'p_title': r.title,
                'slug': r.slug,
                'image': r.image_url1,
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

    musteri_adi = request.GET.get('musteri_adi', '')
    eposta = request.GET.get('eposta', '')
    mobile = request.GET.get('mobile', '')
    sex = request.GET.get('sex', '')

    query = f"?musteri_adi={musteri_adi}&eposta={eposta}&mobile={mobile}&sex={sex}"

    if musteri_adi:
        tum_kullanicilar = tum_kullanicilar.filter(
            Q(first_name__icontains=musteri_adi) | Q(last_name__icontains=musteri_adi))

    if eposta:
        tum_kullanicilar = tum_kullanicilar.filter(email=eposta)

    if mobile:
        tum_kullanicilar = tum_kullanicilar.filter(mobile=mobile)

    if sex:
        if sex == "erkek":
            tum_kullanicilar = tum_kullanicilar.filter(gender=True)
        elif sex == "kadın":
            tum_kullanicilar = tum_kullanicilar.filter(gender=False)

    p = Paginator(tum_kullanicilar, 50)
    page = request.GET.get('page')
    kullanicilar = p.get_page(page)

    context.update({
        'kullanicilar': kullanicilar,
        'query': query
    })

    if 'single_send_mail' in request.POST:
        email = request.POST.get('single_email')
        messages.success(request, f'{email} eposta adresine mail başarıyla gönderildi.')
        return redirect('email_pazarlama')

    return render(request, 'backend/yonetim/sayfalar/pazarlama_yonetimi/e_posta_pazarlama.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kampanyalar(request):
    context = {}

    tum_kampanyalar = Campaign.objects.all()

    kampanya_name = request.GET.get("kampanya_adi", '')
    query = f"?kampanya_adi={kampanya_name}"

    if kampanya_name:
        tum_kampanyalar = tum_kampanyalar.filter(Q(name__icontains=kampanya_name))

    p = Paginator(tum_kampanyalar, 30)
    page = request.GET.get('page')
    kampanya = p.get_page(page)

    form = CampaingForm(data=request.POST or None, files=request.FILES or None)
    context.update({
        'form': form,
        'kampanya': kampanya,
        'query': query,
    })

    if 'addForm' in request.POST:
        if form.is_valid():
            data = form.save(commit=False)

            is_publish = request.POST.get('is_publish')

            if is_publish == 'on':
                is_publish = True
            else:
                is_publish = False

            data.is_publish = is_publish
            data.save()

            messages.success(request, 'Kampanya başarıyla oluşturuldu.')
            return redirect('kampanyalar')

    return render(request, 'backend/yonetim/sayfalar/kampanya_yonetimi/kampanyalar.html', context)


def kampanya_publish(request, id):
    kampanya = get_object_or_404(Campaign, id=id)

    if kampanya.is_publish == True:
        kampanya.is_publish = False
        messages.info(request, f'{kampanya.name} kampanyası yayından kaldırıldı!')
    else:
        kampanya.is_publish = True
        messages.info(request, f'{kampanya.name} kampanyası yayına alındı!')
    kampanya.save()

    return redirect('kampanyalar')


def kampanya_export_excel(request):
    columns = ['Kampanya Adı', 'İndirim Oranı', 'Başlangıç Tarihi', 'Bitiş Tarihi', 'is_publish']

    rows = Campaign.objects.all().values_list('name', 'discountrate', 'start_date', 'end_date', 'is_publish')
    return exportExcel('Harcamalar', 'Kampanyalar', columns=columns, rows=rows)


@login_required(login_url="/yonetim/giris-yap/")
def kampanya_hepsini_sil(request):
    context = {}
    kampanya = Campaign.objects.all().delete()
    messages.success(request, 'Tüm harcamalar silindi.')
    return redirect("kampanyalar")


@login_required(login_url="/yonetim/giris-yap/")
def kampanya_secilileri_sil(request):
    kampanya_id = request.GET.getlist('kampanya[]')

    Campaign.objects.filter(id__in=kampanya_id).delete()
    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def kampanya_urun_ekle(request, slug):
    context = {}
    kampanya = get_object_or_404(Campaign, slug=slug)
    categories = SubBottomCategory.objects.filter(maincategory_id=1)
    products = Product.objects.filter(is_publish=True)

    kategori = request.GET.get('kategori', '')
    urun_adi = request.GET.get('baslik', '')

    if kategori:
        products = products.filter(subbottomcategory_id=kategori)

    if urun_adi:
        products = products.filter(Q(title__icontains=urun_adi))

    query = f"?kategori={kategori}&urun_adi={urun_adi}"

    indirim_orani = 1 - (kampanya.discountrate / 100)

    p = Paginator(products, 30)
    page = request.GET.get('page')
    product = p.get_page(page)

    context.update({
        'kampanya': kampanya,
        'categories': categories,
        'products': product,
        'indirim_orani': indirim_orani,
        'query': query
    })
    return render(request, 'backend/yonetim/sayfalar/kampanya_yonetimi/urun_ekle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kampanya_urun_sec(request, kampanya_id):
    product_id = request.GET.get('product_id')
    kampanya = get_object_or_404(Campaign, id=kampanya_id)
    product = Product.objects.get(id=product_id)
    product.is_discountprice = True
    product.discountprice = float(product.price) * (1 - (kampanya.discountrate / 100))
    product.save()
    CampaingProduct.objects.create(campaign=kampanya, product=product)
    return JsonResponse(data='success', safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def kampanya_urun_kaldir(request, kampanya_id):
    product_id = request.GET.get('product_id')
    kampanya = get_object_or_404(Campaign, id=kampanya_id)
    products = Product.objects.get(id=product_id)

    products.is_discountprice = False
    products.discountprice = 0.0
    products.save()
    CampaingProduct.objects.get(campaign=kampanya, product=products).delete()
    return JsonResponse(data='success', safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def kampanya_secili_urunler(request, kampanya_id):
    context = {}

    kampanya = get_object_or_404(Campaign, id=kampanya_id)
    products = CampaingProduct.objects.filter(campaign=kampanya)

    p = Paginator(products, 30)
    page = request.GET.get('page')
    product = p.get_page(page)

    context.update({
        'kampanya': kampanya,
        'products': product
    })
    return render(request, 'backend/yonetim/sayfalar/kampanya_yonetimi/secili_urunler.html', context)


def kampanya_secili_urunler_excel(request, kampanya_id):
    columns = ['Ürün Adı', 'Barkod', 'Stok Kodu', 'Model Kodu', 'Stok', 'Renk', 'Beden', 'Fiyat', 'Kampanyalı Fiyat']

    rows = CampaingProduct.objects.filter(campaign_id=kampanya_id).values_list('product__title', 'product__barcode',
                                                                               'product__stock_code',
                                                                               'product__model_code',
                                                                               'product__quantity',
                                                                               'product__color__name',
                                                                               'product__size__name', 'product__price',
                                                                               'product__discountprice')
    return exportExcel('Kampanya Ürünleri', 'Kampanya', columns=columns, rows=rows)


@login_required(login_url="/yonetim/giris-yap/")
def bildirimler(request):
    context = {}
    tum_bildirimler = Notification.objects.all()

    p = Paginator(tum_bildirimler, 30)
    page = request.GET.get('page')
    bildirimler = p.get_page(page)

    context.update({
        'bildirimler': bildirimler,
    })

    return render(request, "backend/yonetim/sayfalar/bildirimler.html", context)


@login_required(login_url="/yonetim/giris-yap/")
def tum_bildirimleri_okundu_olarak_isaretle(request):
    bildirimler = Notification.objects.all()
    for b in bildirimler:
        b.is_read = True
        b.save()
    data = "success"
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def tum_bildirimleri_sil(request):
    bildirimler = Notification.objects.all().delete()
    messages.info(request, 'Tüm bildirimler silindi.')
    return redirect('bildirimler')


@login_required(login_url="/yonetim/giris-yap/")
def bildirim_sil(request, id):
    bildirim = get_object_or_404(Notification, id=id)
    bildirim.delete()
    messages.info(request, 'İlgili bildirim silindi.')
    return redirect('bildirimler')


@login_required(login_url="/yonetim/giris-yap/")
def bildirim_goruntule(request, id):
    context = {}
    bildirim = get_object_or_404(Notification, id=id)

    context.update({
        'bildirim': bildirim,
    })

    return render(request, "backend/yonetim/sayfalar/bildirim_oku.html", context)


def refresh_bildirim(request):
    exists_notification = Notification.objects.filter(is_read=False).exists()

    notification_list = []

    notification = Notification.objects.filter(is_read=False)

    for n in notification:
        notification_list.append({
            'id': n.id,
            'n_type': n.noti_type,
            'title': n.title,
            'passing_time': n.passing_time(),
        })

    data = [exists_notification, notification_list]

    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def blog_kategori(request):
    context = {}
    kategoriler = BlogCategory.objects.all()

    kategori_adi = request.GET.get('kategori_adi', '')

    if kategori_adi:
        kategoriler = kategoriler.filter(Q(name__icontains=kategori_adi))

    form = BlogCategoryForm(data=request.POST or None, files=request.FILES or None)
    context.update({
        'kategoriler': kategoriler,
        'form': form,
    })

    if 'addBtn' in request.POST:
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            messages.success(request, 'Kategori başarıyla eklendi.')
            return redirect('blog_kategori')
        else:
            messages.warning(request, 'Bir hata meydana geldi.')
            return redirect('blog_kategori')

    return render(request, 'backend/yonetim/sayfalar/blog_yonetimi/kategoriler.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def blog_kategori_guncelle(request, id):
    context = {}
    category = BlogCategory.objects.get(id=id)
    form = BlogCategoryForm(instance=category, data=request.POST or None, files=request.FILES or None)
    context.update({
        'category': category,
        'form': form,
    })

    if 'updateBtn' in request.POST:
        if form.is_valid():
            form.save()
            messages.info(request, 'Kategori güncellendi.')
            return redirect("blog_kategori_guncelle", id)

    return render(request, 'backend/yonetim/sayfalar/blog_yonetimi/kategori_guncelle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def blog_kategori_sil(request, id):
    context = {}
    category = BlogCategory.objects.get(id=id)
    category.delete()
    messages.info(request, "İlgili kategori silindi.")
    return redirect("blog_kategori")


def blog_kategori_export_excel(request):
    columns = ['ID', 'Başlık', 'Oluşturan Kullanıcı', 'Oluşturulma Tarihi']

    rows = BlogCategory.objects.all().values_list('id', 'name', 'user__email', 'created_at')
    return exportExcel('BlogKategori', 'BlogKategori', columns=columns, rows=rows)


@login_required(login_url="/yonetim/giris-yap/")
def blog_kategori_hepsini_sil(request):
    context = {}
    category = BlogCategory.objects.all().delete()
    messages.info(request, 'Blog kategorileri silindi.')
    return redirect("blog_kategori")


@login_required(login_url="/yonetim/giris-yap/")
def blog_kategori_secilileri_sil(request):
    categoy_id = request.GET.getlist('category[]')

    BlogCategory.objects.filter(id__in=categoy_id).delete()
    data = 'success'
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def blog_yazilari(request):
    context = {}
    blog_yazilari = Blog.objects.all()
    kategoriler = BlogCategory.objects.all()

    blog_baslik = request.GET.get('blog_baslik', '')
    kategori_id = request.GET.get('kategori', '')
    publish_status = request.GET.get('publish_status', '')

    if blog_yazilari:
        blog_yazilari = blog_yazilari.filter(Q(title__icontains=blog_baslik))

    if kategori_id:
        blog_yazilari = blog_yazilari.filter(category_id=kategori_id)

    if publish_status:
        if publish_status == True:
            blog_yazilari = blog_yazilari.filter(is_publish=True)
        else:
            blog_yazilari = blog_yazilari.filter(is_publish=False)

    context.update({
        'blog_yazilari': blog_yazilari,
        'kategoriler': kategoriler,
    })

    return render(request, 'backend/yonetim/sayfalar/blog_yonetimi/blog_yazilari.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def blog_ekle(request):
    context = {}
    form = BlogForm(data=request.POST or None, files=request.FILES or None)
    context.update({
        'form': form,
    })

    if 'addBtn' in request.POST:
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            tags = request.POST.get('inputtags', '')
            data.save()

            if tags:
                for tag in tags.split(","):
                    BlogKeywords.objects.create(blog=data, name=tag)

            messages.success(request, 'Blog başarıyla eklendi')
            return redirect('blog_yazilari')

    return render(request, 'backend/yonetim/sayfalar/blog_yonetimi/blog_ekle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def hepsiburada_siparis_ekle(request):
    hepsiburada = Hepsiburada.objects.all().last()
    h_order_number = request.POST.get("h_order_number", '')
    h_pocket_number = request.POST.get("h_pocket_number", '')
    h_buyer = request.POST.get("h_buyer", '')
    h_title = request.POST.get("h_title", '')
    h_barcode = request.POST.get("h_barcode", '')
    h_stock_code = request.POST.get("h_stock_code", '')
    h_color = request.POST.get("h_color", '')
    h_size = request.POST.get("h_size", '')
    h_quantity = request.POST.get("h_quantity", '')
    h_unit_price = request.POST.get("h_unit_price", '')
    h_sales_price = request.POST.get("h_sales_price", '')
    h_discount_price = request.POST.get("h_discount_price", '')
    h_city = request.POST.get("h_city", '')
    h_order_date = request.POST.get("h_order_date", '')
    h_status = request.POST.get("h_status", '')

    count = 0

    if h_order_number:
        count += 1

    if h_pocket_number:
        count += 1

    if h_title:
        count += 1

    if h_barcode:
        count += 1

    if h_stock_code:
        count += 1

    if h_color:
        count += 1

    if h_size:
        count += 1

    if h_unit_price:
        count += 1

    if h_sales_price:
        count += 1

    if h_discount_price:
        count += 1

    if h_city:
        count += 1

    if h_order_date:
        count += 1

    if h_status:
        count += 1

    if h_quantity:
        count += 1

    if h_buyer:
        count += 1

    if count == 15:
        HepsiburadaSiparisler.objects.create(order_number=h_order_number, packet_number=h_pocket_number, buyer=h_buyer,
                                             quantity=h_quantity, title=h_title, barcode=h_barcode, color=h_color,
                                             size=h_size, stock_code=h_stock_code, unit_price=h_unit_price,
                                             sales_amount=h_sales_price, discount_amount=h_discount_price,
                                             shippment_city=h_city, order_date=h_order_date,
                                             service_price=hepsiburada.hizmet_bedeli,
                                             process_price=hepsiburada.islem_bedeli, status=h_status)
        data = "success"
    else:
        data = "error"
    return JsonResponse(data=data, safe=False)


@login_required(login_url="/yonetim/giris-yap/")
def hepsiburada_order_detail(request, id):
    context = {}

    order = get_object_or_404(HepsiburadaSiparisler, id=id)

    order_products = HepsiburadaMoreProductOrder.objects.filter(order_number=order.order_number,
                                                                packet_number=order.packet_number)
    harcamalar = Harcamalar.objects.filter(siparis_numarasi=order.order_number)

    context.update({
        'order': order,
        'order_products': order_products,
        'harcamalar': harcamalar
    })

    if 'addHepsiburadaCost' in request.POST:
        delivery_price = request.POST.get('delivery_price', 0.0)
        commission_price = request.POST.get('commission_price', 0.0)
        service_price = request.POST.get('service_price', 0.0)
        process_price = request.POST.get('process_price', 0.0)

        order.delivery_price = delivery_price
        order.commission_price = commission_price
        order.service_price = service_price
        order.process_price = process_price
        order.save()
        messages.success(request, 'Sipariş güncellendi.')
        return redirect('hepsiburada_order_detail', id)

    if 'returnStatusBtn' in request.POST:
        is_return = request.POST.get('is_return')

        if is_return == None or is_return == "None":
            order.is_return = False
        else:
            order.is_return = True
            created_at = datetime.now()
            for harcama in Harcamalar.objects.filter(siparis_numarasi=order.order_number):
                Harcamalar.objects.create(siparis_numarasi=order.order_number, harcama_adi=harcama.harcama_adi,
                                          harcama_tutari=harcama.harcama_tutari, harcama_notu=harcama.harcama_notu,
                                          harcama_tipi="Ürün Alımı", durum="İade Yapıldı", created_at=created_at)
        order.save()
        messages.success(request, 'Sipariş iade edildi.')
        return redirect('hepsiburada_order_detail', id)

    return render(request, 'backend/yonetim/sayfalar/siparis_yonetimi/hepsiburada_siparis_detaylari.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def change_order_status(request):
    platform = request.POST.get("platform")
    siparis_no = request.POST.get("siparis_no")
    status = request.POST.get("status")
    if platform == "trendyol":
        trendyol = get_object_or_404(TrendyolOrders, order_number=siparis_no)
        trendyol.status = status
        trendyol.save()

    if platform == "hepsiburada":
        hepsiburada = get_object_or_404(HepsiburadaSiparisler, order_number=siparis_no)
        hepsiburada.status = status
        hepsiburada.save()
    data = "success"
    return JsonResponse(data=data, safe=False)
