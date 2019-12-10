from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Transaction, Cart, Order, Profile
from .forms import UserProfileForm, InsertProductForm, Filter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

class Home(View):
      
    categories = ['Technology', 'Comedy', 'Adventure', 'Horror', 'Romance', 'Other', 'Mystery']
    visible = {'Technology': True, 'Comedy': True, 'Adventure': True, 'Horror': True, 'Romance': True, 'History': True, 'Mystery': True}
    choices = ('T', 'C', 'A', 'H', 'R', 'O', 'M',)

    def get(self, request, *args, **kwargs):

        if 'visible' not in request.session:
            request.session['visible'] = {'Technology': True, 'Comedy': True, 'Adventure': True, 'Horror': True, 'Romance': True, 'History': True, 'Mystery': True}
        
        if 'choices' not in request.session:
            request.session['choices'] = ('T', 'C', 'A', 'H', 'R', 'O', 'M',)

        choices = request.session['choices']
        visible = request.session['visible']

        model = Product.objects.filter(ProductType__in=choices)
        
        paginator = Paginator(model, 4)

        page = request.GET.get('page', 1)
        try :
            offset = paginator.page(page)
        except PageNotAnInteger:
            offset = paginator.page(1)
        except EmptyPage:
            offset = paginator.page(paginator.num_pages)

        form = Filter(request.POST or None, initial=visible)
        context = {
            'form': form,
            'page_obj': offset,
        }
        return render(self.request, "home.html", context=context)

    def post(self, request, *args, **kwargs):
        
        visible = request.session['visible']
        choices=()
        form = Filter(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                for category in self.categories:
                    if not category in request.POST:
                        visible[category] = False
                    else:
                        choices += (category[0],)
                        visible[category] = True
                print(self.choices)

                form = Filter(request.POST, initial=visible)
                model = Product.objects.filter(ProductType__in=choices)
                paginator = Paginator(model, 4)

                request.session['visible'] = visible
                request.session['choices'] = choices

                page = request.GET.get('page', 1)
                try :
                    offset = paginator.page(page)
                except PageNotAnInteger:
                    offset = paginator.page(1)
                except EmptyPage:
                    offset = paginator.page(paginator.num_pages)
                
                context = {
                    'form': form,
                    'page_obj': offset,
                }
                return render(self.request, "home.html", context=context)
        
        return redirect('items:home') 

class Details(DetailView):
    model = Product
    template_name = "product.html"

class CartSummary(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.filter(UserID=request.user)
            total = 0
            for product in order:
                total += product.total_price()

            context = {
                'object': order,
                'total': total
                }

            return render(self.request, "cart_summary.html", context=context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have any order")
            return redirect("/")

class Checkout(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(UserID=request.user)
        if profile.exists():
            try:
                order = Order.objects.filter(UserID=request.user)
            
                total = 0
                for product in order:
                    total += product.total_price()

                context = {
                    'profile': profile,
                    'object': order,
                    'total': total
                }
                return render(self.request, "checkout.html", context=context)

            except ObjectDoesNotExist:
                return redirect("/")
        else:
            return redirect("items:profile")
        

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    cartList = Cart.objects.filter(UserID=request.user)
    orderList = Order.objects.filter(UserID=request.user, ProductID=product.ProductID)

    if cartList.exists():
            cart = cartList[0]
            cart.TotalQuantity += 1
            if orderList.exists():
                order = orderList[0]
                order.Quantity += 1
                if order.Quantity <= product.Stock:
                    order.save()
                    cart.save()
            else:
                Order.objects.create(UserID=request.user, ProductID=product, Quantity=1)
                cart.save()
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
            cart.save()
            order.delete()

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
        if form.is_valid():
            checkProfile = Profile.objects.filter(UserID=request.user)
            Name = form.cleaned_data.get('Name')
            LastName = form.cleaned_data.get('LastName')
            CardID = form.cleaned_data.get('CardID')
            Address = form.cleaned_data.get('Address')
            Country = form.cleaned_data.get('Country')
            if checkProfile.exists():
                checkProfile.delete()
            Profile.objects.create(UserID=request.user, Name=Name, LastName=LastName, Address=Address, CardID=CardID, Country=Country)
            return redirect('items:home')

        form = UserProfileForm()
        context = {
            'form': form
        }

        return render(self.request, "profile.html", context=context)



class AddProduct(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = InsertProductForm(self.request.POST, self.request.FILES)
        context = {
            'form': form,
            'valid': 'true'
        }
        return render(self.request, "add_product.html", context=context)


    def post(self, request, *args, **kwargs):
        form = InsertProductForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            slug = form.cleaned_data.get('slug')
            checkSlug = Product.objects.filter(slug=slug)
            if checkSlug.exists():
                context = {
                    'form': form,
                    'valid': 'false'
                }
                return render(self.request, "add_product.html", context=context)
            else:
                ProductName = form.cleaned_data.get('ProductName')
                Price = form.cleaned_data.get('Price')
                Discount = form.cleaned_data.get('Discount')
                Description = form.cleaned_data.get('Description')
                Image = form.cleaned_data.get('Image')
                Stock = form.cleaned_data.get('Stock')
                slug = form.cleaned_data.get('slug')
                ProductType = form.cleaned_data.get('ProductType')
                Product.objects.create(ProductName=ProductName, Price=Price, Discount=Discount,
                            Description=Description, Image=Image, Stock=Stock,
                            slug=slug, ProductType=ProductType, UserID=request.user)
                
 
                return redirect('items:home')


@login_required
def completion(request):
    orderList = Order.objects.filter(UserID=request.user)
    cartList = Cart.objects.filter(UserID=request.user)
    if cartList.exists():
        if orderList.exists():
            for order in orderList:
                cart = cartList[0]
                cart.TotalQuantity -= order.Quantity
                cart.save()
                order.delete()
                if order.ProductID.Stock - order.Quantity == 0:
                    product = get_object_or_404(Product, ProductID=order.ProductID.ProductID)
                    product.delete()
                else:
                    product = get_object_or_404(Product, ProductID=order.ProductID.ProductID)
                    product.Stock -= order.Quantity
                    product.save()


    return redirect('items:home')
