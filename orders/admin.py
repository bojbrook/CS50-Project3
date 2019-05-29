from django.contrib import admin

from .models import shoppingCart, menu_item, Order, topping, Salad, Pasta, Dinner_Platter, Sub,food_type
# Register your models here.

admin.site.register(topping)
admin.site.register(shoppingCart)
admin.site.register(menu_item)
admin.site.register(Order)
admin.site.register(Salad)
admin.site.register(Pasta)
admin.site.register(Dinner_Platter)
admin.site.register(Sub)
admin.site.register(food_type)

