from django.db import models
from product.models import Product, ProductVariant


# Create your models here.

class TrendyolOrders(models.Model):

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


class TrendyolMoreProductOrder(models.Model):
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
    quantity = models.BigIntegerField(null=True, verbose_name="Adet")
    title = models.CharField(verbose_name="Ürün Adı", max_length=500, null=True)
    barcode = models.CharField(verbose_name="Barkod", max_length=100, null=True)
    color = models.CharField(verbose_name="Renk", max_length=100, null=True, blank=True)
    size = models.CharField(verbose_name="Beden", max_length=100, null=True, blank=True)
    stock_code = models.CharField(verbose_name="Stok Kodu", max_length=100, null=True, blank=True)
    unit_price = models.FloatField(verbose_name="Birim Fiyat", null=True, blank=False)
    sales_amount = models.FloatField(verbose_name="Satış Tutarı", null=True, blank=False)
    discount_amount = models.FloatField(verbose_name="İndirim Tutarı", null=True, blank=True)
    status = models.CharField(choices=STATUS, verbose_name="Durum", null=True, max_length=255)

    class Meta:
        ordering = ['-title']

    def __str__(self):
        return f"{self.order_number}"


class TrendyolCommission(models.Model):
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

class TrendyolProduct(models.Model):
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, verbose_name="Trendyol Ürün")
    is_publish = models.BooleanField(default=False, verbose_name="Yayında Mı?")
    category = models.CharField(max_length=255, verbose_name="Trendyol Kategori", null=True, blank=True)
    category_id = models.BigIntegerField(verbose_name="Kategori ID", null=True, blank=True)
    is_ready = models.BooleanField(default=False, verbose_name="Hazır mı?", null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Trendyol Ürünler"
        verbose_name_plural = "Trendyol Ürünler"

    def __str__(self):
        return f"{str(self.product.title)}"

    def get_attributes(self, attributeId, allowcustom):
        try:
            attributes = TrendyolAttributes.objects.get(trendyol_product=self, code=attributeId)
            if allowcustom == False:
                return int(attributes.value)
            else:
                return attributes.value
        except:
            return None

    def save(self, *args, **kwargs):
        if self.product.is_publish_trendyol == True:
            self.is_publish = True
        super(TrendyolProduct, self).save(*args, **kwargs)

class TrendyolAttributes(models.Model):
    trendyol_product = models.ForeignKey(TrendyolProduct, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Özellik Adı", null=True, blank=True)
    code = models.CharField(verbose_name="Özellik ID", null=True, blank=True, max_length=255)
    value = models.CharField(verbose_name="Özellik Değeri", null=True, blank=True, max_length=255)
    customStatus = models.BooleanField(default=False, verbose_name="Custom", null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Trendyol Ürün Özellikleri"
        verbose_name_plural = "Trendyol Ürün Özellikleri"

    def __str__(self):
        return f"{str(self.trendyol_product.product.title)} - {self.name}"

class TrendyolReport(models.Model):
    name = models.CharField(max_length=255, verbose_name="Rapor Adı", null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Trendyol Rapor"
        verbose_name_plural = "Trendyol Rapor"

    def __str__(self):
        return f"{str(self.name)}"

    def get_sending_product(self):
        return TrendyolReportProduct.objects.filter(report=self)

class TrendyolReportProduct(models.Model):
    report = models.ForeignKey(TrendyolReport, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Ürünler")
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Trendyol Rapor Ürünler"
        verbose_name_plural = "Trendyol Rapor Ürünler"

    def __str__(self):
        return f"{str(self.product.product.title)}"


