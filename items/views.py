from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Product, Transaction, Cart, Order

# Create your views here.

class Home(ListView):
    model = Product
    template_name = "home.html"

class Details(DetailView):
    model = Product
    template_name = "product.html"

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    cartList = Cart.objects.filter(UserID=request.user)
    orderList = Order.objects.filter(UserID=request.user, ProductID=product.ProductID)

    if cartList.exists():
        cart = cartList[0]
        cart.TotalQuantity += 1
        cart.save()
        if orderList.exists():
            order = orderList[0]
            order.Quantity += 1
            order.save()
        else:
            Order.objects.create(UserID=request.user, ProductID=product, Quantity=1)
    else:
        Order.objects.create(UserID=request.user, ProductID=product, Quantity=1)
        Cart.objects.create(UserID=request.user, TotalQuantity=1)

    return redirect("items:details", slug=slug)
    
