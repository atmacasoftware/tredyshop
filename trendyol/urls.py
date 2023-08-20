from django.urls import path
from trendyol.views import *

urlpatterns = [
    path('xml-yonetimi/trendyol/', trendyol, name="trendyol"),
    path('xml-yonetimi/trendyol/urun-yonetimi/', trendyol_product, name="trendyol_product"),
]
