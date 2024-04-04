from carts.models import *

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=request.META.get('REMOTE_ADDR'))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter()
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += 1
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count, cart_items=cart_items)