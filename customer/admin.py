from django.contrib import admin

from customer.models import CustomerAddress,Subscription,Coupon

# Register your models here.

class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'city', 'county', 'neighbourhood', 'bill_type']
    list_filter = ['is_active']
    search_fields = ('title',)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'ip', 'created_at']
    search_fields = ('email',)

class CouponAdmin(admin.ModelAdmin):
    list_display = ['user', 'coupon_code', 'coupon_price', 'coupon_conditional', 'coupon_category']
    search_fields = ('coupon_code',)

admin.site.register(CustomerAddress, CustomerAddressAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Coupon, CouponAdmin)
