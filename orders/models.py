from datetime import timedelta

from django.db import models

from customer.models import CustomerAddress
from product.models import Product, Variants
from user_accounts.models import User


# Create your models here.

class Order(models.Model):

    STATUS = (
        ('Yeni', 'Yeni'),
        ('Onaylandı', 'Onaylandı'),
        ('Hazırlanıyor', 'Hazırlanıyor'),
        ('Kargolandı', 'Kargolandı'),
        ('Tamamlandı', 'Tamamlandı'),
        ('İptal Edildi', 'İptal Edildi')
    )

    PAYMENT_TYPE = (
        ('Banka/Kredi Kartı', 'Banka/Kredi Kartı'),
        ('Havale/EFT', 'Havale/EFT'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Müşteri")
    order_number = models.CharField(max_length=20, verbose_name="Sipariş Numarası", blank=True, null=True)
    address = models.ForeignKey(CustomerAddress, on_delete=models.SET_NULL, blank=False, null=True, verbose_name="Adres")
    order_total = models.FloatField(verbose_name="Sipariş Toplamı")
    paymenttype = models.CharField(choices=PAYMENT_TYPE, max_length=30, null=True)
    cardholder = models.CharField(max_length=255, blank=False, null=True, verbose_name="Kart Sahibi")
    cardnumber = models.CharField(max_length=20, blank=False, null=True, verbose_name="Kart Numarası")
    status = models.CharField(max_length=50, choices=STATUS, null=True, default="Yeni", verbose_name="Sipariş Durumu")
    used_coupon = models.FloatField(verbose_name="Kullanılan Kupon" ,blank=True, null=True)
    ip = models.CharField(max_length=50, blank=False, verbose_name="İp Adresi")
    is_ordered = models.BooleanField(default=False, verbose_name="Sipariş Verildi Mi?")
    bonuses = models.FloatField(verbose_name="Verdiği Bonu", blank=True, null=True)
    approved_contract = models.BooleanField(default=False, verbose_name="Sözleşme Onayı")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "1. Siparişler"
        verbose_name_plural = "1. Siparişler"

    def delivered_time(self):
        return self.created_at + timedelta(days=1)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Sipariş")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Müşteri")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=False, verbose_name="Ürün")
    variation = models.ForeignKey(Variants, on_delete=models.CASCADE, verbose_name="Ürün Çeşidi", blank=True, null=True)
    color = models.CharField(max_length=50, verbose_name="Renk")
    size = models.CharField(max_length=50, verbose_name="Boyut")
    quantity = models.IntegerField(verbose_name="Miktar")
    product_price = models.FloatField(verbose_name="Ürün Fiyatı")
    ordered = models.BooleanField(default=False, verbose_name="Sipariş Verildi Mi?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    def __str__(self):
        return str(self.product.title)

    class Meta:
        verbose_name = "2. Ürün Siparişleri"
        verbose_name_plural = "2. Ürün Siparişleri"

class BankInfo(models.Model):
    name = models.CharField(max_length=255, verbose_name="Banka Adı", null=True, blank=False)
    image = models.ImageField(blank=True, upload_to="img/order/bank/", verbose_name="Banka Logusu")
    ıban = models.CharField(max_length=20, verbose_name="IBAN", null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    def __str__(self):
        return str(self.product.title)

    class Meta:
        verbose_name = "3. Banka Bilgileri"
        verbose_name_plural = "3. Banka Bilgileri"

