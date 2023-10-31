from django.db import models

# Create your models here.

class TrendyolFirstCategory(models.Model):
    id = models.BigIntegerField(verbose_name="ID", primary_key=True)
    name = models.CharField(max_length=120, verbose_name="Kategori Adı")
    parentId = models.BigIntegerField(null=True, blank=True)
    is_subcategory = models.BooleanField(default=False)

    class Meta:
        verbose_name = "1) Trendyol 1. Kategori"
        verbose_name_plural = "1) Trendyol 1. Kategori"
        ordering = ['id']

    def __str__(self):
        return f"{self.name}"

class TrendyolSecondCategory(models.Model):
    id = models.BigIntegerField(verbose_name="ID", primary_key=True)
    name = models.CharField(max_length=120, verbose_name="Kategori Adı")
    parentId = models.BigIntegerField(null=True, blank=True)
    is_subcategory = models.BooleanField(default=False)

    class Meta:
        verbose_name = "2) Trendyol 2. Kategori"
        verbose_name_plural = "2) Trendyol 2. Kategori"
        ordering = ['id']

    def __str__(self):
        return f"{self.name}"


class TrendyolThirdCategory(models.Model):
    id = models.BigIntegerField(verbose_name="ID", primary_key=True)
    name = models.CharField(max_length=120, verbose_name="Kategori Adı")
    parentId = models.BigIntegerField(null=True, blank=True)
    is_subcategory = models.BooleanField(default=False)

    class Meta:
        verbose_name = "3) Trendyol 3. Kategori"
        verbose_name_plural = "3) Trendyol 3. Kategori"
        ordering = ['id']

    def __str__(self):
        return f"{self.name}"

class TrendyolFourCategory(models.Model):
    id = models.BigIntegerField(verbose_name="ID", primary_key=True)
    name = models.CharField(max_length=120, verbose_name="Kategori Adı")
    parentId = models.BigIntegerField(null=True, blank=True)
    is_subcategory = models.BooleanField(default=False)

    class Meta:
        verbose_name = "4) Trendyol 4. Kategori"
        verbose_name_plural = "4) Trendyol 4. Kategori"
        ordering = ['id']

    def __str__(self):
        return f"{self.name}"


class TrendyolFiveCategory(models.Model):
    id = models.BigIntegerField(verbose_name="ID", primary_key=True)
    name = models.CharField(max_length=120, verbose_name="Kategori Adı")
    parentId = models.BigIntegerField(null=True, blank=True)
    is_subcategory = models.BooleanField(default=False)

    class Meta:
        verbose_name = "5) Trendyol 5. Kategori"
        verbose_name_plural = "5) Trendyol 5. Kategori"
        ordering = ['id']

    def __str__(self):
        return f"{self.name}"

class TrendyolSixCategory(models.Model):
    id = models.BigIntegerField(verbose_name="ID", primary_key=True)
    name = models.CharField(max_length=120, verbose_name="Kategori Adı")
    parentId = models.BigIntegerField(null=True, blank=True)
    is_subcategory = models.BooleanField(default=False)

    class Meta:
        verbose_name = "6) Trendyol 6. Kategori"
        verbose_name_plural = "6) Trendyol 6. Kategori"
        ordering = ['id']

    def __str__(self):
        return f"{self.name}"


class TrendyolBrand(models.Model):
    id = models.BigIntegerField(verbose_name="ID", primary_key=True)
    name = models.CharField(max_length=120, verbose_name="Kategori Adı")

    class Meta:
        verbose_name = "7) Trendyol Markalar"
        verbose_name_plural = "7) Trendyol Markalar"
        ordering = ['id']

    def __str__(self):
        return f"{self.name}"


class TrendyolOrders(models.Model):
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
    order_date = models.DateTimeField(auto_now_add=False, verbose_name="Sipariş Tarihi")

    class Meta:
        verbose_name = "Trendyol Siparişler"
        verbose_name_plural = "Trendyol Siparişler"
        ordering = ['-order_number']

    def __str__(self):
        return f"{self.order_number}"



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