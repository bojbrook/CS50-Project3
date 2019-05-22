from django.contrib import admin

from .models import Toppings, dinnerTypes, Food
# Register your models here.

admin.site.register(Toppings)
admin.site.register(dinnerTypes)
admin.site.register(Food)