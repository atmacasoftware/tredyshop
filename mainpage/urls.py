from django.urls import path
from mainpage.views import *

urlpatterns = [
    path('', index, name="mainpage"),
    path('searching/', ajax_search, name="ajax_search"),
    path('arama/', search, name="search"),
    path('bilgi-duyuru/<str:slider_slug>', slider_info, name="slider_info"),
    path('sikca-sorulan-sorular', sss, name="faq"),
    path('teslimat-kosullari', delivery_conditional, name="delivery_conditional"),
    path('uyelik-sozlesmesi', membership_contract, name="membership_contract"),
    path('site-kullanim-sartlari', terms_of_use, name="terms_of_use"),
    path('gizlilik-politikasi', security_policy, name="security_policy"),
    path('kvkk-aydinlatma-metni', kvkk, name="kvkk"),
]
