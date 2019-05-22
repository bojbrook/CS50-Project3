from django.http import HttpResponse
from django.shortcuts import render

from .models import Toppings, Food,dinnerTypes

# Create your views here.
def index(request):
    context = {
        "toppings": Toppings.objects.all(),
        "foods": Food.objects.all(),
        "salads": Food.objects.filter(foodType=dinnerTypes.objects.get(name="Salad")),
        "pastas" : Food.objects.filter(foodType=dinnerTypes.objects.get(name="Pasta"))

    }
    return render(request,"orders/index.html", context)