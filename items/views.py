from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Transaction, Cart, Order

# Create your views here.

class Home(ListView):
    model = Product
    template_name = "home.html"

class Details(DetailView):
    model = Product
    template_name = "product.html"

class CartSummary(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.filter(UserID=request.user)
            context = {'object': order}

            return render(self.request, "cart_summary.html", context=context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have any order")
            return redirect("/")

@login_required
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

    return redirect("items:cart_summary")


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    cartList = Cart.objects.filter(UserID=request.user)
    orderList = Order.objects.filter(UserID=request.user, ProductID=product.ProductID)

    if cartList.exists():
        if orderList.exists():
            order = orderList[0]
            if order.Quantity > 1:
                order.Quantity -= 1
                order.save()
            else:
                order.delete()
            cart = cartList[0]
            cart.TotalQuantity -= 1
            cart.save()

    return redirect("items:cart_summary")
    
