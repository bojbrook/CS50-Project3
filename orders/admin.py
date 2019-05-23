from django.contrib import admin

from .models import Toppings, shoppingCart, Pizza, menu_item, Order
# Register your models here.

admin.site.register(Toppings)
admin.site.register(shoppingCart)
admin.site.register(Pizza)
admin.site.register(menu_item)
admin.site.register(Order)