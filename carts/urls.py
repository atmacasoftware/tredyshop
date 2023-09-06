from django.urls import path
from carts.views import *

urlpatterns = [
    path('sepetim', cart, name="cart"),
    path('urun_ekle/<int:product_id>', add_cart, name="add_cart"),
    path('urun_sil/<int:product_id>/<int:cart_item_id>', remove_cart, name="remove_cart"),
    path('urun_miktari/azalt/<int:product_id>/<int:cart_item_id>', minus_quantity, name="minus_quantity"),
    path('urun_miktari/arttir/<int:product_id>/<int:cart_item_id>', plus_quantity, name="plus_quantity"),
    path('odeme-adimi', submitCheckout, name="submitCheckout"),
    path('checkout', checkout, name="checkout"),
    path('odeme-basarisiz', payment_failed, name="payment_failed"),
    path('paytr-bildirim-url/', callback, name="paytr_bildirim"),
    path('checkout/adres-secimi/<int:address_id>', select_address, name="select_address"),
    path('odeme-tamamlandi/siparis_no=<str:order_number>', completed_checkout, name="completed_checkout"),

    path('kupon-uygula', uses_coupon, name='uses_coupon'),
    path('kupon-kaldir', delete_coupon, name='delete_coupon'),
]
