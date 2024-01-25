import datetime
from datetime import timedelta, timezone
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from carts.models import Cart
from customer.models import CustomerAddress
from product.models import *
from user_accounts.models import User


# Create your models here.

class PreOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_number = models.CharField(verbose_name="Sipariş Numarası", null=True, blank=False, max_length=255)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    coupon = models.FloatField(null=True, blank=True)
    bonuses = models.FloatField(verbose_name="Verdiği Bonus", blank=True, null=True)
    cart_total = models.FloatField(null=True, blank=True)
    delivery_price = models.CharField(max_length=100, verbose_name="Kargo Ücreti", null=True, blank=True)
    address = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Sipariş Adresi")
    preliminary_information_form = RichTextUploadingField(verbose_name='Ön Bilgilendirme Formu', null=True, blank=True)
    distance_selling_contract = RichTextUploadingField(verbose_name='Mesafeli Satış Sözleşmesi', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")


class Order(models.Model):

    STATUS = (
        ('Yeni', 'Yeni'),
        ('Onaylandı', 'Onaylandı'),
        ('Hazırlanıyor', 'Hazırlanıyor'),
        ('Kargolandı', 'Kargolandı'),
        ('Tamamlandı', 'Tamamlandı'),
        ('İptal Edildi', 'İptal Edildi'),
        ('Ödeme Yapılmadı', 'Ödeme Yapılmadı'),
    )

    PAYMENT_TYPE = (
        ('Banka/Kredi Kartı', 'Banka/Kredi Kartı'),
        ('Havale/EFT', 'Havale/EFT'),
    )

    PLATFORM = (
        ("TredyShop","TredyShop"),
        ("Trendyol","Trendyol"),
        ("Hepsiburada","Hepsiburada"),
        ("PTTAvm","PTTAvm"),
        ("N11","N11"),
        ("Çiçeksepeti","Çiçeksepeti"),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Müşteri")
    order_platform = models.CharField(choices=PLATFORM, null=True, blank=True, default="TredyShop", max_length=100, verbose_name="Sipariş Verilen Platform")
    order_number = models.CharField(max_length=20, verbose_name="Sipariş Numarası", blank=True, null=True)
    address = models.ForeignKey(CustomerAddress, on_delete=models.SET_NULL, blank=False, null=True, verbose_name="Adres")
    order_amount = models.FloatField(verbose_name="Sipariş Tutarı", null=True)
    order_total = models.FloatField(verbose_name="Ödenen Tutar", null=True)
    delivery_name = models.CharField(max_length=255, verbose_name="Kargo Şirketi", null=True, blank=True)
    delivery_price = models.CharField(max_length=100, verbose_name="Kargo Ücreti", null=True, blank=True)
    delivery_track = models.CharField(max_length=255, verbose_name="Takip Kodu", null=True, blank=True)
    track_link = models.CharField(max_length=500, verbose_name="Takip Linki", null=True, blank=True)
    paymenttype = models.CharField(choices=PAYMENT_TYPE, max_length=30, null=True, verbose_name="Ödeme Tipi")
    cardholder = models.CharField(max_length=255, blank=True, null=True, verbose_name="Kart Sahibi")
    cardnumber = models.CharField(max_length=20, blank=True, null=True, verbose_name="Kart Numarası")
    status = models.CharField(max_length=50, choices=STATUS, null=True, default="Yeni", verbose_name="Sipariş Durumu")
    coupon_name = models.CharField(verbose_name="Kullanılan Kupon Adı", max_length=255, blank=True, null=True)
    used_coupon = models.FloatField(verbose_name="Kullanılan Kupon", blank=True, null=True)
    bill = models.FileField(upload_to='documents/bill/', null=True, verbose_name="Fatura Yükle")
    preliminary_information_form = RichTextUploadingField(verbose_name='Ön Bilgilendirme Formu', null=True, blank=True)
    distance_selling_contract = RichTextUploadingField(verbose_name='Mesafeli Satış Sözleşmesi', null=True, blank=True)
    ip = models.CharField(max_length=50, blank=False, verbose_name="İp Adresi")
    is_installment = models.BooleanField(default=False, verbose_name="Taksitli Mi?", null=True, blank=False)
    installment = models.IntegerField(default=0, verbose_name="Taksit Sayısı", null=True, blank=True)
    is_ordered = models.BooleanField(default=False, verbose_name="Sipariş Verildi Mi?")
    bonuses = models.FloatField(verbose_name="Verdiği Bonus", blank=True, null=True)
    approved_contract = models.BooleanField(default=False, verbose_name="Sözleşme Onayı")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    def __str__(self):
        return str(self.order_number)

    class Meta:
        verbose_name = "1. Siparişler"
        verbose_name_plural = "1. Siparişler"
        ordering = ['-created_at']

    def delivered_time(self):
        return self.created_at + timedelta(days=1)

    def get_bill(self):
        if self.bill:
            return self.bill.url

    def returnPeriodRequirementTime(self):
        bugun = datetime.now(timezone.utc)
        gecen_sure = bugun - self.created_at
        result = False
        if gecen_sure.days <= 2:
            result = True
        return result

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Sipariş")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Müşteri")
    product = models.ForeignKey(ApiProduct, on_delete=models.CASCADE, null=True, blank=False, verbose_name="Ürün")
    title = models.CharField(verbose_name="Ürün Başlığı", null=True, max_length=500)
    product_slug = models.CharField(verbose_name="Ürün Slug", null=True, max_length=500)
    color = models.CharField(max_length=50, verbose_name="Renk")
    size = models.CharField(max_length=50, verbose_name="Boyut")
    quantity = models.IntegerField(verbose_name="Miktar")
    product_price = models.FloatField(verbose_name="Ürün Fiyatı")
    forward_sale = models.FloatField(verbose_name="Vadeli Satış Fiyatı (KDV Dahil)", null=True, blank=True)
    coupon_name = models.CharField(verbose_name="Kullanılan Kupon Adı", max_length=255, blank=True, null=True)
    used_coupon = models.FloatField(verbose_name="Kullanılan Kupon", blank=True, null=True)
    ordered = models.BooleanField(default=False, verbose_name="Sipariş Verildi Mi?")
    is_cancelling = models.BooleanField(default=False, verbose_name="İptal Talebi Var Mı?")
    is_extradation = models.BooleanField(default=False, verbose_name="İade Talebi Var Mı?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    def __str__(self):
        return str(self.product.title)

    class Meta:
        verbose_name = "2. Ürün Siparişleri"
        verbose_name_plural = "2. Ürün Siparişleri"


class BankInfo(models.Model):
    name = models.CharField(max_length=255, verbose_name="Banka Adı", null=True, blank=False)
    branch = models.CharField(max_length=255, verbose_name="Banka Şubesi", null=True, blank=False)
    image = models.ImageField(blank=True, upload_to="img/order/bank/", verbose_name="Banka Logusu")
    iban = models.CharField(max_length=20, verbose_name="IBAN", null=True, blank=False)
    account_no = models.CharField(max_length=155, verbose_name="Hesap Numarası", null=True, blank=False)
    account_holder = models.CharField(max_length=100, verbose_name="Hesap Sahibi", null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "3. Banka Bilgileri"
        verbose_name_plural = "3. Banka Bilgileri"


class ExtraditionRequest(models.Model):

    TYPE = (
        ("Arızalı geldi","Arızalı geldi"),
        ("Hasarlı geldi","Hasarlı geldi"),
        ("Farklı ürün geldi","Farklı ürün geldi"),
        ("Bedeni bana uygun değil","Bedeni bana uygun değil"),
        ("Almaktan vazgeçtim","Almaktan vazgeçtim"),
        ("Hatalı sipariş geldi","Hatalı sipariş geldi"),
        ("Diğer","Diğer"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Müşteri")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Sipariş", null=True)
    product = models.ForeignKey(ApiProduct, on_delete=models.CASCADE, null=True, blank=False, verbose_name="Ürün")
    extradition_type = models.CharField(choices=TYPE, max_length=255, verbose_name="İade Nedeni", null=True)
    description = models.TextField(verbose_name="Açıklama", help_text="İade talebeinizin daha hızlı sonuçlanması için açıklama yazabilirsiniz.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi", null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi", null=True)

    class Meta:
        ordering = ['-created_at']


class ExtraditionRequestResult(models.Model):
    TYPE = (
        ("Kabul Edili", "Kabul Edili"),
        ("Red", "Red"),
    )

    extraditionrequest = models.ForeignKey(ExtraditionRequest, on_delete=models.CASCADE, verbose_name="Sipariş", null=True)
    typ = models.CharField(choices=TYPE, max_length=255, verbose_name="İade Sonucu", null=True)
    description = models.TextField(verbose_name="Açıklama", max_length=2000, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi", null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi", null=True)


class CancellationRequest(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Sipariş", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Müşteri", null=True)
    product = models.ForeignKey(ApiProduct, on_delete=models.CASCADE, null=True, blank=False, verbose_name="Ürün")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi", null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi",null=True)

    class Meta:
        ordering = ['-created_at']


class BINList(models.Model):
    bank_code = models.CharField(verbose_name="Banka Kodu", null=True, blank=True, max_length=10)
    bank_name = models.CharField(verbose_name="Banka Adı", null=True, blank=True, max_length=255)
    bin_code = models.BigIntegerField(verbose_name="BIN Numarası", null=True, blank=True)
    card_type = models.CharField(verbose_name="Kart Tipi", null=True, blank=True, max_length=50)
    businesscard = models.BooleanField(default=False, verbose_name="Ticari Kart")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi", null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi", null=True)

    class Meta:
        ordering = ['-bank_code']