from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Toppings, Food, dinnerTypes, shoppingCart,Pizza, menu_item

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
          return render(request, "orders/login.html", {"message": None})
    context = {
        "toppings": Toppings.objects.all(),
        "foods": Food.objects.all(),
        "salads": menu_item.objects.filter(item_type="SA"),
        # "regpizzas": Food.objects.filter(foodType=dinnerTypes.objects.get(name="Regular Pizza")),
        "regpizzas": Pizza.objects.all(),
        "sicpizzas": Food.objects.filter(foodType=dinnerTypes.objects.get(name="Sicilian Pizza")),
        "pastas" : menu_item.objects.filter(item_type="PA"),
        "subs" : menu_item.objects.filter(item_type="SU"),
        "dinnerPlatters" : menu_item.objects.filter(item_type="DP")

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
            cart_price += food.price
    shopping_cart[0].total = cart_price
    shopping_cart[0].save()
    
    context= {
        "cart": shopping_cart
    }
    return render(request,"orders/cart.html",context)

# function to add item to cart
def add_to_cart(request, menu_item_id):
    print ("adding item to cart")
    try:
        current_user = request.user
        item = menu_item.objects.get(pk=menu_item_id)
        shopping_cart = shoppingCart.objects.filter(user=current_user)
    except menu_item.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No selection."})
    except shoppingCart.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No shopping cart."})
    shopping_cart[0].Items.add(item)
    return HttpResponseRedirect(reverse("index"))

# function to remove item from cart
def remove_from_cart(request, menu_item_id):
    print ("removing item from cart")
    try:
        current_user = request.user
        item = menu_item.objects.get(pk=menu_item_id)
        shopping_cart = shoppingCart.objects.filter(user=current_user)[0]
    except menu_item.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No selection."})
    except shoppingCart.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No shopping cart."})

    new_cart = shopping_cart.Items.exclude(pk=menu_item_id)
    shopping_cart.Items.set(new_cart)
    # shopping_cart.save()
    print(new_cart)
    # shopping_cart[0].Items.add(item)
    return HttpResponseRedirect(reverse("cart"))