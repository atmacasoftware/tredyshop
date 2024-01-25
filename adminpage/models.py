from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.template import defaultfilters
from django_ckeditor_5.fields import CKEditor5Field
from django_resized import ResizedImageField
from unidecode import unidecode

from categorymodel.models import MainCategory, SubBottomCategory
from orders.models import Order
from product.models import ApiProduct, Question
from trendyol.models import TrendyolOrders
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
    hizmet_bedeli = models.FloatField(verbose_name="Hizmet Bedeli", null=True, blank=True)

    class Meta:
        verbose_name = "1) Trendyol Hesap Bilgileri"
        verbose_name_plural = "1) Trendyol Hesap Bilgileri"


class Hepsiburada(models.Model):
    companyname = models.CharField(max_length=255, verbose_name="Firma Adı", null=True, blank=True)
    kep = models.CharField(max_length=255, verbose_name="KEP Adresi", null=True, blank=True)
    username = models.CharField(max_length=255, verbose_name="Kullanıcı Adı", null=True, blank=True)
    password = models.CharField(max_length=255, verbose_name="Şifre", null=True, blank=True)
    merchantID = models.CharField(max_length=255, verbose_name="Merchant ID", null=True, blank=True)
    token = models.CharField(max_length=255, verbose_name="Token", null=True, blank=True)
    firstbarem = models.FloatField(verbose_name="Barem 1. Aralık Maksimum Değeri", null=True)
    secondbarem = models.FloatField(verbose_name="Barem 2. Aralık Maksimum Değeri", null=True)
    hizmet_bedeli = models.FloatField(verbose_name="Hizmet Bedeli", null=True, blank=True)
    islem_bedeli = models.FloatField(verbose_name="İşlem Bedeli", null=True, blank=True)

    class Meta:
        verbose_name = "Hepsiburada Hesap Bilgileri"
        verbose_name_plural = "Hepsiburada Hesap Bilgileri"


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

    TYPE = (
        ("Satış", "Satış"),
        ("Genel İade", "Genel İade"),
        ("Tevkifat", "Tevkifat"),
        ("Tevkifat İade", "Tevkifat İade"),
        ("İstisna", "İstisna"),
        ("Özel Matrah", "Özel Matrah"),
        ("İhraç Kayıtlı", "İhraç Kayıtlı"),
        ("Konaklama Vergisi", "Konaklama Vergisi"),
    )

    bill_type = models.CharField(choices=TYPE, default="Satış", verbose_name="Fatura Tipi", null=True, blank=False,
                                 max_length=100)
    bill_number = models.CharField(verbose_name="Fatura Numarası", max_length=255, null=True, blank=False)
    name = models.CharField(verbose_name="Ad/Soyad/Ünvan", max_length=500, null=True)
    tax_number = models.BigIntegerField(verbose_name="Vergi Numarası", null=True)
    tax_administration = models.CharField(max_length=255, verbose_name="Vergi Dairesi", null=True, blank=True)
    price = models.FloatField(verbose_name="KDV Hariç Fiyat", null=True, blank=False)
    tax_rate = models.IntegerField(verbose_name="KDV Oranı", null=True, blank=False)
    tax_amount = models.FloatField(verbose_name="KDV Tutarı", null=True, blank=True)
    price_amount = models.FloatField(verbose_name="Toplam Tutar", null=True, blank=True)
    year = models.CharField(max_length=10, choices=YEAR, null=True, default="2023", verbose_name="Düzenlenme Yılı")
    month = models.CharField(max_length=10, choices=MONTH, null=True, default="1", verbose_name="Düzenleme Ayı")
    file = models.FileField(upload_to="adminpage/kesilen_fatular/", verbose_name="Fatura", null=True, blank=True)
    edited_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Fatura Düzenlenme Tarihi",
                                   null=True)
    is_cancelling = models.BooleanField(default=False, verbose_name="İptal Edildi Mi?", null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "2) Kesilen Faturalar"
        verbose_name_plural = "2) Kesilen Faturalar"
        ordering = ['-created_at']

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

    TYPE = (
        ("Satış", "Satış"),
        ("Genel İade", "Genel İade"),
        ("Tevkifat", "Tevkifat"),
        ("Tevkifat İade", "Tevkifat İade"),
        ("İstisna", "İstisna"),
        ("Özel Matrah", "Özel Matrah"),
        ("İhraç Kayıtlı", "İhraç Kayıtlı"),
        ("Konaklama Vergisi", "Konaklama Vergisi"),
    )

    bill_type = models.CharField(choices=TYPE, default="Satış", verbose_name="Fatura Tipi", null=True, blank=False,
                                 max_length=100)
    bill_number = models.CharField(verbose_name="Fatura Numarası", max_length=255, null=True, blank=False)
    price = models.FloatField(verbose_name="KDV Hariç Fiyat", null=True, blank=False)
    tax_rate = models.IntegerField(verbose_name="KDV Oranı", null=True, blank=False)
    tax_amount = models.FloatField(verbose_name="KDV Tutarı", null=True, blank=True)
    price_amount = models.FloatField(verbose_name="Toplam Tutar", null=True, blank=True)
    year = models.CharField(max_length=10, choices=YEAR, null=True, default="2023", verbose_name="Düzenlenme Yılı")
    month = models.CharField(max_length=10, choices=MONTH, null=True, default="1", verbose_name="Düzenleme Ayı")
    file = models.FileField(upload_to="adminpage/kesilen_fatular/", verbose_name="Fatura", null=True, blank=True)
    is_cancelling = models.BooleanField(default=False, verbose_name="İptal Edildi Mi?", null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "3) Alınan Faturalar"
        verbose_name_plural = "3) Alınan Faturalar"
        ordering = ['-created_at']


class Notification(models.Model):
    TYPE = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
    )

    # 1: Ürünler pazaryerlerine yüklendi.
    # 2: XML güncellemesi yapıldı.
    # 3: Pazaryeri stok-fiyat güncellemesi yapıldı.
    # 4: Yeni sipariş alındı.
    # 5: Ürün sorusu soruldu.
    # 6: Ürün iade talebi geldi.
    # 7: Ürün yorumu yapıldı.
    # 8: Yeni müşteri kaydı.
    # 9: Görev ataması

    noti_type = models.CharField(choices=TYPE, max_length=20, verbose_name="Bildirim Tipi")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kullanıcı",
                             related_name="noti_user")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Müşteri",
                                 related_name="noti_customer")
    trendyol_orders = models.ForeignKey(TrendyolOrders, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Trendyol Siparişi")
    tredyshop_orders = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tredyshop Siparişi")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Soru")
    task_id = models.BigIntegerField(verbose_name="Task ID", blank=True, null=True)
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
            passing = f"{pass_time.days} gn."

        elif pass_time.days < 1:
            if pass_time.seconds / 60 < 60:
                passing = f"{math.floor(pass_time.seconds / 60)} dk."
            elif pass_time.seconds / 60 > 59:
                passing = f"{math.floor(pass_time.seconds / 3600)} sa."
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
    trendyol_url = models.CharField(max_length=255, verbose_name="Trendyol Mağaza Adresi", null=True)
    hepsiburada_url = models.CharField(max_length=255, verbose_name="Hepsiburada Mağaza Adresi", null=True)
    pttavm_url = models.CharField(max_length=255, verbose_name="PTTAvm Mağaza Adresi", null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")


class Campaign(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kampanya Adı", null=True)
    description = models.TextField(verbose_name="Açıklama", null=True, blank=True, max_length=1000)
    discountrate = models.PositiveIntegerField(default=0, verbose_name="İndirim Oranı")
    image = models.FileField(upload_to='adminpage/campaign', verbose_name="Kampanya Resmi", null=True, blank=True)
    start_date = models.DateField(verbose_name="Başlangıç Tarihi", null=True, blank=True)
    end_date = models.DateField(verbose_name="Bitiş Tarihi", null=True, blank=True)
    is_publish = models.BooleanField(default=False, verbose_name="Yayında mı?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    class Meta:
        ordering = ["created_at"]

    def urun_sayisi(self):
        urunler = CampaingProduct.objects.filter(campaign=self)
        return urunler.count()

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(unidecode(self.name))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = Campaign.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except Campaign.DoesNotExist:
                    self.slug = slug
                    break
        super(Campaign, self).save(*args, **kwargs)

class CampaingProduct(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="campaing_products")
    product = models.ForeignKey(ApiProduct, on_delete=models.CASCADE, null=True, verbose_name="Kampanya Ürünü")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

class Banner(models.Model):
    TYPE = (
        ("Belirli Tutar Altı", "Belirli Tutar Altı"),
        ("İndirimli Ürünler", "İndirimli Ürünler"),
        ("Kategori Bazlı Ürünler", "Kategori Bazlı Ürünler"),
        ("Kampanya Bazlı Ürünler", "Kampanya Bazlı Ürünler"),
    )

    banner_type = models.CharField(max_length=100, choices=TYPE, verbose_name="Tip", null=True, blank=False)
    banner_title = models.CharField(max_length=255, verbose_name="Banner Başlık", null=True, blank=False)
    banner_maxprice = models.IntegerField(verbose_name="En Yüksek Fiyat", null=True, blank=True)
    banner_discountrate = models.IntegerField(null=True, verbose_name="İndirim Oranı", blank=True)
    banner_category = models.ForeignKey(SubBottomCategory, on_delete=models.CASCADE, max_length=255, verbose_name="Kategori Seçiniz", null=True, blank=True)
    image = ResizedImageField(force_format="WEBP", quality=50, upload_to="adminpage/banner", null=True, blank=True)
    is_publish = models.BooleanField(default=False, verbose_name="Yayında Mı?")
    order = models.PositiveIntegerField(null=True, blank=False, verbose_name="Sıra Sayısı")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    viewd_count = models.BigIntegerField(default=0, null=True, blank=True, verbose_name="Görüntülenme Sayısı")
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    class Meta:
        ordering = ["created_at"]

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(unidecode(self.banner_title))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = Banner.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except Banner.DoesNotExist:
                    self.slug = slug
                    break
        super(Banner, self).save(*args, **kwargs)


class Harcamalar(models.Model):
    TYPE = (
        ("Ürün Alımı", "Ürün Alımı"),
        ("KDV Ödemesi", "KDV Ödemesi"),
        ("Gelir Geçici Vergi Ödemesi", "Gelir Geçici Vergi Ödemesi"),
        ("Reklam Harcaması", "Reklam Harcaması"),
        ("Diğer Harcamalar", "Diğer Harcamalar")
    )

    STATUS = (
        ("Ödeme Yapıldı", "Ödeme Yapıldı"),
        ("İptal Edildi", "İptal Edildi"),
        ("İade Yapıldı", "İade Yapıldı"),
    )

    siparis_numarasi = models.CharField(null=True, blank=True, max_length=155, verbose_name="Sipariş Numarası")
    harcama_tipi = models.CharField(choices=TYPE, null=True, blank=False, max_length=100, verbose_name="Harcama Tipi")
    harcama_adi = models.CharField(max_length=300, verbose_name="Harcama Adı", null=True)
    harcama_tutari = models.FloatField(verbose_name="Harcama Tutarı", null=True)
    harcama_notu = models.TextField(null=True, blank=True, verbose_name="Not")
    durum = models.CharField(choices=STATUS, null=True, blank=False, verbose_name="Ödeme Durumu",
                             default="Ödeme Yapıldı", max_length=50)
    created_at = models.DateField(verbose_name="Harcama Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Harcamalar"
        verbose_name_plural = "Harcamalar"
        ordering = ['-created_at']

    def __str__(self):
        return str(self.harcama_adi)


class UpdateHistory(models.Model):
    TYPE = (
        ("Modaymış Yeni Ürün Ekleme", "Modaymış Yeni Ürün Ekleme"),
        ("Modaymış Güncelleme", "Modaymış Güncelleme"),
        ("Modaymış Aktif Olmayan Ürün", "Modaymış Aktif Olmayan Ürün"),
        ("Tahtakale Güncelleme", "Tahtakale Güncelleme"),
        ("Trendyol Stok&Fiyat Güncelleme", "Trendyol Stok&Fiyat Güncelleme"),
        ("XML Dünyası Yeni Ürün Ekleme", "XML Dünyası Yeni Ürün Ekleme"),
        ("XML Dünyası Güncelleme", "XML Dünyası Güncelleme"),
        ("XML Dünyası Aktif Olmayan Ürün", "XML Dünyası Aktif Olmayan Ürün"),
        ("XML Dünyası Diğer Ürün Ekleme", "XML Dünyası Diğer Ürün Ekleme"),
        ("XML Dünyası Ürün Diğer", "XML Dünyası Ürün Diğer"),
    )
    history_type = models.CharField(choices=TYPE, max_length=100, null=True, verbose_name="Geçmiş Tipi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        ordering = ['-created_at']


class Izinler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    ana_slider = models.BooleanField(default=False, verbose_name="Ana Slayt Ekranı")
    kategori_gorme = models.BooleanField(default=False, verbose_name="Kategoleri Görme")
    kategori_duzenleme = models.BooleanField(default=False, verbose_name="Kategori Düzenleme")
    urun_ekleme = models.BooleanField(default=False, verbose_name="Ürün Ekleme")
    urun_duzeneleme = models.BooleanField(default=False, verbose_name="Ürün Düzenleme")
    kampanyali_urunler = models.BooleanField(default=False, verbose_name="Kampanyalı Ürün İşlemleri")
    urun_ozellik_islemleri = models.BooleanField(default=False, verbose_name="Ürün Özellik İşlemleri")
    tredyshop_siparisleri = models.BooleanField(default=False, verbose_name="TredyShop Sipariş İşlemleri")
    trendyol_siparisleri = models.BooleanField(default=False, verbose_name="Trendyol Sipariş İşlemleri")
    xml_islemleri = models.BooleanField(default=False, verbose_name="XML Yönetimi İşlemleri")
    kullanici_ekleme = models.BooleanField(default=False, verbose_name="Kullanıcı Ekleme İşlemi")
    kullanici_silme = models.BooleanField(default=False, verbose_name="Kullanıcı Silme İşlemi")
    kullanici_duzenleme = models.BooleanField(default=False, verbose_name="Kullanıcı Düzenleme İşlemi")
    kullanici_yetkilendirme = models.BooleanField(default=False, verbose_name="Kullanıcı Yetkilendirme İşlemi")
    anasayfa_islemleri = models.BooleanField(default=False, verbose_name="Anasayfa İşlemleri")
    hakkimizda_islemleri = models.BooleanField(default=False, verbose_name="Hakkımızda Sayfası İşlemleri")
    trendyol_hesap_bilgileri = models.BooleanField(default=False, verbose_name="Trendyol Hesap Bilgileri")
    trendyol_urun_girisi = models.BooleanField(default=False, verbose_name="Trendyol Ürün Girişi")
    trendyol_stok_fiyat_guncelleme = models.BooleanField(default=False, verbose_name="Trendyol Stok & Fiyat Güncelleme")
    trendyol_bilgi_guncelleme = models.BooleanField(default=False, verbose_name="Trendyol Bilgi Güncelleme")
    trendyol_urun_silme = models.BooleanField(default=False, verbose_name="Trendyol Ürün Silme")
    trendyol_urunleri = models.BooleanField(default=False, verbose_name="Trendyol Ürünlerine Erişim")
    trendyol_siparis_ekle = models.BooleanField(default=False, verbose_name="Trendyol Sipariş Ekleme")
    trendyol_istek_cevaplari = models.BooleanField(default=False, verbose_name="Trendyol İstek Cevapları")
    kesilen_fatura = models.BooleanField(default=False, verbose_name="Kesilen Fatura İşlemleri")
    alinan_fatura = models.BooleanField(default=False, verbose_name="Alınan Fatura İşlemleri")
    harcamalar = models.BooleanField(default=False, verbose_name="Harcama İşlemleri")
    gecmis_kayitlar = models.BooleanField(default=False, verbose_name="Geçmiş Kayıt İşlemleri")
    istatistikler = models.BooleanField(default=False, verbose_name="İstatistiki Bilgilere Erişim")
    aksyionlar = models.BooleanField(default=False, verbose_name="Aksiyonlara Erişim")
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi", null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi", null=True)

    class Meta:
        verbose_name = "İzinler"
        verbose_name_plural = "İzinler"

    def __str__(self):
        return str(self.user.first_name) + str(self.user.last_name)

class TredyShopFiyatAyarla(models.Model):
    kdv1 = models.FloatField(verbose_name="KDV Oranı 1", blank=False, null=True)
    kdv2 = models.FloatField(verbose_name="KDV Oranı 2", blank=False, null=True)
    commission = models.FloatField(verbose_name="Sanal POS Komisyon Oranı", blank=False, null=True)
    kargo = models.FloatField(verbose_name="Kargo Maliyeti (KDV Dahil)", null=True, blank=False)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    update_at = models.DateField(auto_now=True, verbose_name="Güncellenme Tarihi")


class TredyShopKarMarji(models.Model):
    tredyshop = models.ForeignKey(TredyShopFiyatAyarla, on_delete=models.CASCADE, null=True, blank=False)
    baslangic = models.FloatField(verbose_name="Başlangıç Fiyatı", null=True, blank=False)
    bitis = models.FloatField(verbose_name="Bitiş Fiyatı", null=True, blank=False)
    kar_maji = models.FloatField(verbose_name="Kar Marjı", null=True, blank=False)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi", null=True)
    update_at = models.DateField(auto_now=True, verbose_name="Güncellenme Tarihi", null=True)

class TrendyolFiyatAyarla(models.Model):
    kdv1 = models.FloatField(verbose_name="KDV Oranı 1", blank=False, null=True)
    kdv2 = models.FloatField(verbose_name="KDV Oranı 2", blank=False, null=True)
    commission = models.FloatField(verbose_name="Trendyol Komisyonu", blank=False, null=True)
    service = models.FloatField(verbose_name="Hizmet Bedeli (KDV Dahil)", blank=False, null=True)
    kargo = models.FloatField(verbose_name="Kargo Maliyeti (KDV Dahil)", null=True, blank=False)
    indirim = models.FloatField(verbose_name="İndirim Tutarı", null=True, blank=False)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    update_at = models.DateField(auto_now=True, verbose_name="Güncellenme Tarihi")


class TrendyolKarMarji(models.Model):
    trendyol = models.ForeignKey(TrendyolFiyatAyarla, on_delete=models.CASCADE, null=True, blank=False)
    baslangic = models.FloatField(verbose_name="Başlangıç Fiyatı", null=True, blank=False)
    bitis = models.FloatField(verbose_name="Bitiş Fiyatı", null=True, blank=False)
    kar_maji = models.FloatField(verbose_name="Kar Marjı", null=True, blank=False)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi", null=True)
    update_at = models.DateField(auto_now=True, verbose_name="Güncellenme Tarihi", null=True)

class HepsiburadaFiyatAyarla(models.Model):
    kdv1 = models.FloatField(verbose_name="KDV Oranı 1", blank=False, null=True)
    kdv2 = models.FloatField(verbose_name="KDV Oranı 2", blank=False, null=True)
    commission = models.FloatField(verbose_name="Hepsiburada Komisyonu", blank=False, null=True)
    service = models.FloatField(verbose_name="Hizmet Bedeli (KDV Dahil)", blank=False, null=True)
    process = models.FloatField(verbose_name="İşlem Bedeli (KDV Dahil)", blank=False, null=True)
    kargo = models.FloatField(verbose_name="Kargo Maliyeti (KDV Dahil)", null=True, blank=False)
    indirim = models.FloatField(verbose_name="İndirim Tutarı", null=True, blank=False)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    update_at = models.DateField(auto_now=True, verbose_name="Güncellenme Tarihi")

class HepsiburadaKarMarji(models.Model):
    hepsiburada = models.ForeignKey(HepsiburadaFiyatAyarla, on_delete=models.CASCADE, null=True, blank=False)
    baslangic = models.FloatField(verbose_name="Başlangıç Fiyatı", null=True, blank=False)
    bitis = models.FloatField(verbose_name="Bitiş Fiyatı", null=True, blank=False)
    kar_maji = models.FloatField(verbose_name="Kar Marjı", null=True, blank=False)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi", null=True)
    update_at = models.DateField(auto_now=True, verbose_name="Güncellenme Tarihi", null=True)

class AmazonFiyatAyarla(models.Model):
    kdv1 = models.FloatField(verbose_name="KDV Oranı 1", blank=False, null=True)
    kdv2 = models.FloatField(verbose_name="KDV Oranı 2", blank=False, null=True)
    commission = models.FloatField(verbose_name="Amazon Komisyonu", blank=False, null=True)
    service = models.FloatField(verbose_name="Hizmet Bedeli (KDV Dahil)", blank=False, null=True)
    kargo = models.FloatField(verbose_name="Kargo Maliyeti (KDV Dahil)", null=True, blank=False)
    indirim = models.FloatField(verbose_name="İndirim Tutarı", null=True, blank=False)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    update_at = models.DateField(auto_now=True, verbose_name="Güncellenme Tarihi")

class AmazonKarMarji(models.Model):
    amazon = models.ForeignKey(AmazonFiyatAyarla, on_delete=models.CASCADE, null=True, blank=False)
    baslangic = models.FloatField(verbose_name="Başlangıç Fiyatı", null=True, blank=False)
    bitis = models.FloatField(verbose_name="Bitiş Fiyatı", null=True, blank=False)
    kar_maji = models.FloatField(verbose_name="Kar Marjı", null=True, blank=False)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi", null=True)
    update_at = models.DateField(auto_now=True, verbose_name="Güncellenme Tarihi", null=True)

class PttAvmFiyatAyarla(models.Model):
    kdv1 = models.FloatField(verbose_name="KDV Oranı 1", blank=False, null=True)
    kdv2 = models.FloatField(verbose_name="KDV Oranı 2", blank=False, null=True)
    commission = models.FloatField(verbose_name="PTT Avm Komisyonu", blank=False, null=True)
    service = models.FloatField(verbose_name="Hizmet Bedeli (KDV Dahil)", blank=False, null=True)
    kargo = models.FloatField(verbose_name="Kargo Maliyeti (KDV Dahil)", null=True, blank=False)
    indirim = models.FloatField(verbose_name="İndirim Tutarı", null=True, blank=False)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    update_at = models.DateField(auto_now=True, verbose_name="Güncellenme Tarihi")

class PttAvmKarMarji(models.Model):
    pttavm = models.ForeignKey(PttAvmFiyatAyarla, on_delete=models.CASCADE, null=True, blank=False)
    baslangic = models.FloatField(verbose_name="Başlangıç Fiyatı", null=True, blank=False)
    bitis = models.FloatField(verbose_name="Bitiş Fiyatı", null=True, blank=False)
    kar_maji = models.FloatField(verbose_name="Kar Marjı", null=True, blank=False)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi", null=True)
    update_at = models.DateField(auto_now=True, verbose_name="Güncellenme Tarihi", null=True)


class ProductSellStatistic(models.Model):
    name = models.CharField(max_length=255, verbose_name="Ürün Adı", null=True)
    barcode = models.CharField(max_length=255, verbose_name="Ürün Barkodu", unique=True, null=True)
    image_url = models.CharField(max_length=500, verbose_name="Ürün Linki", null=True, blank=True)
    sell_count = models.BigIntegerField(default=0, verbose_name="Toplam Satış Sayısı", null=True, blank=True)
    satis = models.FloatField(default=0.0, verbose_name="Satış Fiyatı", blank=True)
    maliyet = models.FloatField(default=0.0, verbose_name="Maliyet Fiyatı", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    def __str__(self):
        return str(self.name)

    def satisOrani(self):
        maliyet = 0.0
        if self.maliyet != None:
            maliyet = self.maliyet
        tumu = self.satis + maliyet
        oran = 0
        if tumu != 0:
            oran = 100 * self.satis / tumu
        return oran

    def maliyetOrani(self):
        maliyet = 0
        if self.maliyet != None:
            maliyet = self.maliyet
        tumu = self.satis + maliyet
        oran = 0
        if tumu != 0:
            oran = 100 * maliyet / tumu
        return oran

class SiteSetting(models.Model):
    title = models.CharField(max_length=255, verbose_name="Başlık", blank=True, null=True)
    free_shipping = models.BigIntegerField(verbose_name="Ücretsiz Kargo Tutarı", null=True, blank=True)
    shipping_company = models.CharField(max_length=100, verbose_name="Kargo Firması", null=True, blank=True)
    shipping_price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Kargo Ücreti", null=True,
                                         blank=True)
    keywords = models.CharField(max_length=255, verbose_name="Anahtar Kelime", blank=True, null=True)
    description = models.CharField(max_length=255, verbose_name="Açıklama", null=True, blank=True)
    company = models.CharField(max_length=255, verbose_name="Şirket Adı", null=True, blank=True)
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name="Şirket Adresi")
    phone = models.CharField(blank=True, null=True, max_length=15, verbose_name="Telefon Numarası")
    fax = models.CharField(blank=True, max_length=15, verbose_name="Fax")
    email = models.CharField(blank=True, max_length=255, verbose_name="Email")
    vkn = models.CharField(blank=True, max_length=50, verbose_name="Vergi Kimlik Numarası")
    mersis = models.CharField(blank=True, max_length=100, verbose_name="Mersis Numarası")
    logo = models.ImageField(blank=True, upload_to="img/logo/", verbose_name="Site Logosu")
    favicon = models.ImageField(blank=True, upload_to="img/favicon/", verbose_name="Site Faviconu")
    facebook = models.CharField(max_length=255, null=True, blank=True, verbose_name="Facebook")
    instagram = models.CharField(max_length=255, null=True, blank=True, verbose_name="İnstagram")
    twitter = models.CharField(max_length=255, null=True, blank=True, verbose_name="Twitter")
    youtube = models.CharField(max_length=255, null=True, blank=True, verbose_name="Youtube")
    tiktok = models.CharField(max_length=255, null=True, blank=True, verbose_name="Tiktok")
    linkedin = models.CharField(max_length=255, null=True, blank=True, verbose_name="Linkedin")
    whatsapp = models.CharField(max_length=255, null=True, blank=True, verbose_name="Whatsapp")
    google_analytics = models.TextField(max_length=255, null=True, blank=True, verbose_name="Google Analytics Kodu")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Task(models.Model):

    TASK_TIME = (
        ("Her Gün","Her Gün"),
        ("Belirli Gün","Belirli Gün"),
    )

    name = models.CharField(max_length=500, null=True, blank=True, verbose_name="Görev Adı")
    task_time = models.CharField(choices=TASK_TIME, max_length=500, null=True, blank=True, verbose_name="Görev Zamanı")
    task_date = models.DateField(null=True, blank=True, verbose_name="Görev Zamanı")
    detail = RichTextUploadingField(null=True, blank=True, verbose_name="Görev Açıklaması")
    is_completed = models.BooleanField(default=False, verbose_name="Tamamlandı Mı")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-create_at"]

    def get_users(self):
        return UserTask.objects.filter(task=self)

class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False, verbose_name="Kullanıcı")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=False, verbose_name="Görev")
    all_completed = models.BooleanField(default=False, verbose_name="Hepsi Tamamladı Mı?")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
