from django.urls import path
from trendyol.views import *

urlpatterns = [
    path('yonetim/trendyol/hesap-bilgileri/', trendyol_hesap_bilgileri, name="trendyol_hesap_bilgileri"),
    path('yonetim/trendyol/entegrasyon-islemleri/', trendyol_engtegrasyon_islemleri, name="trendyol_engtegrasyon_islemleri"),
    path('yonetim/trendyol/kategori-eslestir/', trendyol_kategori_eslestir, name="trendyol_kategori_eslestir"),
    path('yonetim/trendyol/kategori-eslestir/kategorileri-al/', trendyol_kategori_al, name="trendyol_kategori_al"),
    path('yonetim/trendyol/kategori-eslestir/ozellikleri-getir/', trendyol_ozellikleri_getir, name="trendyol_ozellikleri_getir"),
    path('yonetim/trendyol/kategori-eslestir/ozellik-kaydet/', trendyol_ozellik_kaydet, name="trendyol_ozellik_kaydet"),
    path('yonetim/trendyol/urun-gonder/', trendyol_urun_gonder, name="trendyol_urun_gonder"),
    path('yonetim/trendyol/stok-fiyat-guncelle/', trendyol_stok_fiyat_guncelle, name="trendyol_stok_fiyat_guncelle"),
]
