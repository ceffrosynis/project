from django.db import models
from django.conf import settings

# Create your models here.

CATEGORIES = (
        ('S', 'Shirt'),
        ('SW', 'Sport Wear'),
        ('O', 'Outwear')
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()

    category = models.CharField(choices=CATEGORIES, max_length=2)

    def __str__(self):
        return self.title

class OrderItem(models.Model):
    pass

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)

    ordered_date = models.DateTimeField()

    
    
