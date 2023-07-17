from django.urls import path
from mainpage.views import *

urlpatterns = [
    path('', index, name="mainpage"),
    path('searching/', ajax_search, name="ajax_search"),
    path('arama/', search, name="search"),
    path('bilgi-duyuru/<str:slider_slug>', slider_info, name="slider_info"),
    path('sikca-sorulan-sorular', sss, name="faq"),
]
