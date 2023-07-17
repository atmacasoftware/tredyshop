from django.urls import path
from customer.views import *

urlpatterns = [
    path('giris-yap', login, name="login"),
    path('kayit-ol', register, name="register"),
    path('aktivasyon/<uidb64>/<token>', activate, name="activate"),
    path('cikis-yap', logout, name="logout"),
    path('check-email/', validate_email, name="validate-email"),
    path('kullanici-bilgilerim', profile_mainpage, name="profile_mainpage"),
    path('adreslerim', address, name="address"),
    path('adreslerim/adres_id=<int:id>/guncelle', update_address, name="update_address"),
    path('adreslerim/adres_id=<int:id>/sil', delete_address, name="delete_address"),
    path('favorilerim', wishlist, name="wishlist"),
    path('favorilerim/<int:id>', delete_wishlist, name="delete_wishlist"),
    path('degerlendirmelerim', reviews, name="reviews"),
    path('siparislerim', order_page, name="order_page"),
    path('siparislerim/siparis_takip/siparis_no=<str:order_number>', order_detail, name="order_detail"),
    path('kuponlarim', coupon_page, name="coupon_page"),

    path('ajax/load-counties/', load_counties, name='load_counties'),
]
