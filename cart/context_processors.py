from .models import Cart, CartItem

def cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        total_items = sum(item.quantity for item in cart_items)
        total_price = sum(item.get_total_price() for item in cart_items)
        
        return {
            'cart_items': cart_items,
            'cart_total_items': total_items,
            'cart_total_price': total_price,
        }
    return {
        'cart_items': [],
        'cart_total_items': 0,
        'cart_total_price': 0,
    }