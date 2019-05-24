from django.db import models
from django.contrib.auth.models import User

from datetime import datetime    

# Create your models here.
class Toppings(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Pizza(models.Model):
    PIZZA_SIZES = (
        ('S', 'Small'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=64)
    pizza_size = models.CharField(max_length=1, choices=PIZZA_SIZES)
    toppings = models.ManyToManyField(Toppings,blank=True)
    pizza_price = models.FloatField()

    def __str__(self):
        str_toppings = ""
        for items in self.toppings.all():
            str_toppings += items.name + " - "
        return f"{self.name}: {str_toppings} {self.pizza_size}  - ${self.pizza_price}"

class dinnerTypes(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Food(models.Model):
    name = models.CharField(max_length=64)
    priceOfSmall = models.FloatField()
    priceOfLarge = models.FloatField()
    foodType = models.ForeignKey(dinnerTypes, on_delete=models.CASCADE, related_name="type")

    def __str__(self):
        if self.foodType == dinnerTypes.objects.get(name="Salads") or self.foodType == dinnerTypes.objects.get(name="Pasta"):
            return f"{self.name} Type: {self.foodType} - ${self.priceOfSmall:.2f}"
        else:
            return f"{self.name} Small: ${self.priceOfSmall:.2f}  Large: ${self.priceOfLarge:.2f}"


class menu_item(models.Model):
    SIZES = (
        ('S', 'Small'),
        ('L', 'Large'),
    )
    FOOD_TYPES = {
        ('DP', 'Dinner Platters'),
        ('SA', 'Salads'),
        ('PA', 'Pasta'),
        ('SU', 'Subs'),
        ('SP', 'Sicilian Pizza'),
        ('RP', 'Regular Pizza'),
    }
    name = models.CharField(max_length=64)
    price = models.FloatField()
    item_type = models.CharField(max_length=2, choices=FOOD_TYPES)
    item_size = models.CharField(max_length=2, choices=SIZES, blank=True)

    def __str__(self):
        return f"{self.name}: {self.get_item_type_display()} {self.item_size} - ${self.price:.2f}"

class shoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total =  models.FloatField(default=0.0)
    Items = models.ManyToManyField(menu_item)

    def __str__(self):
        return f"{self.user} - ${self.total:.2f}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_time = models.DateTimeField(default=datetime.now)
    is_completed = models.BooleanField(default=False)
    order_price = models.FloatField()
    order_items = models.ManyToManyField(menu_item)

    def get_items_str(self):
        items = ""
        for item in self.order_items.all():
            items += item.name + "\n"
        return items

    def __str__(self):
        return f"{self.user} - ${self.order_price} @ {self.order_time} Completed: {self.is_completed}"