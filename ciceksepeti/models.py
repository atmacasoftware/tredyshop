from django.db import models

from product.models import ApiProduct


# Create your models here.

class Ciceksepeti(models.Model):
    companyname = models.CharField(max_length=255, verbose_name="Firma Adı", null=True, blank=True)
    kep = models.CharField(max_length=255, verbose_name="KEP Adresi", null=True, blank=True)
    apikey = models.CharField(max_length=255, verbose_name="Api Key", null=True, blank=True)
    saticiid = models.BigIntegerField(verbose_name="Satıcı ID (Cari ID)", null=True, blank=True)
    token = models.CharField(max_length=255, verbose_name="Token", null=True, blank=True)
    listeleme_bedeli = models.FloatField(verbose_name="Listeleme Bedeli", null=True, blank=True)

    class Meta:
        verbose_name = "1) Çiçeksepeti Hesap Bilgileri"
        verbose_name_plural = "1) Çiçeksepeti Hesap Bilgileri"


class CiceksepetiUrunler(models.Model):
    product = models.ForeignKey(ApiProduct, on_delete=models.CASCADE, verbose_name="Ürün")
    ciceksepeti_kategori_id = models.BigIntegerField(verbose_name="Çiceksepeti Kategori ID", null=True)
    yayin_durumu = models.BooleanField(default=False, verbose_name="Yayın Durumu")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '2) Çiçeksepeti Ürünler'
        verbose_name_plural = '2) Çiçeksepeti Ürünler'

    def __str__(self):
        return str(self.product.title)


class CiceksepetiOrders(models.Model):

    STATUS = (
        ('Yeni', 'Yeni'),
        ('Onaylandı', 'Onaylandı'),
        ('Hazırlanıyor', 'Hazırlanıyor'),
        ('Kargolandı', 'Kargolandı'),
        ('Tamamlandı', 'Tamamlandı'),
        ('İptal Edildi', 'İptal Edildi'),
        ('İade Edildi', 'İade Edildi'),
        ('Ödeme Yapılmadı', 'Ödeme Yapılmadı'),
        ('Birden Fazla', 'Birden Fazla'),
    )

    order_number = models.CharField(max_length=255, verbose_name="Sipariş Numarası", null=True, blank=False)
    packet_number = models.CharField(max_length=255, verbose_name="Paket Numarası", null=True, blank=False)
    buyer = models.CharField(max_length=255, verbose_name="Alıcı", null=True, blank=False)
    quantity = models.BigIntegerField(null=True, verbose_name="Adet")
    title = models.CharField(verbose_name="Ürün Adı", max_length=500, null=True)
    barcode = models.CharField(verbose_name="Barkod", max_length=100, null=True)
    color = models.CharField(verbose_name="Renk", max_length=100, null=True, blank=True)
    size = models.CharField(verbose_name="Beden", max_length=100, null=True, blank=True)
    stock_code = models.CharField(verbose_name="Stok Kodu", max_length=100, null=True, blank=True)
    unit_price = models.FloatField(verbose_name="Birim Fiyat", null=True, blank=False)
    sales_amount = models.FloatField(verbose_name="Satış Tutarı", null=True, blank=False)
    discount_amount = models.FloatField(verbose_name="İndirim Tutarı", null=True, blank=True)
    shippment_city = models.CharField(verbose_name="Teslimat Şehri", null=True, blank=True, max_length=255)
    delivery_price = models.FloatField(verbose_name="Kargo Bedeli (KDV Dahil)", null=True, blank=True)
    commission_price = models.FloatField(verbose_name="Komisyon Tutarı", null=True, blank=True)
    service_price = models.FloatField(verbose_name="Hizmet Bedeli", null=True, blank=True)
    tax_price = models.FloatField(verbose_name="Vergi Tutarı", null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=False, verbose_name="Sipariş Tarihi")
    is_return = models.BooleanField(default=False, null=True, verbose_name="İade Edildi Mi?")
    status = models.CharField(choices=STATUS, verbose_name="Durum", null=True, max_length=255)

    class Meta:
        verbose_name = "Trendyol Siparişler"
        verbose_name_plural = "Trendyol Siparişler"
        ordering = ['-order_date']

    def __str__(self):
        return f"{self.order_number}"