from django.contrib.sitemaps import Sitemap
from categorymodel.models import *

class MaincategorySitemap(Sitemap):
    def items(self):
        return MainCategory.objects.all()

class SubcategorySitemap(Sitemap):
    def items(self):
        return SubCategory.objects.all()

class SubbottomcategorySitemap(Sitemap):
    def items(self):
        return SubBottomCategory.objects.all()