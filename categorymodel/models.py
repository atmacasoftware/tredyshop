from django.db import models
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.template import defaultfilters
from unidecode import unidecode
# Create your models here.

class MainCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name="Kategori Adı")
    keyword = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    image = models.ImageField(blank=True, upload_to='img/category/', null=True)
    order = models.IntegerField(verbose_name="Sırası", null=True, blank=False)
    category_no = models.CharField(verbose_name="Kategori Numarası", null=True, blank=True, max_length=50)
    is_active = models.BooleanField(default=True, verbose_name="Yayınlansın mı?")
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "1) 1. Düzey Kategori"
        verbose_name_plural = "1) 1. Düzey Kategori"
        ordering = ["order"]

    def __str__(self):
        return f"{self.title}"

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Kapak'

    def get_url(self):
        return reverse('product_by_category', args=[self.slug])

    def get_absolute_url(self):
        return reverse('first_category', args=[self.slug])

    def product_count(self):
        return self.main_category.filter(is_publish=True).count()

    def exist_subbottomcategories(self):
        c = self.maincategories.filter(maincategory_id=self.id)
        if c.exists():
            return "True"
        else:
            return "False"

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(unidecode(self.title))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = MainCategory.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except MainCategory.DoesNotExist:
                    self.slug = slug
                    break
        super(MainCategory, self).save(*args, **kwargs)


class SubCategory(models.Model):
    maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE, null=True, blank=False,
                                     verbose_name="Ana Kategori", related_name='subcategories')
    title = models.CharField(max_length=255, verbose_name="Kategori Adı")
    keyword = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    image = models.ImageField(blank=True, upload_to='img/category/', null=True)
    category_no = models.CharField(verbose_name="Kategori Numarası", null=True, blank=True, max_length=50)
    is_active = models.BooleanField(default=True, verbose_name="Yayınlansın mı?")
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "2) 2. Düzey Kategori"
        verbose_name_plural = "2) 2. Düzey Kategori"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title}"

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return None

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Kapak'

    def get_url(self):
        return reverse('product_by_subcategory', args=[self.maincategory.slug,self.slug])

    def get_absolute_url(self):
        return reverse('second_category', args=[self.slug])

    def product_count(self):
        return self.sub_category.filter(is_publish=True).count()

    def save(self, *args, **kwargs):

        if not self.id and not self.slug:
            slug = defaultfilters.slugify(unidecode(self.title))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = SubCategory.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except SubCategory.DoesNotExist:
                    self.slug = slug
                    break
        super(SubCategory, self).save(*args, **kwargs)


class SubBottomCategory(models.Model):
    maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE, null=True, blank=False,
                                     verbose_name="Ana Kategori", related_name="maincategories")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=False,
                                     verbose_name="Alt Kategori", related_name='subbottomcategories')
    title = models.CharField(max_length=255, verbose_name="Kategori Adı")
    keyword = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    image = models.ImageField(blank=True, upload_to='img/category/', null=True)
    category_no = models.CharField(verbose_name="Kategori Numarası", null=True, blank=True, max_length=50)
    is_active = models.BooleanField(default=True, verbose_name="Yayınlansın mı?")
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "3) 3. Düzey Kategori"
        verbose_name_plural = "3) 3. Düzey Kategori"
        ordering = ('title',)

    def __str__(self):
        return f"{self.maincategory.title} > {self.subcategory.title} > {self.title}"

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Kapak'

    def get_url(self):
        return reverse('product_by_subbottomcategory', args=[self.maincategory.slug,self.subcategory.slug,self.slug])

    def get_title(self):
        return self.title

    def get_absolute_url(self):
        return reverse('third_category', args=[self.slug])

    def product_count(self):
        return self.subbottom_category.filter(is_publish=True).count()

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(unidecode(self.title))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = SubBottomCategory.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except SubBottomCategory.DoesNotExist:
                    self.slug = slug
                    break
        super(SubBottomCategory, self).save(*args, **kwargs)


