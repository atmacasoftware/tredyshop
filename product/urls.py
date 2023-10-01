from django.urls import path
from product.views import *

urlpatterns = [
    path('urun/<str:product_slug>', products_detail, name="products_detail"),
    path('load-more-reviews', load_more_reviews, name="load_more_reviews"),
    path('load-more-question', load_more_question, name="load_more_question"),
    path('favourite', ajax_favourite, name="ajax_favourite"),
    path('stockalarm', ajax_stockalarm, name="ajax_stockalarm"),
]
