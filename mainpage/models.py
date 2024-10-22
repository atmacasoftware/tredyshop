from django.db import models
from django.utils.safestring import mark_safe
from autoslug import AutoSlugField
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from django.template import defaultfilters
from unidecode import unidecode

# Create your models here.

class Setting(models.Model):
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
    logo = models.ImageField(blank=True, upload_to="img/logo/")
    icon = models.ImageField(blank=True, upload_to="img/favicon/")
    facebook = models.CharField(max_length=255, null=True, blank=True, verbose_name="Facebook")
    instagram = models.CharField(max_length=255, null=True, blank=True, verbose_name="İnstagram")
    twitter = models.CharField(max_length=255, null=True, blank=True, verbose_name="Twitter")
    youtube = models.CharField(max_length=255, null=True, blank=True, verbose_name="Youtube")
    tiktok = models.CharField(max_length=255, null=True, blank=True, verbose_name="Tiktok")
    linkedin = models.CharField(max_length=255, null=True, blank=True, verbose_name="Linkedin")
    whatsapp = models.CharField(max_length=255, null=True, blank=True, verbose_name="Whatsapp")
    aboutus = models.TextField(verbose_name="Hakkımızda", blank=True, null=True)
    references = models.TextField(verbose_name="Referanslar", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "1) Ayarlar"
        verbose_name_plural = "1) Ayarlar"


class City(models.Model):
    title = models.CharField(max_length=100, null=True, blank=False, verbose_name="Şehir Adı")
    code = models.IntegerField(verbose_name="Plaka Kodu", null=True)
    slug = AutoSlugField(populate_from="title", unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "2) Şehirler"
        verbose_name_plural = "2) Şehirler"
        ordering = ['code']

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(unidecode(self.title))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = City.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except City.DoesNotExist:
                    self.slug = slug
                    break
        super(City, self).save(*args, **kwargs)


class County(models.Model):
    title = models.CharField(max_length=100, null=True, blank=False, verbose_name="İlçe Adı")
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, verbose_name="Şehir")
    slug = AutoSlugField(populate_from="title", unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "3) İlçeler"
        verbose_name_plural = "3) İlçeler"
        ordering = ['id']

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(unidecode(self.title))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = County.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except County.DoesNotExist:
                    self.slug = slug
                    break
        super(County, self).save(*args, **kwargs)


class MostSearchingKeyword(models.Model):
    keyword = models.CharField(max_length=50, null=True, blank=False)
    ip = models.CharField(max_length=20, blank=True)
    count = models.BigIntegerField(default=0, verbose_name="Arama Sayısı", null=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "5) En Çok Aranan Kelimeler"
        verbose_name_plural = "5) En Çok Aranan Kelimeler"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.keyword}"

    def get_url(self):
        return reverse('products_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(unidecode(self.keyword))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = MostSearchingKeyword.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except MostSearchingKeyword.DoesNotExist:
                    self.slug = slug
                    break
        super(MostSearchingKeyword, self).save(*args, **kwargs)


class SSS(models.Model):
    question = models.CharField(max_length=255, verbose_name="Soru", null=True, blank=False)
    answer = models.TextField(max_length=1000, verbose_name="Cevap", null=True, blank=False)
    icon = models.CharField(max_length=5000, verbose_name="İkon", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "6) Sıkça Sorulan Sorular"
        verbose_name_plural = "6) Sıkça Sorulan Sorular"
        ordering = ['-id']

    def __str__(self):
        return f"{self.question}"


class Contracts(models.Model):
    delivery = CKEditor5Field('Teslimat Koşulları', config_name='extends', null=True, blank=True)
    membership = CKEditor5Field('Üyelik Sözleşmesi', config_name='extends', null=True, blank=True)
    term_of_use = CKEditor5Field('Site Kullanım Şartları', config_name='extends', null=True, blank=True)
    security = CKEditor5Field('Gizlilik Politikası', config_name='extends', null=True, blank=True)
    kvkk = CKEditor5Field('KVKK Aydınlatma Politası', config_name='extends', null=True, blank=True)
    cookie = CKEditor5Field('Cookies', config_name='extends', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "7) Sözleşmeler"
        verbose_name_plural = "7) Sözleşmeler"
        ordering = ['created_at']


class Cookies(models.Model):
    cookie_provider = models.CharField(max_length=255, null=True, blank=True, verbose_name="Cookie Sağlayıcısı")
    cookie_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Cookie İsmi")
    cookie_aim = models.CharField(max_length=255, null=True, blank=True, verbose_name="Cookie Amacı")
    cookie_type = models.CharField(max_length=255, null=True, blank=True, verbose_name="Cookie Tipi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?", null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "8) Çerezler"
        verbose_name_plural = "8) Çerezler"
        ordering = ['created_at']
