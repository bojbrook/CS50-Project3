from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

from .models import  shoppingCart,Order,topping, Pizza, Salad, Pasta, Dinner_Platter, Sub, Food
from datetime import datetime    

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
          return render(request, "orders/login.html", {"message": None})
    context = {
        "toppings": topping.objects.all().order_by("name"),
        "sub_toppings": topping.objects.filter(item_type="Subs").all(),
        "salads": Salad.objects.all(),
        "pastas" : Pasta.objects.all(),
        "subs_no_toppings" : Sub.objects.exclude(has_toppings=True).all(),
        "subs_w_toppings" : Sub.objects.exclude(has_toppings=False).all(),  
        "dinnerPlatters" : Dinner_Platter.objects.all()

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
        for food in shopping_cart.items.all():
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


def create_pizza(request):
    #Getting Items from POST
    topping_1 = request.POST["topping1"]
    topping_2 = request.POST["topping2"]
    topping_3 = request.POST["topping3"]
    order_size = request.POST["rb_size"]
    
    name_str= "Cheese"
    count = 0
    
    if(topping_1 != "NONE"):
        topping_item_1 = topping.objects.get(pk=topping_1)
        name_str += " + " + topping_item_1.display_name
        count+=1
    if(topping_2 != "NONE"):
        topping_item_2 = topping.objects.get(pk=topping_2)
        name_str += " + " + topping_item_2.display_name
        count+=1
    if(topping_3 != "NONE"):
        topping_item_3 = topping.objects.get(pk=topping_3)
        name_str += " + " + topping_item_3.display_name
        count+=1

    # Creating the pizza
    if(order_size == 'L'):
        p = Pizza(name = name_str, item_size = order_size, num_toppings=count, item_type="RP", price=17.45)
    else:
        p = Pizza(name = name_str, item_size = order_size, num_toppings=count, item_type="RP", price=12.20)
    p.set_price()
    p.save()
    if(count == 1):
        p.toppings.add(topping_item_1)
    elif count == 2:
        p.toppings.add(topping_item_1,topping_item_2)
    else:
        p.toppings.add(topping_item_1,topping_item_2,topping_item_3)
    print(p)  
    p.save()
    return HttpResponseRedirect(reverse("add_to_cart",kwargs={'food_id':p.id}))

# function to add item to cart
def add_to_cart(request, food_id):
    print ("adding item to cart")

    try:
        current_user = request.user
        item = Food.objects.get(pk=food_id)
        print(item)
        shopping_cart = shoppingCart.objects.filter(user=current_user).first()
    except Food.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No selection."})
    except shoppingCart.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No shopping cart."})

    if shopping_cart == None:
        sc = shoppingCart(user=current_user)
        sc.save()

    # Checking if food is a sub
    if(item.item_type == "SU"):
        if(item.has_toppings == True):
            sub_toppings = topping.objects.filter(item_type="Subs").all()
            sub = Sub.objects.filter(name=item.name).first()
            print(sub)
            # getting all of the options for subs with toppings
            for top in sub_toppings:
                name = sub.item_size+ "_"+  top.name
                print(request.POST[name])
    # shopping_cart = shoppingCart.objects.filter(user=current_user).first()
    # shopping_cart.items.add(item)
    return HttpResponseRedirect(reverse("index"))

# function to remove item from cart
def remove_from_cart(request, food_id):
    print ("removing item from cart")
    try:
        current_user = request.user
        item = Food.objects.get(pk=food_id)
        shopping_cart = shoppingCart.objects.filter(user=current_user).first()
    except menu_item.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No selection."})
    except shoppingCart.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No shopping cart."})

    new_cart = shopping_cart.items.exclude(pk=food_id)
    shopping_cart.items.set(new_cart)
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
    print (cart.items.all())
    order = Order(user=current_user, order_price=cart.total)
    order.save()
    order.order_items.set(cart.items.all())

    # deleting the shopping cart
    cart.delete()
    
    
    return HttpResponseRedirect(reverse("index"))