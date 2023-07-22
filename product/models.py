from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.db import models
from django.db.models import Avg, Count
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify
from django.urls import reverse
from categorymodel.models import MainCategory, SubCategory, SubBottomCategory
from user_accounts.models import User


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
        verbose_name = "2) Markalar"
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
            self.title = self.title.replace("ı", "i")
            self.title = self.title.replace("ö", "o")
            self.title = self.title.replace("ü", "u")
            self.title = self.title.replace("ş", "s")
            slug = slugify(self.title)
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


class Product(models.Model):
    TYPE = (
        ("Renk-Boyut", "Renk-Boyut"),
        ("Renk", "Renk"),
        ("Boyut", "Boyut"),
        ("Yok", "Yok"),
    )

    category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, null=True, blank=False,
                                 verbose_name="1. Düzey Kategori", related_name="main_category")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=False,
                                    verbose_name="2. Düzey Kategori", related_name="sub_category")
    subbottomcategory = models.ForeignKey(SubBottomCategory, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name="3. Düzey Kategori", related_name="subbottom_category")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Marka",
                              related_name="brands")
    title = models.CharField(max_length=50, verbose_name="Başlık")
    description = models.CharField(max_length=255, verbose_name="Açıklama")
    image = models.ImageField(blank=True, upload_to="img/product/", verbose_name="Kapak Resmi")
    price = models.DecimalField(verbose_name="Fiyat", decimal_places=2, max_digits=20)
    discountprice = models.DecimalField(verbose_name="İndirimli Fiyat", decimal_places=2, max_digits=20, null=True,
                                        blank=True)
    is_discountprice = models.BooleanField(default=False, verbose_name="İndirimli Yayınla", null=True, blank=True)
    amount = models.IntegerField(verbose_name="Miktar")
    stock_code = models.CharField(verbose_name="Stok Kodu", null=True, blank=False, max_length=50)
    detail = RichTextUploadingField(verbose_name="Detay")
    variant = models.CharField(choices=TYPE, max_length=20, blank=True, default="Yok", null=True, verbose_name="Tip")
    is_publish = models.BooleanField(default=True, verbose_name="Yayında mı?", null=True)
    sell_count = models.BigIntegerField(default=0, verbose_name="Toplam Satış Sayısı", null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    status = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "1) Ürünler"
        verbose_name_plural = "1) Ürünler"

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return None

    def not_stock(self):
        if self.amount <= 0:
            self.is_publish = False
            self.save()

    def get_url(self):
        return reverse('products_detail', args=[self.slug])

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Kapak'

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

    def get_variations(self):
        variations = Variants.objects.all().filter(product=self)
        if variations.count() > 0:
            return variations
        else:
            return None

    def discountRate(self):
        if self.is_discountprice == True:
            rate = int(100 - ((self.discountprice * 100) / self.price))
            return rate
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.title = self.title.replace("ı", "i")
            self.title = self.title.replace("ö", "o")
            self.title = self.title.replace("ü", "u")
            self.title = self.title.replace("ş", "s")
            slug = slugify(self.title)
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = Product.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except Product.DoesNotExist:
                    self.slug = slug
                    break
        super(Product, self).save(*args, **kwargs)


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, verbose_name="Başlık")
    image = models.ImageField(blank=True, upload_to="img/product/", verbose_name="Resim")

    def __str__(self):
        return f"{str(self.id)}"

    class Meta:
        verbose_name = "Ürüne Ait Resimler"
        verbose_name_plural = "Ürüne Ait Resimler"

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return None


class Color(models.Model):
    name = models.CharField(max_length=20, verbose_name="Renk")
    code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Renk Kodu")

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color: {}">Renk</p>'.format(self.code))
        else:
            return ""


    class Meta:
        verbose_name = "Renkler"
        verbose_name_plural = "Renkler"

class Size(models.Model):
    name = models.CharField(max_length=20, verbose_name="Boyut")
    code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Boyut Kodu")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Boyut/Kapasite"
        verbose_name_plural = "Boyut/Kapasite"


class Variants(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="Başlık")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Ürün")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name="Renk", blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name="Boyut", null=True, blank=True)
    image_id = models.IntegerField(blank=True, null=True, default=0)
    quantity = models.IntegerField(default=1, verbose_name="Miktar")
    price = models.FloatField(default=0, verbose_name="Fiyat")
    discountprice = models.DecimalField(verbose_name="İndirimli Fiyat", decimal_places=2, max_digits=20, null=True,
                                        blank=True)
    is_discountprice = models.BooleanField(default=False, verbose_name="İndirimli Yayınla", null=True, blank=True)
    is_publish = models.BooleanField(default=True, verbose_name="Yayında mı?", null=True)
    sell_count = models.BigIntegerField(default=0, verbose_name="Toplam Satış Sayısı", null=True, blank=True)

    def __str__(self):
        return self.title


    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage = ""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""

class DescriptionList(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    list = models.CharField(max_length=100, blank=False, null=True, verbose_name="Açıklama")

    class Meta:
        verbose_name = "Öne Çıkan Açıklamalar"
        verbose_name_plural = "Öne Çıkan Açıklamalar"


class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, verbose_name="Başlık")
    description = models.CharField(max_length=100, blank=False, null=True, verbose_name="Açıklama")

    class Meta:
        verbose_name = "Ürüne Ait Özellikler"
        verbose_name_plural = "Ürüne Ait Özellikler"


class ProductKeywords(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100, blank=False, null=True, verbose_name="Anahtar Kelime")

    class Meta:
        verbose_name = "Anahtar Kelime"
        verbose_name_plural = "Anahtar Kelime"

    def __str__(self):
        return self.product.title


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(max_length=200, blank=True)
    rating = models.FloatField(blank=True)
    ip = models.CharField(max_length=20, blank=True)
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
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
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE, related_name='like_product')
    comment = models.ForeignKey(ReviewRating, null=True, on_delete=models.CASCADE)
    ip = models.CharField(max_length=20, blank=True)
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
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='dislike_product')
    comment = models.ForeignKey(ReviewRating, null=True, on_delete=models.CASCADE)
    ip = models.CharField(max_length=20, blank=True)
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
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='favorite_product')
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '6) Favorilere Eklenen Ürünler'

    def __str__(self):
        return "%s %s" % (self.customer.email, self.product.title)


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Müşteri", null=True, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Ürün", null=True, blank=False)
    question = models.CharField(max_length=300, verbose_name="Soru", null=True, blank=False)
    answer = models.CharField(max_length=300, verbose_name="Cevap", null=True, blank=True)
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '7) Soru ve Cevaplar'
        verbose_name_plural = '7) Soru ve Cevaplar'

    def __str__(self):
        return "%s %s" % (self.user.email, self.product.title)


class StockAlarm(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, verbose_name="Ürün")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip = models.CharField(max_length=120, verbose_name="İp Adresi")
    is_active = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name = '8) Gelince Haber Ver'
        verbose_name_plural = '8) Gelince Haber Ver'

    def __str__(self):
        return str(self.product.title)
