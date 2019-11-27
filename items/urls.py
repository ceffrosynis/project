from django.urls import path
from .views import Home, Details, add_to_cart, CartSummary, remove_from_cart
from django.conf.urls.static import static
from django.conf import settings

app_name = 'items'

urlpatterns = [
    path('', Home.as_view(), name='home'), 
    path('product/<slug>/', Details.as_view(), name='details'),
    path('cart/<slug>', add_to_cart, name="cart"),
    path('cart_summary', CartSummary.as_view(), name='cart_summary'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove_from_cart')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
