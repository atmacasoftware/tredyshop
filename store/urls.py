from django.urls import path
from store.views import *

urlpatterns = [
    path('ara/', store_page, name="store"),
    path('ara/marka/<slug:brands_slug>/', store_page, name="product_by_brands"),
    path('ara/<slug:categroy_slug>/', store_page, name="product_by_category"),
    path('ara/<slug:categroy_slug>/<slug:subcategory_slug>/', store_page, name="product_by_subcategory"),
    path('ara/<slug:categroy_slug>/<slug:subcategory_slug>/<slug:subbottomcategory_slug>/', store_page, name="product_by_subbottomcategory"),
    path('filtreler/<slug:categroy_slug>/<slug:subcategoryslug>/', filter_data, name='ajax_product_filter'),
    path('filtreler/<slug:categroy_slug>/<slug:subcategoryslug>/<slug:subottomcategoryslug>/', filter_data, name='ajax_product_filter'),
    path('filtreler/marka/<slug:brandsslug>/', filter_data, name='ajax_product_filter'),
    path('yeni-urunler/', new_product, name="new_product"),
    path('en-cok-satan-urunler/', most_sell_product, name="most_sell_product"),
    path('firsatlar/', banner_one, name="banner_one"),
    path('indirimler/', banner_two, name="banner_two"),
    path('super-firsatlar/', most_discount_product, name="most_discount_product"),
    path('load-more-product/', product_list, name="load_more_data"),
]
