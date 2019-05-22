from django.http import HttpResponse
from django.shortcuts import render

from .models import Toppings, Food, dinnerTypes

# Create your views here.
def index(request):
    context = {
        "toppings": Toppings.objects.all(),
        "foods": Food.objects.all(),
        "salads": Food.objects.filter(foodType=dinnerTypes.objects.get(name="Salads")),
        "regpizzas": Food.objects.filter(foodType=dinnerTypes.objects.get(name="Regular Pizza")),
        "sicpizzas": Food.objects.filter(foodType=dinnerTypes.objects.get(name="Sicilian Pizza")),
        "pastas" : Food.objects.filter(foodType=dinnerTypes.objects.get(name="Pasta")),
        "subs" : Food.objects.filter(foodType=dinnerTypes.objects.get(name="Subs")),
        "dinnerPlatters" : Food.objects.filter(foodType=dinnerTypes.objects.get(name="Dinner Platters"))

    }
    return render(request,"orders/index.html", context)
    