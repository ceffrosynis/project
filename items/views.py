from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Transaction, Cart, Order, Profile
from .forms import UserProfileForm

# Create your views here.

class Home(ListView):
    model = Product
    paginate_by = 1
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

class Checkout(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(self.request, "checkout.html")
        

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


@login_required
def remove_row(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    cartList = Cart.objects.filter(UserID=request.user)
    orderList = Order.objects.filter(UserID=request.user, ProductID=product.ProductID)

    if cartList.exists():
        if orderList.exists():
            order = orderList[0]
            cart = cartList[0]
            cart.TotalQuantity -= order.Quantity
            order.delete()
            cart.save()

    return redirect("items:cart_summary")




class UserProfile(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        checkProfile = Profile.objects.filter(UserID=request.user)
        if checkProfile.exists():
            form = UserProfileForm(initial={
                'Name': checkProfile[0].Name,
                'LastName': checkProfile[0].LastName,
                'CardID': checkProfile[0].CardID,
                'Address': checkProfile[0].Address,
                'Country': checkProfile[0].Country,
                })
        else:
            form = UserProfileForm()

        context = {
            'form': form
        }
        return render(self.request, "profile.html", context=context)
    
    def post(self, request, *args, **kwargs):
        form = UserProfileForm(self.request.POST or None)
        print("In post")
        if form.is_valid():
            print("The form is valid")
            checkProfile = Profile.objects.filter(UserID=request.user)
            if not checkProfile.exists():
                Name = form.cleaned_data.get('Name')
                LastName = form.cleaned_data.get('LastName')
                CardID = form.cleaned_data.get('CardID')
                Address = form.cleaned_data.get('Address')
                Country = form.cleaned_data.get('Country')
                Profile.objects.create(UserID=request.user, Name=Name, LastName=LastName, Address=Address, CardID=CardID, Country=Country)
            return redirect('items:home')

        form = UserProfileForm()
        context = {
            'form': form
        }

        return render(self.request, "profile.html", context=context)