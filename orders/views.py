from django.http import HttpResponse
from django.shortcuts import render

from .models import Toppings, Salads, Pasta

# Create your views here.
def index(request):
    context = {
        "toppings": Toppings.objects.all(),
        "salads": Salads.objects.all(),
        "pastas": Pasta.objects.all()
    }
    return render(request,"orders/index.html", context)