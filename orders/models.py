from django.db import models
from django.contrib.auth.models import User

from datetime import datetime    



#################################################################

# Used for toppings
class food_type(models.Model):
    name = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return f"{self.name}"

# Base model for all the food types
class Food(models.Model):
    FOOD_TYPES = {
        ('DP', 'Dinner Platters'),
        ('SA', 'Salads'),
        ('PA', 'Pasta'),
        ('SU', 'Sub'),
        ('PI', 'Pizza'),
    }
    name = models.CharField(max_length=64)
    display_name = models.CharField(max_length = 64)
    price = models.FloatField()
    item_type = models.CharField(max_length=2, choices=FOOD_TYPES)
    has_toppings = models.BooleanField(default=False)

    class Meta:
        abstract = False

    # returns specific food item based on its id
    def get_food(self):
        if self.item_type == "PI":
            return Pizza.objects.get(pk = self.id)
        if self.item_type == "SU":
            return Sub.objects.get(pk = self.id)
        if self.item_type == "PA":
            return Pasta.objects.get(pk = self.id)
        if self.item_type == "SA":
            return Salad.objects.get(pk = self.id)
        if self.item_type == "DP":
            return Dinner_Platter.objects.get(pk = self.id)

    # prints out different strings for each food item
    def food_print(self):
        if self.item_type == "PI":
            pizza = self.get_food()
            return f"{self.get_item_type_display()} {self.display_name} ${self.price:.2f} - {pizza.get_item_size_display()} {pizza.get_pizza_type_display()}"
        if self.item_type == "SU":
            sub = self.get_food()
            return f"{self.display_name}: {sub.get_item_size_display()} ${self.price:.2f} "
        if self.item_type == "PA":
            pasta = self.get_food()
            return f"{self.name} ${self.price:.2f}"
        if self.item_type == "SA":
            salad = self.get_food()
            return f"{self.name} ${self.price:.2f}"
        if self.item_type == "DP":
            platter = self.get_food()
            return f"{self.display_name}: {platter.get_item_size_display()}  ${self.price:.2f}"

    # return the price of the food with all of its toppings
    def get_price(self):
        if(self.item_type != "PI"):
            topping_price = 0
            for topping in self.toppings.all():
                topping_price += topping.price
            return self.price + topping_price
        else:
            return self.price
   
    def __str__(self):
        # return self.food_print()
        return f"{self.get_item_type_display()} {self.name}"

class order_item(models.Model):
    food = models.ForeignKey(Food,on_delete=models.CASCADE)
    order = models.ForeignKey('Order',on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)
    toppings = models.ManyToManyField("topping",blank=True)
    quantity = models.IntegerField(default=0)

    def get_price(self):
        total_price = self.price
        for top in self.toppings.all():
            total_price += top.price
        return total_price

    def __str__(self):
        return f"{self.food.name} {self.toppings.all()} {self.quantity} ${self.get_price():.2f}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    order_price = models.FloatField(default=0.0)
    order_items = models.ManyToManyField(Food, through=order_item)
    has_paid = models.BooleanField(default=False)
    
    def get_items_str(self):
        items = ""
        for item in self.order_items.all():
            items += item.name + "\n"
        return items

    def __str__(self):
        return f"{self.user} - ${self.order_price:.2f}"

class topping(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    display_name = models.CharField(max_length=64)
    item_type = models.ManyToManyField(food_type, blank=True)
    price = models.FloatField(default=0.50)
    # Used for keeping track of where each topping is going
    orders = models.ManyToManyField(Order,blank=True)
    food_items = models.ManyToManyField(Food,blank=True)


    def __str__(self):
        return f"{self.display_name}"

class Pizza(Food):
    SIZES = (
        ('S', 'Small'),
        ('L', 'Large'),
    )
    PIZZA_TYPE = {
        ('R', 'Regular'),
        ('S', 'Sicilian')
    }
    size = models.CharField(max_length=1, choices=SIZES)
    pizza_type = models.CharField(max_length=1, choices=PIZZA_TYPE)
    num_toppings = models.IntegerField()

    def set_price(self):
        self.price = self.calculate_price()
    
    def calculate_price(self):
        if self.size == "L":
            return self.price + (2 * self.num_toppings)
        else:
            if self.num_toppings == 2:
                return self.price + 2.5
            return self.price + (1 * self.num_toppings) + (.5 * (int)(self.num_toppings/3))

    def __str__(self):
        return f"{self.get_item_type_display()} {self.name} ${self.price:.2f} - {self.get_size_display()} {self.get_pizza_type_display()}"

class Sub(Food):
    SIZES = (
        ('S', 'Small'),
        ('L', 'Large'),
    )
    size = models.CharField(max_length=1, choices=SIZES,blank=True)
    extra_cheese = models.BooleanField(default=False)

    def get_extra_charge_total(self):
        return .5 * self.num_toppings

    def get_unique_name(self):
        return self.item_size +"_"+self.name

    def get_toppings_str(self):
        if(self.has_toppings):
            items = ""
            for item in self.toppings.all():
                items += item.name + "-"
            return items
   
    def __str__(self):
        # if(self.has_toppings):
        #     return f"{self.name}: {self.get_toppings_str()} {self.get_item_size_display()} ${self.get_price():.2f}"
        return f"{self.display_name} {self.get_size_display()} ${self.price:.2f}"

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
    size = models.CharField(max_length=1, choices=SIZES)

    def __str__(self):

        return f"{self.display_name}: {self.get_size_display()}  ${self.price:.2f}"

class shoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total =  models.FloatField(default=0.0)
    items = models.ManyToManyField(Food)
    extra_charge = models.FloatField(default=0.0)


    def set_total(self):
        count = 0
        for item in self.items.all():
            count += item.price

        self.total = count
        return count

    def get_total(self):
        total = self.set_total()
        return total + self.extra_charge

    def __str__(self):
        return f"{self.user} - ${self.get_total():.2f}"




