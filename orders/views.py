from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Toppings, Food, dinnerTypes, shoppingCart,Pizza

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
          return render(request, "orders/login.html", {"message": None})
    context = {
        "toppings": Toppings.objects.all(),
        "foods": Food.objects.all(),
        "salads": Food.objects.filter(foodType=dinnerTypes.objects.get(name="Salads")),
        # "regpizzas": Food.objects.filter(foodType=dinnerTypes.objects.get(name="Regular Pizza")),
        "regpizzas": Pizza.objects.all(),
        "sicpizzas": Food.objects.filter(foodType=dinnerTypes.objects.get(name="Sicilian Pizza")),
        "pastas" : Food.objects.filter(foodType=dinnerTypes.objects.get(name="Pasta")),
        "subs" : Food.objects.filter(foodType=dinnerTypes.objects.get(name="Subs")),
        "dinnerPlatters" : Food.objects.filter(foodType=dinnerTypes.objects.get(name="Dinner Platters"))

    }
    return render(request,"orders/index.html", context)
    

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})

# VIEW FOR THE SHOPPING CART
def cart_view(request):
    
    current_user = request.user
    shopping_cart = shoppingCart.objects.filter(user=current_user)
    
    # updating the price for the cart
    cart_price = 0
    for item in shopping_cart:
        for food in item.Items.all():
            cart_price += food.priceOfSmall
    shopping_cart[0].total = cart_price
    shopping_cart[0].save()
    
    context= {
        "cart": shopping_cart
    }
    return render(request,"orders/cart.html",context)