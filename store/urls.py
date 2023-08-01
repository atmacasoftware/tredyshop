from django.urls import path
from store.views import *

urlpatterns = [
    path('ara/', store_page, name="store"),
    path('ara/marka/<slug:brands_slug>/', store_page, name="product_by_brands"),
    path('ara/<slug:categroy_slug>/', store_page, name="product_by_category"),
    path('ara/<slug:categroy_slug>/<slug:subcategory_slug>/', store_page, name="product_by_subcategory"),
    path('ara/<slug:categroy_slug>/<slug:subcategory_slug>/<slug:subbottomcategory_slug>/', store_page, name="product_by_subbottomcategory"),
    path('yeni-urunler/', new_product, name="new_product"),
    path('en-cok-satan-urunler/', most_sell_product, name="most_sell_product"),
    path('50-tl-alti-urunler/', under_50_price, name="under_50_price"),
    path('super-firsatlar/', most_discount_product, name="most_discount_product"),
]
