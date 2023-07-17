from django.urls import path
from store.views import *

urlpatterns = [
    path('ara/', store_page, name="store"),
    path('ara/marka/<slug:brands_slug>/', store_page, name="product_by_brands"),
    path('ara/<slug:categroy_slug>/', store_page, name="product_by_category"),
    path('ara/<slug:categroy_slug>/<slug:subcategory_slug>/', store_page, name="product_by_subcategory"),

]
