from django.contrib.sitemaps import Sitemap
from product.models import ApiProduct

class ProductSitemap(Sitemap):
    def items(self):
        return ApiProduct.objects.all()