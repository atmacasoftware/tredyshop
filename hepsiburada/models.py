from django.db import models

# Create your models here.

class HepsiburadaSiparisler(models.Model):

    STATUS = (
        ('Yeni', 'Yeni'),
        ('Onaylandı', 'Onaylandı'),
        ('Hazırlanıyor', 'Hazırlanıyor'),
        ('Kargolandı', 'Kargolandı'),
        ('Tamamlandı', 'Tamamlandı'),
        ('İptal Edildi', 'İptal Edildi'),
        ('İade Edildi', 'İade Edildi'),
        ('Ödeme Yapılmadı', 'Ödeme Yapılmadı'),
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


class HepsiburadaKomisyonlar(models.Model):
    kategori_adi = models.CharField(verbose_name="Kategori Adı", null=True, blank=False, max_length=255)
    komisyon_tutari = models.FloatField(verbose_name="Komisyon Tutarı", null=True, blank=False)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Trendyol Komisyon Tutarları"
        verbose_name_plural = "Trendyol Komisyon Tutarları"
        ordering = ['kategori_adi']

    def __str__(self):
        return self.kategori_adi

class LogRecords(models.Model):
    TYPE = (
        ('1','Ürün Yükleme'),
        ('2','Stok&Fiyat Güncelleme'),
        ('3','Bilgi Güncelleme'),
        ('4','Ürün Silme'),
    )
    log_type = models.CharField(choices=TYPE, max_length=50, verbose_name="Log Tipi")
    batch_id = models.CharField(max_length=255, verbose_name="Batch Request ID", null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_at']
