from django.urls import path
from product.views import *

urlpatterns = [
    path('urun/<str:product_slug>', products_detail, name="products_detail"),
    path('urun/<str:slug>/urun-degerlendirmeleri/', degerlendirme_sayfasi, name="degerlendirme_sayfasi"),
    path('urun/<int:id>/urun-degerlendirmeleri/filtered/', filter_yorum, name="filter_yorum"),
    path('urun/<int:id>/urun-degerlendirmeleri/daha-fazla-yukle/', load_more_degerlendirme, name="load_more_degerlendirme"),
    path('urun/<str:slug>/urun-sorulari/', soru_sayfasi, name="soru_sayfasi"),
    path('urun/<int:id>/urun-sorulari/daha-fazla-yukle/', load_more_question, name="load_more_question"),
    path('favourite/', ajax_favourite, name="ajax_favourite"),
    path('favourite/kaldir/product_id=<int:product_id>', deleted_favourite, name="deleted_favourite"),
    path('stockalarm', ajax_stockalarm, name="ajax_stockalarm"),
]
