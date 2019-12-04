from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField

CATEGORIES = (
        ('T', 'Technology'),
        ('C', 'Comedy'),
        ('A', 'Adventure'),
        ('H', 'Horror'),
        ('R', 'Romance'),
        ('O', 'Other'),
        ('M', 'Mystery')
)

class Product(models.Model):
    ProductID = models.AutoField(primary_key=True)    
    ProductName = models.CharField(max_length=100)
    Price = models.FloatField()
    Discount = models.FloatField(blank=True, null=True)
    Description = models.TextField()
    Image = models.ImageField(default = 'default.png')
    Stock = models.IntegerField(default=1)
    slug = models.SlugField()
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ProductType = models.CharField(choices=CATEGORIES, max_length=1)

    def get_absolute_url(self):
        return reverse("items:details", kwargs={
                'slug': self.slug
        })

    def get_cart_url(self):
        return reverse("items:cart", kwargs={
                'slug': self.slug
        })

    def get_final_price(self):
        if self.Discount == 0:
            return self.Price
        else:
            return round(self.Price - self.Discount, 2)

    def __str__(self):
        return self.ProductName

class Transaction(models.Model):
    TransactionID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ProductID = models.ForeignKey(Product, on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.TransactionID)

class Order(models.Model):
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ProductID = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    Quantity = models.IntegerField(default=0)

    def get_price(self):
        if self.ProductID.Discount == 0:
            return self.ProductID.Price
        else:
            return round(self.ProductID.Price - self.ProductID.Discount, 2)

    def total_price(self):
        if self.ProductID.Discount is None:
            return self.ProductID.Price * self.Quantity
        else:
            return round((self.ProductID.Price - self.ProductID.Discount), 2) * self.Quantity

    def __str__(self):
        return str(self.ProductID)

class Cart(models.Model):
    CartID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    TotalQuantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.CartID)

    
    
class Profile(models.Model):
    UserID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    CardID = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    Country = CountryField()
    

    def __str__(self):
        return str(self.UserID)