from django.db import models
from django.contrib.auth.models import User

from datetime import datetime    


# ACTUAL MODELS THAT I'M CURRENTLY USING
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


#################################################################

class food_type(models.Model):
    name = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return f"{self.name}"

class topping(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    display_name = models.CharField(max_length=64)
    item_type = models.ManyToManyField(food_type, blank=True)

    def __str__(self):
        return f"{self.display_name}"

# Test for new database scheme
class common_food(models.Model):
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

    class Meta:
        abstract = True


class Food(models.Model):
    FOOD_TYPES = {
        ('DP', 'Dinner Platters'),
        ('SA', 'Salads'),
        ('PA', 'Pasta'),
        ('SU', 'Subs'),
        ('PI', 'Pizza'),
    }
    name = models.CharField(max_length=64)
    item_type = models.CharField(max_length=2, choices=FOOD_TYPES)
    price = models.FloatField()
    has_toppings = models.BooleanField(default=False)
    toppings = models.ManyToManyField(topping,blank=True)

    class Meta:
        abstract = False

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"

class Pizza(Food):
    SIZES = (
        ('S', 'Small'),
        ('L', 'Large'),
    )
    PIZZA_TYPE = {
        ('R', 'Regular'),
        ('S', 'Sicilian')
    }
    item_size = models.CharField(max_length=1, choices=SIZES)
    pizza_type = models.CharField(max_length=1, choices=PIZZA_TYPE)
    num_toppings = models.IntegerField()

    def set_price(self):
        self.price = self.calculate_price()
    

    def calculate_price(self):
        if self.item_size == "L":
            return self.price + (2 * self.num_toppings)
        else:
            if self.num_toppings == 2:
                return self.price + 2.5
            return self.price + (1 * self.num_toppings) + (.5 * (int)(self.num_toppings/3))


    def __str__(self):
        return f"{self.name} ${self.price:.2f} - {self.get_item_size_display()} {self.get_pizza_type_display()}"

class Sub(Food):
    SIZES = (
        ('S', 'Small'),
        ('L', 'Large'),
    )
    item_size = models.CharField(max_length=1, choices=SIZES)
    num_toppings = models.IntegerField(default=0)
    extra_cheese = models.BooleanField(default=False)

    def get_price(self):
        if self.has_toppings == True:
            return self.price + (.5 * self.num_toppings)
        return self.price

    def get_unique_name(self):
        return self.item_size +"_" + topping

    def __str__(self):
        return f"{self.name}: {self.get_item_size_display()} ${self.price:.2f} "

class Salad(Food):

    def __str__(self):
        return f"{self.name} ${self.price:.2f}"

class Pasta(Food):

    def __str__(self):
        return f"{self.name} ${self.price:.2f}"

class Dinner_Platter(Food):
    SIZES = (
        ('S', 'Small'),
        ('L', 'Large'),
    )
    item_size = models.CharField(max_length=1, choices=SIZES)

    def __str__(self):
        return f"{self.name}: {self.get_item_size_display()}  ${self.price:.2f}"


class shoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total =  models.FloatField(default=0.0)
    items = models.ManyToManyField(Food)


    def set_total(self):
        count = 0
        for item in self.items.all():
            count += item.price

        self.total = count
        return count

    def __str__(self):
        return f"{self.user} - ${self.set_total():.2f}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_time = models.DateTimeField(default=datetime.now)
    is_completed = models.BooleanField(default=False)
    order_price = models.FloatField()
    order_items = models.ManyToManyField(Food)

    def get_items_str(self):
        items = ""
        for item in self.order_items.all():
            items += item.name + "\n"
        return items

    def __str__(self):
        return f"{self.user} - ${self.order_price} @ {self.order_time} Completed: {self.is_completed}"