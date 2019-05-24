from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Toppings, Food, dinnerTypes, shoppingCart,Pizza, menu_item, Order
from datetime import datetime    

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
        return render(request, "orders/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})


def register_view(request):
    return render(request, "orders/register.html")

def add_user(request):
    email = request.POST["email"]
    username = request.POST["username"]
    password = request.POST["password"]
    print("I am in the add user")
    print(f"{email} - {username} password: {password}")
    if User.objects.filter(username=username).exists():
        print("already a user")
        return HttpResponseRedirect(reverse("register"))

    user = User.objects.create_user(username=username,email=email, password=password)
    return HttpResponseRedirect(reverse("index"))

# VIEW FOR THE SHOPPING CART
def cart_view(request):  
    current_user = request.user
    try:
        shopping_cart = shoppingCart.objects.filter(user=current_user)
    except shoppingCart.DoesNotExist:
        shopping_cart = shoppingCart(user= current_user, total = 0.0)
        shopping_cart.save()
    # creating new shopping cart
    if not shopping_cart:
        shopping_cart = shoppingCart(user= current_user, total = 0.0)
        shopping_cart.save()
    # updating the price for the cart
    else:
        shopping_cart = shopping_cart[0]
        cart_price = 0
        for food in shopping_cart.Items.all():
            cart_price += food.price
        shopping_cart.total = cart_price
        shopping_cart.save()

    context= {
        "cart": shopping_cart
    }
    return render(request,"orders/cart.html",context)

def user_orders_view(request):
    current_user = request.user
    try:
        orders = Order.objects.filter(user=current_user).order_by('-order_time')
    except Order.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No Orders."})
    for order in orders:
        print(order.user.username)
        items = ""
        for item in order.order_items.all():
            items += item.name + "-"
        print(items)
    context = {
        "orders": orders
    }
    return render(request,"orders/orders.html",context)

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

def submit_order(request, shopping_cart_id):
    print("submitting your order")
    current_user = request.user
    try:
        cart = shoppingCart.objects.get(pk=shopping_cart_id)
    except shoppingCart.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No Order."})
    print (cart.Items.all())
    order = Order(user=current_user, order_price=cart.total)
    order.save()
    order.order_items.set(cart.Items.all())

    # deleting the shopping cart
    cart.delete()
    
    
    return HttpResponseRedirect(reverse("index"))