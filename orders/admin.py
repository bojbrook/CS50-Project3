from django.contrib import admin

from .models import Toppings, Salads, Pasta
# Register your models here.

admin.site.register(Toppings)
admin.site.register(Salads)
admin.site.register(Pasta)