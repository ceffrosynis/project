from django.contrib import admin

from .models import Product, Transaction, Cart, Order
# Register your models here.


admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(Cart)
admin.site.register(Order)
