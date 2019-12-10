from django import template
from items.models import Cart

register = template.Library()

@register.filter
def products_in_cart(user):
    if user.is_authenticated:
        cart = Cart.objects.filter(UserID=user)
        if cart.exists():
            return cart[0].quantity
    return 0
