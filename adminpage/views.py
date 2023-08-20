from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from adminpage.forms import *
from categorymodel.models import SubCategory, SubBottomCategory
from product.read_xml import modaymissaveXML2db, updateModaymisSaveXML2db, updateTahtakaleSaveXML2db, \
    tahtakaleSaveXML2db
# Create your views here.
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
import xlwt
from datetime import timedelta, datetime, date

from user_accounts.models import User


def admin_login(request):
    try:
        if request.user.is_authenticated:
            messages.success(request, 'Giriş yapıldı')
            return redirect('mainpage')
        if 'loginBtn' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_obj = User.objects.filter(email=email)
            if not user_obj.exists():
                messages.error(request, 'Bu kullanıcı mevcut değil.')
                return redirect('admin_login')
            user_obj = authenticate(email=email, password=password)
            if user_obj is not None:
                if User.objects.get(email=email, is_superuser=True):
                    auth_login(request, user_obj)
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
    return render(request, 'backend/adminpage/pages/mainpage.html')


@login_required(login_url="/yonetim/giris-yap/")
def products(request):
    return render(request, 'backend/adminpage/pages/products.html')


@login_required(login_url="/yonetim/giris-yap/")
def tahtakale_product(request):
    return render(request, "backend/adminpage/pages/tahtakale.html")


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
        messages.success(request, 'Veriler güncelledi!')
        return redirect("tahtakale_product")
    except:
        return redirect("tahtakale_product")


@login_required(login_url="/yonetim/giris-yap/")
def haydigiy_product(request):
    return render(request, "backend/adminpage/pages/haydigiy.html")


@login_required(login_url="/yonetim/giris-yap/")
def haydigiy_product_load(request):
    try:
        modaymissaveXML2db()()
        messages.success(request, 'Veriler yüklendi!')
        return redirect("haydigiy_product")
    except:
        return redirect("haydigiy_product")


@login_required(login_url="/yonetim/giris-yap/")
def haydigiy_product_update(request):
    try:
        tahtakaleSaveXML2db()
        messages.success(request, 'Veriler güncelledi!')
        return redirect("haydigiy_product")
    except:
        return redirect("haydigiy_product")


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_add_product(request):
    return render(request, 'backend/adminpage/pages/trendyol/urun_girisi.html')


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_add_product_giyim(request):
    return render(request, 'backend/adminpage/pages/trendyol/urun_girisi_giyim.html')


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_add_product_giyim_category1(request, category_no):
    context = {}
    categories = SubBottomCategory.objects.filter(subcategory__category_no=category_no)
    context.update({'categories': categories})
    return render(request, 'backend/adminpage/pages/trendyol/urun_girisi_giyim_category1.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def trendyol_add_product_giyim_send_trendyol(request, id):
    context = {}
    category = SubBottomCategory.objects.get(id=id)
    context.update({'category': category})

    return render(request, 'backend/adminpage/pages/trendyol/urun_girisi_giyim_send_trendyol.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kesilen_fatura_ekle(request):
    context = {}
    form = IssuedInvoicesAddForm(data=request.POST, files=request.FILES)
    context.update({'form': form})
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Fatura başarıyla eklendi!')
            return redirect("kesilen_fatura_ekle")
    return render(request, 'backend/adminpage/pages/kesilen_fatura_ekle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def kesilen_faturalar(request):
    context = {}
    faturalar = IssuedInvoices.objects.all()
    context.update({
        'faturalar': faturalar
    })
    return render(request, 'backend/adminpage/pages/kesilen_faturalar.html', context)


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
    return render(request, 'backend/adminpage/pages/kesilen_fatura_guncelle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def delete_kesilen_fatura(request, id):
    fatura = IssuedInvoices.objects.get(id=id)
    fatura.delete()
    messages.success(request, 'Fatura başarıyla silindi!')
    return redirect('kesilen_faturalar')


def kesilen_faturalar_export_excel(request):
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=kesilen-faturalar-' + str(datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Ödemeler')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Ad/Soyad/Ünvan', 'Vergi Numarası', 'Vergi Dairesi', 'Yıl', 'Ay', 'KDV Hariç Tutar (TL)',
               'KDV Oranı', 'Fatura Düzenlenme Tarihi']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = IssuedInvoices.objects.all().values_list('name', 'tax_number', 'tax_administration', 'year', 'month',
                                                    'price', 'tax_rate', 'edited_date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response


@login_required(login_url="/yonetim/giris-yap/")
def alinan_fatura_ekle(request):
    context = {}
    form = InvoicesReceivedAddForm(data=request.POST, files=request.FILES)
    context.update({'form': form})
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Fatura başarıyla eklendi!')
            return redirect("alinan_fatura_ekle")
    return render(request, 'backend/adminpage/pages/alinan_fatura_ekle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def alinan_faturalar(request):
    context = {}
    faturalar = InvoicesReceived.objects.all()
    context.update({
        'faturalar': faturalar
    })
    return render(request, 'backend/adminpage/pages/alinan_faturalar.html', context)


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
    return render(request, 'backend/adminpage/pages/alinan_fatura_guncelle.html', context)


@login_required(login_url="/yonetim/giris-yap/")
def delete_alinan_fatura(request, id):
    fatura = InvoicesReceived.objects.get(id=id)
    fatura.delete()
    messages.success(request, 'Fatura başarıyla silindi!')
    return redirect('alinan_faturalar')


def alinan_faturalar_export_excel(request):
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=alinan-faturalar-' + str(datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Ödemeler')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Yıl', 'Ay', 'KDV Hariç Tutar (TL)',
               'KDV Oranı', 'Oluşturulma Tarihi']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = InvoicesReceived.objects.all().values_list('year', 'month', 'price', 'tax_rate', 'created_at')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response
