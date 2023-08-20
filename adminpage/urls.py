from django.urls import path
from adminpage.views import *

urlpatterns = [
    path('giris-yap/', admin_login, name='admin_login'),

    path('', mainpage, name='admin_mainpage'),
    path('urunler/', products, name='admin_product'),

    path('xml-yonetimi/tahtakale/veri-yukle-guncelle/', tahtakale_product, name="tahtakale_product"),
    path('xml-yonetimi/tahtakale/veri-yukle/', tahtakale_product_load, name="tahtakale_product_load"),
    path('xml-yonetimi/tahtakale/veri-guncelle/', tahtakale_product_update, name="tahtakale_product_update"),
    path('xml-yonetimi/haydigiy/veri-yukle-guncelle/', haydigiy_product, name="haydigiy_product"),
    path('xml-yonetimi/haydigiy/veri-yukle/', haydigiy_product_load, name="haydigiy_product_load"),
    path('xml-yonetimi/haydigiy/veri-guncelle/', haydigiy_product_update, name="haydigiy_product_update"),

    # trendyol
    path('trendyol/urun-giris/', trendyol_add_product, name="trendyol_add_product"),
    path('trendyol/urun-giris/giyim/', trendyol_add_product_giyim, name="trendyol_add_product_giyim"),
    path('trendyol/urun-giris/giyim/kategori_no=<category_no>/', trendyol_add_product_giyim_category1,
         name="trendyol_add_product_giyim_category1"),
    path('trendyol/urun-giris/giyim/kategori_id=<int:id>/trendyol/urun-gonder/',
         trendyol_add_product_giyim_send_trendyol, name="trendyol_add_product_giyim_send_trendyol"),

    # muhasebe
    path('kesilen-faturalar/fatura-ekle/', kesilen_fatura_ekle, name="kesilen_fatura_ekle"),
    path('kesilen-faturalar/tum-faturalar/', kesilen_faturalar, name="kesilen_faturalar"),
    path('kesilen-faturalar/tum-faturalar/fatura-guncelle/fatura_id=<int:id>/', update_kesilen_fatura,
         name="update_kesilen_fatura"),
    path('kesilen-faturalar/tum-faturalar/fatura-sil/fatura_id=<int:id>/', delete_kesilen_fatura,
         name="delete_kesilen_fatura"),
    path('kesilen-faturalar/tum-faturalar/excel/', kesilen_faturalar_export_excel,
         name="kesilen_faturalar_export_excel"),

    path('alinan-faturalar/fatura-ekle/', alinan_fatura_ekle, name="alinan_fatura_ekle"),
    path('alinan-faturalar/tum-faturalar/', alinan_faturalar, name="alinan_faturalar"),
    path('alinan-faturalar/tum-faturalar/fatura-guncelle/fatura_id=<int:id>/', update_alinan_fatura,
         name="update_alinan_fatura"),
    path('alinan-faturalar/tum-faturalar/fatura-sil/fatura_id=<int:id>/', delete_alinan_fatura,
         name="delete_alinan_fatura"),
    path('alinan-faturalar/tum-faturalar/excel/', alinan_faturalar_export_excel,
         name="alinan_faturalar_export_excel"),

    path('hesap-bilgilerim/', user_info, name='user_info'),
    path('sifre-degistir/', change_password, name='admin_change_password'),
]
