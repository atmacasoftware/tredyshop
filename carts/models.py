from django.db import models
from user_accounts.models import User
from customer.models import CustomerAddress, Coupon
from product.models import ProductVariant
from mainpage.models import Setting
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

    def total_price(self):
        total = 0
        for item in CartItem.objects.filter(cart=self):
            if item.product.product.is_discountprice == True:
                total += (item.product.product.discountprice * item.quantity)
            else:
                total += (item.product.product.price * item.quantity)

        return total

    def total_not_discuntprice(self):
        total = 0
        for item in CartItem.objects.filter(cart=self):
                total += (item.product.product.price * item.quantity)
        return total

    def total_discount(self):
        minus = 0
        for item in CartItem.objects.filter(cart=self):
            if item.product.product.is_discountprice == True:
                total_discount_price = item.product.product.discountprice * item.quantity
                total_price = item.product.product.price * item.quantity
                minus = total_price - total_discount_price
        return minus

    def used_coupon(self):
        is_used = Coupon.objects.filter(user_id=self.cart_id, is_active=True).exists()
        return is_used

    def coupon(self):
        try:
            coupon = Coupon.objects.get(user_id=self.cart_id, is_active=True)
            if CartItem.objects.filter(cart=self).count() == 0:
                coupon.is_active = False
                coupon.save()
            return coupon
        except:
            return "Not available"

    def delivery_price(self):
        setting = Setting.objects.all().last()
        total_price = self.total_price()
        if total_price > setting.free_shipping:
            return "Ücretsiz"
        else:
            return setting.shipping_price

    def total_quantity(self):
        quantity = 0
        for cart_item in CartItem.objects.filter(cart=self):
            quantity += cart_item.quantity

        return quantity

    def general_total(self):
        setting = Setting.objects.all().last()
        delivery_price = setting.shipping_price
        is_coupon = self.used_coupon()
        coupon = self.coupon()
        total = self.total_price()
        general_total = 0
        if CartItem.objects.filter(cart=self).count() > 0:
            quantity = 0
            for cart_item in CartItem.objects.filter(cart=self):
                quantity += cart_item.quantity

                if total < setting.free_shipping:
                    if is_coupon == True:
                        general_total = float(total) + float(setting.shipping_price) - float(coupon.coupon_price)
                    else:
                        general_total = float(total) + float(setting.shipping_price)
                else:
                    if is_coupon == True:
                        general_total = float(total) + float(setting.shipping_price) - float(coupon.coupon_price)
                    else:
                        general_total = total

        return general_total

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        if self.product.product.is_discountprice == True:
            return self.product.product.discountprice * self.quantity
        else:
            return self.product.product.price * self.quantity

    def not_discount_sub_total(self):
        return self.product.product.price * self.quantity

    def __str__(self):
        return f"{str(self.product.title)}"