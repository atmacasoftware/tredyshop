from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from categorymodel.models import MainCategory
from user_accounts.models import User


# Create your models here.

class Trendyol(models.Model):
    companyname = models.CharField(max_length=255, verbose_name="Firma Adı", null=True, blank=True)
    kep = models.CharField(max_length=255, verbose_name="KEP Adresi", null=True, blank=True)
    apikey = models.CharField(max_length=255, verbose_name="Api Key", null=True, blank=True)
    apisecret = models.CharField(max_length=255, verbose_name="Api Secret", null=True, blank=True)
    saticiid = models.BigIntegerField(verbose_name="Satıcı ID (Cari ID)", null=True, blank=True)
    token = models.CharField(max_length=255, verbose_name="Token", null=True, blank=True)
    sevkiyatadresid_1 = models.BigIntegerField(null=True, blank=True, verbose_name="Sevkiyat Adres ID 1")
    sevkiyatadresid_2 = models.BigIntegerField(null=True, blank=True, verbose_name="Sevkiyat Adres ID 2")
    sevkiyatadresid_3 = models.BigIntegerField(null=True, blank=True, verbose_name="Sevkiyat Adres ID 3")
    sevkiyatadresid_4 = models.BigIntegerField(null=True, blank=True, verbose_name="Sevkiyat Adres ID 4")
    sevkiyatadresid_5 = models.BigIntegerField(null=True, blank=True, verbose_name="Sevkiyat Adres ID 5")
    iadeadresid_1 = models.BigIntegerField(null=True, blank=True, verbose_name="İade Adres ID 1")
    iadeadresid_2 = models.BigIntegerField(null=True, blank=True, verbose_name="İade Adres ID 2")
    iadeadresid_3 = models.BigIntegerField(null=True, blank=True, verbose_name="İade Adres ID 3")
    iadeadresid_4 = models.BigIntegerField(null=True, blank=True, verbose_name="İade Adres ID 4")
    iadeadresid_5 = models.BigIntegerField(null=True, blank=True, verbose_name="İade Adres ID 5")
    firstbarem = models.FloatField(verbose_name="Barem 1. Aralık Maksimum Değeri", null=True)
    secondbarem = models.FloatField(verbose_name="Barem 2. Aralık Maksimum Değeri", null=True)
    class Meta:
        verbose_name = "1) Trendyol Hesap Bilgileri"
        verbose_name_plural = "1) Trendyol Hesap Bilgileri"



class IssuedInvoices(models.Model):

    YEAR = (
        ("2023", "2023"),
        ("2024", "2024"),
        ("2025", "2025"),
        ("2026", "2026"),
        ("2027", "2027"),
        ("2028", "2028"),
        ("2029", "2029"),
        ("2030", "2030"),
    )

    MONTH = (
        ("1","1"),
        ("2","2"),
        ("3","3"),
        ("4","4"),
        ("5","5"),
        ("6","6"),
        ("7","7"),
        ("8","8"),
        ("9","9"),
        ("10","10"),
        ("11","11"),
        ("12","12"),
    )


    name = models.CharField(verbose_name="Ad/Soyad/Ünvan", max_length=500, null=True)
    tax_number = models.BigIntegerField(verbose_name="Vergi Numarası", null=True)
    tax_administration = models.CharField(max_length=255, verbose_name="Vergi Dairesi", null=True, blank=True)
    price = models.FloatField(verbose_name="KDV Hariç Fiyat", null=True, blank=False)
    tax_rate = models.IntegerField(verbose_name="KVD Oranı", null=True, blank=False)
    year = models.CharField(max_length=10, choices=YEAR, null=True, default="2023", verbose_name="Düzenlenme Yılı")
    month = models.CharField(max_length=10, choices=MONTH, null=True, default="1", verbose_name="Düzenleme Ayı")
    file = models.FileField(upload_to="adminpage/kesilen_fatular/", verbose_name="Fatura", null=True, blank=True)
    edited_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Fatura Düzenlenme Tarihi", null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "2) Kesilen Faturalar"
        verbose_name_plural = "2) Kesilen Faturalar"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.name}"

class InvoicesReceived(models.Model):
    YEAR = (
        ("2023", "2023"),
        ("2024", "2024"),
        ("2025", "2025"),
        ("2026", "2026"),
        ("2027", "2027"),
        ("2028", "2028"),
        ("2029", "2029"),
        ("2030", "2030"),
    )

    MONTH = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
        ("11", "11"),
        ("12", "12"),
    )

    price = models.FloatField(verbose_name="KDV Hariç Fiyat", null=True, blank=False)
    tax_rate = models.IntegerField(verbose_name="KVD Oranı", null=True, blank=False)
    year = models.CharField(max_length=10, choices=YEAR, null=True, default="2023", verbose_name="Düzenlenme Yılı")
    month = models.CharField(max_length=10, choices=MONTH, null=True, default="1", verbose_name="Düzenleme Ayı")
    file = models.FileField(upload_to="adminpage/kesilen_fatular/", verbose_name="Fatura", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "3) Alınan Faturalar"
        verbose_name_plural = "3) Alınan Faturalar"
        ordering = ['created_at']


class Notification(models.Model):
    TYPE = (
        ("1","1"),
        ("2","2"),
        ("3","3"),
        ("4","4"),
        ("5","5"),
        ("6","6"),
        ("7","7"),
        ("8","8"),
    )

    # 1: Ürünler pazaryerlerine yüklendi.
    # 2: XML güncellemesi yapıldı.
    # 3: Pazaryeri stok-fiyat güncellemesi yapıldı.
    # 4: Yeni sipariş alındı.
    # 5: Ürün sorusu soruldu.
    # 6: Ürün iade talebi geldi.
    # 7: Ürün yorumu yapıldı.
    # 8: Yeni müşteri kaydı.

    noti_type = models.CharField(choices=TYPE, max_length=20, verbose_name="Bildirim Tipi")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kullanıcı", related_name="noti_user")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Müşteri", related_name="noti_customer")
    title = models.CharField(max_length=255, verbose_name="Bildirim Başlığı", null=True, blank=False)
    detail = models.TextField(max_length=1000, verbose_name="Bildirim İçeriği", null=True, blank=True)
    is_read = models.BooleanField(default=False, verbose_name="Okundu mu?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "4) Bildirimler"
        verbose_name_plural = "4) Bildirimler"
        ordering = ['-created_at']

    def passing_time(self):
        from datetime import datetime, timezone
        import math
        now = datetime.now(timezone.utc)
        pass_time = now - self.created_at
        passing = None

        if pass_time.days > 0 and pass_time.days < 31:
            passing = f"{pass_time.days} g."

        elif pass_time.days < 1:
            if pass_time.seconds / 60 < 60:
                passing = f"{math.floor(pass_time.seconds / 60)} d."
            elif pass_time.seconds / 60 > 59:
                passing = f"{math.floor(pass_time.seconds / 3600)} s."
        return passing


class Hakkimizda(models.Model):
    title = models.CharField(max_length=255, verbose_name="Başlık", null=True)
    company_info = models.TextField(max_length=5000, verbose_name="Şirket Hakkında", null=True)
    foundation_year = models.CharField(max_length=100, verbose_name="Kuruluş Yılı")
    mission = CKEditor5Field('Misyon', config_name='extends', null=True)
    vision = CKEditor5Field('Vizyon', config_name='extends', null=True)
    category_count = models.BigIntegerField(verbose_name="Kategori Sayısı", null=True)
    categories = models.CharField(max_length=500, verbose_name="Kategoriler", null=True)
    product_count = models.BigIntegerField(verbose_name="Ürün Sayısı", null=True)
    trendyol_url = models.CharField(max_length=255,verbose_name="Trendyol Mağaza Adresi", null=True)
    hepsiburada_url = models.CharField(max_length=255,verbose_name="Hepsiburada Mağaza Adresi", null=True)
    pttavm_url = models.CharField(max_length=255,verbose_name="PTTAvm Mağaza Adresi", null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")