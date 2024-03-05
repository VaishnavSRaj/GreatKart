from .models import Cart, CartItem
from .views import _cart_id


def cart_count(request):

    cart_count = 0

    if "admin" in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            print(cart)
            if request.user.is_authenticated:
                print('hi')
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
             cart_count += cart_item.quantity

        except Cart.DoesNotExist:
            print('except block')
            cart_count = 0
        print(f"Cart Count: {cart_count}")    
    return dict(cart_count=cart_count)
