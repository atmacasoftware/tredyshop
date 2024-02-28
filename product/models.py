from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.db import models
from django.db.models import Avg, Count
from django.utils.safestring import mark_safe
from django.urls import reverse
from django_resized import ResizedImageField

from categorymodel.models import MainCategory, SubCategory, SubBottomCategory
from user_accounts.models import User
from django_ckeditor_5.fields import CKEditor5Field
from unidecode import unidecode
from django.template import defaultfilters
from datetime import datetime


# Create your models here.

class Brand(models.Model):
    title = models.CharField(max_length=255, verbose_name="Marka Adı")
    keyword = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    image = models.ImageField(blank=True, upload_to='img/category/', null=True)
    is_active = models.BooleanField(default=True, verbose_name="Yayınlansın mı?")
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "2) Marka"
        verbose_name_plural = "2) Markalar"

    def __str__(self):
        return f"{self.title}"

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Kapak'

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return None

    def get_url(self):
        return reverse('product_by_brands', args=[self.slug])

    def product_count(self):
        return self.brands.count()

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(unidecode(self.title))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = Brand.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except Brand.DoesNotExist:
                    self.slug = slug
                    break
        super(Brand, self).save(*args, **kwargs)


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name="Renk")
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Renk Kodu")

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color: {}">Renk</p>'.format(self.code))
        else:
            return ""

    class Meta:
        verbose_name = "9.1) Renk"
        verbose_name_plural = "9.1) Renkler"


class Size(models.Model):
    name = models.CharField(max_length=50, verbose_name="Boyut")
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Boyut Kodu")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "9.2) Boyut/Kapasite"
        verbose_name_plural = "9.2) Boyut/Kapasite"


class FabricType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Kumaş Tipi")

    def __str__(self):
        return str(self.name)


class Height(models.Model):
    name = models.CharField(max_length=50, verbose_name="Boy")

    def __str__(self):
        return str(self.name)


class Pattern(models.Model):
    name = models.CharField(max_length=50, verbose_name="Kalıp")

    def __str__(self):
        return str(self.name)


class ArmType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Kol Tipi")

    def __str__(self):
        return str(self.name)


class CollerType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Yaka Tipi")

    def __str__(self):
        return str(self.name)


class WeavingType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Dokuma Tipi")

    def __str__(self):
        return str(self.name)


class MaterialType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Materyal")

    def __str__(self):
        return str(self.name)


class EnvironmentType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Ortam")

    def __str__(self):
        return str(self.name)


class LegType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Paça Tipi")

    def __str__(self):
        return str(self.name)


class Pocket(models.Model):
    name = models.CharField(max_length=50, verbose_name="Cep")

    def __str__(self):
        return str(self.name)


class Waist(models.Model):
    name = models.CharField(max_length=50, verbose_name="Bel")

    def __str__(self):
        return str(self.name)


class HeelType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Topuk Tipi")

    def __str__(self):
        return str(self.name)


class HeelSize(models.Model):
    name = models.CharField(max_length=50, verbose_name="Topuk Boyu")

    def __str__(self):
        return str(self.name)


class Sex(models.Model):
    name = models.CharField(max_length=50, verbose_name="Cinsiyet")

    def __str__(self):
        return str(self.name)


class TabletModel(models.Model):
    name = models.CharField(max_length=50, verbose_name="Tablet Modelleri")

    def __str__(self):
        return str(self.name)

class TableCaseType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Kılıf Modeli")

    def __str__(self):
        return str(self.name)

class SleepMode(models.Model):
    name = models.CharField(max_length=50, verbose_name="Uyku Modu")

    def __str__(self):
        return str(self.name)

class BagPattern(models.Model):
    name = models.CharField(max_length=50, verbose_name="Çanta Deseni")

    def __str__(self):
        return str(self.name)


class BijuteriTheme(models.Model):
    name = models.CharField(max_length=50, verbose_name="Tema/Stil")

    def __str__(self):
        return str(self.name)

class ProductKapak(models.Model):
    def product_photo_directory_path(instance, filename):
        return f"products/kapak/{filename}"

    kapak = ResizedImageField(force_format="WEBP", quality=50, upload_to=product_photo_directory_path, null=True,
                              blank=True)
    modal_code = models.CharField(verbose_name="Model Kodu", null=True, blank=False, max_length=150, unique=True)

    def __str__(self):
        return self.modal_code


class ApiProduct(models.Model):
    AGE_GROUP = (
        ("Bebek", "Bebek"),
        ("Bebek&Çocuk", "Bebek&Çocuk"),
        ("Çocuk", "Çocuk"),
        ("Genç", "Genç"),
        ("Yetişkin", "Yetişkin"),
    )

    ACVTIVE_STATUS = (
        ("1", "Evet"),
        ("2", "Hayır"),
    )

    WARRANTY_TYPE = (
        ('Belirtilmemiş','Belirtilmemiş'),
        ('1 Yıl','1 Yıl'),
        ('2 Yıl','2 Yıl'),
        ('3 Yıl','3 Yıl'),
        ('4 Yıl','4 Yıl'),
        ('5 Yıl','5 Yıl'),
        ('6 Ay','6 Ay'),
    )

    COMPATİBLE_BRAND = (
        ("Alcatel Uyumlu","Alcatel Uyumlu"),
        ("Apple Uyumlu","Apple Uyumlu"),
        ("Asus Uyumlu","Asus Uyumlu"),
        ("Casper Uyumlu","Casper Uyumlu"),
        ("General Mobile Uyumlu","General Mobile Uyumlu"),
        ("Honor Uyumlu","Honor Uyumlu"),
        ("Huawei Uyumlu","Huawei Uyumlu"),
        ("Lenovo Uyumlu","Lenovo Uyumlu"),
        ("Oppo Uyumlu","Oppo Uyumlu"),
        ("POCO Uyumlu","POCO Uyumlu"),
        ("Realme Uyumlu","Realme Uyumlu"),
        ("Reeder Uyumlu","Reeder Uyumlu"),
        ("Samsung Uyumlu","Samsung Uyumlu"),
        ("TCL Uyumlu","TCL Uyumlu"),
        ("Xiaomi Uyumlu","Xiaomi Uyumlu"),
    )

    xml_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="XML ID")
    barcode = models.CharField(verbose_name="Barkod", null=True, unique=True, max_length=100)
    model_code = models.CharField(verbose_name="Model Kodu", null=True, blank=True, max_length=100)
    stock_code = models.CharField(verbose_name="Stok Kodu", null=True, blank=True, max_length=100)
    dropshipping = models.CharField(verbose_name="Platform", null=True, blank=True, max_length=255)
    category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, null=True, blank=False,
                                 verbose_name="1. Düzey Kategori", related_name="api_main_category")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=False,
                                    verbose_name="2. Düzey Kategori", related_name="api_sub_category")
    subbottomcategory = models.ForeignKey(SubBottomCategory, on_delete=models.CASCADE, null=True, blank=True,
                                          verbose_name="3. Düzey Kategori", related_name="api_subbottom_category")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Marka",
                              related_name="api_brands")
    trendyol_category_id = models.BigIntegerField(null=True, verbose_name="Trendyol Kategori Numarası", blank=True)
    hepsiburada_category_id = models.BigIntegerField(null=True, verbose_name="Hepsiburada Kategori Numarası",
                                                     blank=True)
    title = models.CharField(max_length=255, verbose_name="Başlık")
    description = models.CharField(max_length=355, verbose_name="Açıklama")
    image_url1 = models.CharField(max_length=500, verbose_name="Resim Link 1", null=True, blank=False)
    image_url2 = models.CharField(max_length=500, verbose_name="Resim Link 2", null=True, blank=True)
    image_url3 = models.CharField(max_length=500, verbose_name="Resim Link 3", null=True, blank=True)
    image_url4 = models.CharField(max_length=500, verbose_name="Resim Link 4", null=True, blank=True)
    image_url5 = models.CharField(max_length=500, verbose_name="Resim Link 5", null=True, blank=True)
    image_url6 = models.CharField(max_length=500, verbose_name="Resim Link 6", null=True, blank=True)
    image_url7 = models.CharField(max_length=500, verbose_name="Resim Link 7", null=True, blank=True)
    image_url8 = models.CharField(max_length=500, verbose_name="Resim Link 8", null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Renk")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Boyut/Beden")
    fabrictype = models.ForeignKey(FabricType, on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name="Kumaş Tipi")
    height = models.ForeignKey(Height, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Boy")
    waist = models.ForeignKey(Waist, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Bel")
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kalıp")
    armtype = models.ForeignKey(ArmType, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kol Tipi")
    collartype = models.ForeignKey(CollerType, on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name="Yaka Tipi")
    weavingtype = models.ForeignKey(WeavingType, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name="Dokuma Tipi")
    material = models.ForeignKey(MaterialType, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Materyal")
    environment = models.ForeignKey(EnvironmentType, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name="Ortam")
    legtype = models.ForeignKey(LegType, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Paça Tipi")
    pocket = models.ForeignKey(Pocket, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Cep")
    heeltype = models.ForeignKey(HeelType, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Topuk Tipi")
    heelsize = models.ForeignKey(HeelSize, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Topuk Boyu")
    price = models.DecimalField(verbose_name="Fiyat", decimal_places=2, max_digits=20)
    quantity = models.BigIntegerField(verbose_name="Miktar", null=True, default=0)
    detail = RichTextUploadingField()
    trendyol_price = models.DecimalField(verbose_name="Trendyol Fiyatı", decimal_places=2, max_digits=20, null=True)
    trendyol_discountprice = models.DecimalField(verbose_name="Trendyol İndirimli Fiyatı", decimal_places=2, max_digits=20, null=True)
    is_trendyol_discountprice = models.BooleanField(default=False, verbose_name="Trendyol İndirim Durumu", null=True, blank=True)
    discountprice = models.DecimalField(verbose_name="İndirimli Fiyat", decimal_places=2, max_digits=20, null=True,
                                        blank=True)
    is_discountprice = models.BooleanField(default=False, verbose_name="İndirimli Yayınla", null=True, blank=True)
    ciceksepeti_price = models.DecimalField(verbose_name="Çiçeksepeti Fiyatı", decimal_places=2, max_digits=20, null=True, blank=True)
    ciceksepeti_discountprice = models.DecimalField(verbose_name="Çiçeksepeti İndirimli Fiyatı", decimal_places=2,
                                                 max_digits=20, null=True)
    is_ciceksepeti_discountprice = models.BooleanField(default=False, verbose_name="Çiçeksepeti İndirim Durumu", null=True,
                                                    blank=True)
    age_group = models.CharField(choices=AGE_GROUP, max_length=50, verbose_name="Yaş Grubu", null=True, blank=True)
    sextype = models.ForeignKey(Sex, verbose_name="Cinsiyet", null=True, blank=True, on_delete=models.CASCADE)
    warranty = models.CharField(choices=WARRANTY_TYPE, default="Belirtilmemiş", null=True, blank=True, verbose_name="Garanti Süresi", max_length=100)
    compatible = models.CharField(choices=COMPATİBLE_BRAND, null=True, blank=True, verbose_name="Uyumlu Marka", max_length=100)
    tabletmodel = models.ForeignKey(TabletModel, on_delete=models.CASCADE, verbose_name="Elektronik Model", null=True, blank=True)
    casetype = models.ForeignKey(TableCaseType, on_delete=models.CASCADE, verbose_name="Kılıf Modeli", null=True, blank=True)
    sleepmode = models.ForeignKey(SleepMode, on_delete=models.CASCADE, verbose_name="Uyku Modu", null=True, blank=True)
    bag_pattern = models.ForeignKey(BagPattern, on_delete=models.CASCADE, verbose_name="Çanta Deseni", null=True, blank=True)
    bijuteri_theme = models.ForeignKey(BijuteriTheme, on_delete=models.CASCADE, verbose_name="Tema/Stil", null=True, blank=True)
    is_publish = models.BooleanField(default=True, verbose_name="Yayında mı?", null=True)
    is_publish_trendyol = models.BooleanField(default=False, verbose_name="Trendyolda Yayında Mı?", null=True)
    is_publish_hepsiburada = models.BooleanField(default=False, verbose_name="Hepsiburadada Yayında Mı?", null=True)
    is_publish_ciceksepeti = models.BooleanField(default=False, verbose_name="Çiçeksepetinde Yayında Mı?", null=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    status = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '1) Ürünler'
        verbose_name_plural = '1) Ürünler'

    def __str__(self):
        return str(self.title)

    def change_float(self):
        return float(self.price)

    def get_data(self):
        category_title = "Yok"
        size_name = "-"
        discountprice = "-"
        satis_durumu = "Hayır"
        if self.subbottomcategory:
            category_title = self.subbottomcategory.title

        if self.size:
            size_name = self.size.name

        if self.discountprice:
            discountprice = self.discountprice

        if self.is_publish:
            satis_durumu = "Evet"

        return {
            'ID': self.id,
            'Başlık': f'<div class="product__info"><div class="product__image"><img src="{self.image_url1}" alt=""></div><div class="product__title"><p><b><a href="{self.get_url()}">{self.title}</a></b></p><span>Stok Kodu: {self.stock_code}</span></div></div>',
            'Barkod': self.barcode,
            'Model Kodu': self.model_code,
            'Platform': self.dropshipping,
            'Kategori': category_title,
            'Marka': self.brand.title,
            'Renk': self.color.name,
            'Beden': size_name,
            'Fiyat (TL)': self.price,
            'İndirimli Fiyat (TL)': discountprice,
            'Stok': self.quantity,
            'Satışta Mı?': satis_durumu,
            'İşlemler': f'<a href="/yonetim/urunler/urun_id={self.id}" class="btn btn-danger btn-sm">Detaya Git</a><div class="dropdown"><button class="btn btn-sm mt-2 btn-secondary dropdown-toggle" type="button"data-toggle="dropdown"aria-expanded="false">İşlemler</button><div class="dropdown-menu"><a class="dropdown-item" href="#">Action</a><a class="dropdown-item" href="#">Another action</a><a class="dropdown-item" href="#">Something else here</a></div></div>'
        }

    def get_url(self):
        return reverse('products_detail', args=[self.slug])

    def get_absolute_url(self):
        return reverse('products_detail', args=[self.slug])

    def favouriteStatus(self, request):
        favourite = self.favorite_product.filter(product=self, customer=request.user)
        status = 'nonfavourite'
        if favourite.count() > 0:
            status = 'favourite'
        return status

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def countQuestion(self):
        question = Question.objects.filter(product=self).aggregate(count=Count('id'))
        count = 0
        if question['count'] is not None:
            count = int(question['count'])
        return count

    def photoReview(self):
        reviews = ReviewRatingImages.objects.all().filter(product=self)
        return reviews

    def one_star(self):
        reviews = ReviewRating.objects.filter(product=self, status=True, rating=1).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None and reviews['count'] != 0:
            count = int(int(reviews['count']) / self.countReview() * 100)
        return count

    def two_star(self):
        reviews = ReviewRating.objects.filter(product=self, status=True, rating=2).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None and reviews['count'] != 0:
            count = int(int(reviews['count']) / self.countReview() * 100)
        return count

    def three_star(self):
        reviews = ReviewRating.objects.filter(product=self, status=True, rating=3).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None and reviews['count'] != 0:
            count = int(int(reviews['count']) / self.countReview() * 100)
        return count

    def four_star(self):
        reviews = ReviewRating.objects.filter(product=self, status=True, rating=4).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None and reviews['count'] != 0:
            count = int(int(reviews['count']) / self.countReview() * 100)
        return count

    def five_star(self):
        reviews = ReviewRating.objects.filter(product=self, status=True, rating=5).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None and reviews['count'] != 0:
            count = int(int(reviews['count']) / self.countReview() * 100)
        return count

    def get_added_like_customer(self):
        return self.like_product.values_list('customer_id', flat=True)

    def get_added_dislike_customer(self):
        return self.dislike_product.values_list('customer_id', flat=True)

    def get_like_count(self):
        like_count = self.like_product.count()
        if like_count > 0:
            return like_count
        return 0

    def get_dislike_count(self):
        dislike_count = self.dislike_product.count()
        if dislike_count > 0:
            return dislike_count
        return 0

    def discountRate(self):
        if self.is_discountprice == True:
            rate = int(100 - ((self.discountprice * 100) / self.price))
            return rate
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(unidecode(self.title))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = ApiProduct.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except ApiProduct.DoesNotExist:
                    self.slug = slug
                    break
        super(ApiProduct, self).save(*args, **kwargs)


class ProductModelGroup(models.Model):
    def product_photo_directory_path(instance, filename):
        return f"products/kapak/{filename}"

    kapak = ResizedImageField(force_format="WEBP", quality=50, upload_to=product_photo_directory_path, null=True,
                              blank=True)
    model_code = models.CharField(verbose_name="Model Kodu", null=True, blank=False, max_length=150, unique=True)
    product = models.ForeignKey(ApiProduct, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.model_code

    def get_kapak(self):
        return self.kapak.url

    def get_product_title(self):
        title = self.product.title
        return str(title)

    def get_product_slug(self):
        slug = self.product.slug
        return str(slug)

    def get_product_price(self):
        price = self.product.price
        return price

    def get_product_isdiscount(self):
        is_discountprice = self.product.is_discountprice
        return is_discountprice

    def get_product_discountprice(self):
        discountprice = self.product.discountprice
        return discountprice

    def third_category(self):
        category_name = self.product.subbottomcategory.title
        return str(category_name)

    def total_stok(self):
        products = ApiProduct.objects.filter(model_code=self.model_code)
        stok = 0

        for p in products:
            stok += p.quantity
        return stok

    def delete(self, using=None, keep_parents=False):
        self.kapak.delete()
        super().delete()


class ReviewRating(models.Model):
    product = models.ForeignKey(ApiProduct, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(max_length=200, blank=True)
    rating = models.FloatField(blank=True)
    ip = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "3) Yorum ve Oylama Sistemi"
        verbose_name_plural = "3) Yorum ve Oylama Sistemi"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def photoReview(self):
        reviews = ReviewRatingImages.objects.all().filter(review=self)
        return reviews


class ReviewRatingImages(models.Model):
    review = models.ForeignKey(ReviewRating, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ApiProduct, on_delete=models.CASCADE, null=True)
    images = models.ImageField(blank=True, upload_to="img/product/comments/", verbose_name="Fotoğraf")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_image(self):
        if self.images:
            return self.images.url
        else:
            return None

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.images.url))

    image_tag.short_description = 'Kapak'


class LikeProduct(models.Model):
    customer = models.ForeignKey(User, null=True, related_name='like_product', on_delete=models.CASCADE)
    product = models.ForeignKey(ApiProduct, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='like_product')
    comment = models.ForeignKey(ReviewRating, null=True, on_delete=models.CASCADE)
    ip = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '4) Beğenilen Ürünler'

    def __str__(self):
        return "%s %s" % (self.customer, self.product)

    def user_liked_product(sender, instance, *args, **kwargs):
        like = instance
        product = like.product
        sender = like.customer

    def user_unlike_product(sender, instance, *args, **kwargs):
        like = instance
        product = like.product
        sender = like.customer


class DisLikeProduct(models.Model):
    customer = models.ForeignKey(User, null=True, related_name='dislike_product', on_delete=models.CASCADE)
    product = models.ForeignKey(ApiProduct, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='dislike_product')
    comment = models.ForeignKey(ReviewRating, null=True, on_delete=models.CASCADE)
    ip = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '5) Beğenilmeyen Ürünler'

    def __str__(self):
        return "%s %s" % (self.customer, self.product)

    def user_disliked_product(sender, instance, *args, **kwargs):
        like = instance
        product = like.product
        sender = like.customer

    def user_undislike_product(sender, instance, *args, **kwargs):
        like = instance
        product = like.product
        sender = like.customer


class Favorite(models.Model):
    customer = models.ForeignKey(User, null=True, related_name='favorite_product', on_delete=models.CASCADE)
    product = models.ForeignKey(ApiProduct, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='favorite_product')
    ip = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '6) Favorilere Eklenen Ürünler'

    def __str__(self):
        return "%s %s" % (self.customer.email, self.product.title)


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Müşteri", null=True, blank=False)
    product = models.ForeignKey(ApiProduct, on_delete=models.CASCADE, verbose_name="Ürün", null=True, blank=False)
    question = models.CharField(max_length=300, verbose_name="Soru", null=True, blank=False)
    answer = models.CharField(max_length=300, verbose_name="Cevap", null=True, blank=True)
    ip = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '7) Soru ve Cevaplar'
        verbose_name_plural = '7) Soru ve Cevaplar'

    def __str__(self):
        return "%s %s" % (self.user.email, self.product.title)

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
                passing = f"{math.floor(pass_time.seconds / 60)} dk."
            elif pass_time.seconds / 60 > 59:
                passing = f"{math.floor(pass_time.seconds / 3600)} sa."
        return passing

class StockAlarm(models.Model):
    product = models.ForeignKey(ApiProduct, on_delete=models.CASCADE, null=True, verbose_name="Ürün")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip = models.CharField(max_length=120, verbose_name="İp Adresi")
    is_active = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name = '8) Gelince Haber Ver'
        verbose_name_plural = '8) Gelince Haber Ver'

    def __str__(self):
        return str(self.product.title)


class KadinUstBedenTablosu(models.Model):
    beden_adi = models.CharField(max_length=50, verbose_name="Beden Adı", null=True, blank=False)
    eu_tr = models.IntegerField(verbose_name="EU-TR Beden", null=True, blank=False)
    boyun = models.CharField(max_length=50, verbose_name="Boyun (cm)", null=True, blank=True)
    gogus = models.CharField(max_length=50, verbose_name="Göğüs (cm)", null=True, blank=True)
    bel = models.CharField(max_length=50, verbose_name="Bel (cm)", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = 'Kadın Üst Beden Tablosu'
        verbose_name_plural = 'Kadın Üst Beden Tablosu'

    def __str__(self):
        return str(self.beden_adi)


class KadinAltBedenTablosu(models.Model):
    beden_adi = models.CharField(max_length=50, verbose_name="Beden Adı", null=True, blank=False)
    eu_tr = models.IntegerField(verbose_name="EU-TR Beden", null=True, blank=False)
    bel = models.CharField(max_length=50, verbose_name="Bel (cm)", null=True, blank=True)
    basen = models.CharField(max_length=50, verbose_name="Basen (cm)", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = 'Kadın Alt Beden Tablosu'
        verbose_name_plural = 'Kadın Alt Beden Tablosu'

    def __str__(self):
        return str(self.beden_adi)


class KadinUstBuyukBedenTablosu(models.Model):
    beden_adi = models.CharField(max_length=50, verbose_name="Beden Adı", null=True, blank=False)
    eu_tr = models.IntegerField(verbose_name="EU-TR Beden", null=True, blank=False)
    boyun = models.CharField(max_length=50, verbose_name="Boyun (cm)", null=True, blank=True)
    gogus = models.CharField(max_length=50, verbose_name="Göğüs (cm)", null=True, blank=True)
    bel = models.CharField(max_length=50, verbose_name="Bel (cm)", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = 'Kadın Üst Büyük Beden Tablosu'
        verbose_name_plural = 'Kadın Üst Büyük Beden Tablosu'

    def __str__(self):
        return str(self.beden_adi)


class KadinAltBuyukBedenTablosu(models.Model):
    beden_adi = models.CharField(max_length=50, verbose_name="Beden Adı", null=True, blank=False)
    eu_tr = models.IntegerField(verbose_name="EU-TR Beden", null=True, blank=False)
    bel = models.CharField(max_length=50, verbose_name="Bel (cm)", null=True, blank=True)
    basen = models.CharField(max_length=50, verbose_name="Basen (cm)", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = 'Kadın Alt Büyük Beden Tablosu'
        verbose_name_plural = 'Kadın Alt Büyük Beden Tablosu'

    def __str__(self):
        return str(self.beden_adi)


class KadinJeanBedenTablosu(models.Model):
    beden_adi = models.CharField(max_length=50, verbose_name="Beden Adı", null=True, blank=False)
    eu_tr = models.CharField(max_length=50, verbose_name="EU-TR Beden", null=True, blank=False)
    bel = models.CharField(max_length=50, verbose_name="Bel (cm)", null=True, blank=True)
    basen = models.CharField(max_length=50, verbose_name="Basen (cm)", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = 'Kadın Jean Beden Tablosu'
        verbose_name_plural = 'Kadın Jean Beden Tablosu'

    def __str__(self):
        return str(self.beden_adi)
