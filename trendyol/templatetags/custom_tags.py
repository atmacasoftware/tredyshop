from django import template

from product.models import ProductVariant
from trendyol.models import TrendyolProduct

register = template.Library()

@register.simple_tag
def get_attribute(product_id, attribute_id, custom):
    try:
        product = ProductVariant.objects.get(id=product_id)
        trendyol_product = TrendyolProduct.objects.get(product=product)
        return trendyol_product.get_attributes(attribute_id, custom)
    except:
        return None