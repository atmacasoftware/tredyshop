from django.contrib.sitemaps import Sitemap
from product.models import Product

class ProductSitemap(Sitemap):
    def items(self):
        return Product.objects.all()