from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models import Count
from django.template import defaultfilters
from unidecode import unidecode
import readtime as readtime

from user_accounts.models import User


# Create your models here.

class BlogCategory(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='Oluşturan Kullanıcı', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Blog Kategorisi")
    slug = models.SlugField(max_length=1000, unique=False, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateField(auto_now=True, null=True, verbose_name="Güncelleme Tarihi")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(unidecode(self.name))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = BlogCategory.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except BlogCategory.DoesNotExist:
                    self.slug = slug
                    break
        super(BlogCategory, self).save(*args, **kwargs)

class Blog(models.Model):
    CATEGORY = (
        ('Moda', 'Moda'),
        ('Elektronik', 'Elektronik'),
        ('Sağlık', 'Sağlık'),
        ('Ev Yaşamı', 'Ev Yaşamı'),
        ('Kozmetik', 'Kozmetik'),
    )

    user = models.ForeignKey(User, null=True, verbose_name='Yazar', on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategory, null=True, on_delete=models.CASCADE, verbose_name="Kategori")
    image = models.ImageField(upload_to='static/img/blog/', blank=True, verbose_name="Blog Resmi")
    title = models.CharField(max_length=200, null=True, verbose_name='Başlık')
    content = RichTextUploadingField()
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateField(auto_now=True, verbose_name="Güncelleme Tarihi")
    blog_views = models.IntegerField(default=0, null=True, blank=True)
    is_publish = models.BooleanField(default=False, verbose_name="Yayında mı?")
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=1000, unique=False, null=True)

    def __str__(self):
        return "%s %s" % (self.user, self.title)

    def get_blog_photos(self):
        if self.image:
            return self.image.url
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
                    slug_exits = Blog.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except Blog.DoesNotExist:
                    self.slug = slug
                    break
        super(Blog, self).save(*args, **kwargs)

    def get_readtime(self):
        result = readtime.of_text(self.content)
        return result.text

    def get_keywords(self):
        keywords = Keywords.objects.filter(blog=self.id)
        return keywords

    def countReview(self):
        reviews = ReviewRatingBlog.objects.filter(blog=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    class Meta:
        ordering = ['-created_at']

class BlogKeywords(models.Model):
    name = models.CharField(max_length=255, verbose_name="Anahtar Kelime", null=True, blank=True)
    blog = models.ForeignKey(Blog, verbose_name="Blog", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.name)

class ReviewRatingBlog(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(max_length=200, blank=True)
    rating = models.FloatField(blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
