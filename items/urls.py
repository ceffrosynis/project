from django.urls import path
from .views import Home, Details, add_to_cart
from django.conf.urls.static import static
from django.conf import settings

app_name = 'items'

urlpatterns = [
    path('', Home.as_view(), name='home'), 
    path('product/<slug>/', Details.as_view(), name='details'),
    path('cart/<slug>', add_to_cart, name="cart")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
