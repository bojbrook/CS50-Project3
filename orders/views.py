from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

from .models import  shoppingCart,Order,topping, Pizza, Salad, Pasta, Dinner_Platter, Sub, Food, order_item
from datetime import datetime    

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
          return render(request, "orders/login.html", {"message": None})

    dinner_platters = Dinner_Platter.objects.all()
    names = Dinner_Platter.objects.values('name').distinct()
    temp = [] 
    count = 0
    for dp in names:
        platter =  Dinner_Platter.objects.filter(name = dp['name'])
        large = 0.0
        small = 0.0
        for plat in platter:
            if plat.item_size == 'S':
                small = plat.price
            else:
                large = plat.price
        dick = {
            'name': dp['name'],
            'p_small': small,
            'p_large': large
        }
        temp.append(dick)
        count += 1
        # print (f"Large: {large} Small: {small}")
        # print (temp)


    context = {
        "toppings": topping.objects.all().order_by("name"),
        "sub_toppings": topping.objects.filter(item_type="Subs").all(),
        "salads": Salad.objects.all(),
        "pastas" : Pasta.objects.all(),
        "subs_no_toppings" : Sub.objects.exclude(has_toppings=True).all(),
        "subs_w_toppings" : Sub.objects.exclude(has_toppings=False).all(),  
        "dinnerPlatters" : Dinner_Platter.objects.all(),
    }
    return render(request,"orders/index.html", context)
    
# VIEW FOR THE LOGIN PAGE
def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})

# LOGS THE CURRENT USER
def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})

# VIEW FOR REGISTERING A NEW USER
def register_view(request):
    return render(request, "orders/register.html")

# ADDS A USER FROM register_view()
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

# view for the place order page, where the user can add items to their cart
def place_order(request):
    context = {
        "toppings": topping.objects.all().order_by("name"),
        "sub_toppings": topping.objects.filter(item_type="Sub").all(),
        "sub_no_topping": Sub.objects.exclude(has_toppings=True).values('name','display_name').distinct(),
        "sub_w_topping": Sub.objects.exclude(has_toppings=False).values('name','display_name').distinct(),
        "pastas" : Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "dinner_platters": Dinner_Platter.objects.values('name','display_name').distinct()
    }
    return render(request,"orders/place_order.html", context)

# VIEW FOR THE SHOPPING CART
def cart_view(request):  
    current_user = request.user
    try:
        shopping_cart = Order.objects.get(user=current_user,has_paid=False)
        toppings = topping.objects.filter(orders=shopping_cart)
        orderItems = order_item.objects.filter(order=shopping_cart)    
    except Order.DoesNotExist:
        shopping_cart = Order(user=current_user)
        shopping_cart.save()
    except topping.DoesNotExist:
        pass
    except orderItems.DoesNotExist:
        pass
   
    # Gatthering all of the toppings for a specific item
    cart = []
    for item in orderItems.all():
        cart_items = {
            'item': item.food,
            "toppings":item.toppings.all(),
            "price": item.get_price(),
            "quantity": item.quantity     
        }
        cart.append(cart_items)
    
    context= {
        "shopping_cart": shopping_cart,
        "cart": cart,
        "toppings": toppings
    }
    return render(request,"orders/cart.html",context)

def user_orders_view(request):
    current_user = request.user
    try:
        orders = Order.objects.filter(user=current_user, has_paid=True).order_by('-created')
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

# Creates a pizza from the place order page and adds it to the shopping cart
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
        p = Pizza(name = name_str, display_name=name_str,item_size = order_size, num_toppings=count, item_type="PI", price=17.45)
    else:
        p = Pizza(name = name_str, display_name=name_str, item_size = order_size, num_toppings=count, item_type="PI", price=12.20)
    p.set_price()
    p.save()
    if(count == 1):
        p.toppings.add(topping_item_1)
    elif count == 2:
        p.toppings.add(topping_item_1,topping_item_2)
    elif count == 3:
        p.toppings.add(topping_item_1,topping_item_2,topping_item_3)
 
    p.save()
    return HttpResponseRedirect(reverse("add_to_cart",kwargs={'food_id':p.id}))

# Creates a sub and toppings and add sit to the shopping cart
def create_sub(request, sub_name):
    size_str = str(sub_name+"_size")
    x_cheese_str = str(sub_name+"_extra_cheese")

    # getting items from html form
    size = request.POST[size_str]
    x_cheese = request.POST.get(x_cheese_str)

    try:
        current_user = request.user
        sub = Sub.objects.get(name=sub_name,size=size)
        shopping_cart = Order.objects.get(user=current_user,has_paid=False)
        # orderItem = order_item.objects.filter(food=sub,order=shopping_cart)
    except Sub.DoesNotExist:
        return render(request, "orders/error.html", {"message": "Something went wrong with adding the sub."})
    except Order.DoesNotExist:
        shopping_cart = Order(user= current_user, order_price = 0.0, has_paid=False)
        shopping_cart.save()
  
    # Getting the Cheese and toppings for each sub
    current_toppings = []
    cheese = None
    if(x_cheese == 'on'):
        cheese = topping.objects.get(name="Extra_Cheese")
        mush = topping.objects.get(name='Mushrooms')
        current_toppings.append(cheese)
    if(sub.has_toppings == True):
        # print("Sub has toppings")
        sub_toppings = topping.objects.filter(item_type="Sub").all()
        for top in sub_toppings:
            input_name = f"{sub.name}_{top.name}"
            # checks if box has been checked then modifies the topping 
            if(request.POST.get(input_name)):
                current_toppings.append(top)
    
    
    print(f"toppings: {current_toppings}") 
    # print(cheese)
    try:
        if current_toppings:
            orderItem = order_item.objects.get(food=sub,order=shopping_cart,toppings__in=current_toppings)
        else:
            orderItem = order_item.objects.filter(food=sub,order=shopping_cart,toppings=None).first()
        # orderItem = order_item.objects.get(food=sub,order=shopping_cart, toppings__in=current_toppings)
        
        print(f"test: {orderItem}")
    except order_item.DoesNotExist:
        orderItem = order_item(food=sub,order =shopping_cart,price=sub.price)
        orderItem.save()
        orderItem.toppings.set(current_toppings)
        print("Does not exist")

    # print(f"test: {test}")
    if not orderItem:
        print("Creating Item")
        orderItem = order_item(food=sub,order =shopping_cart,price=sub.price)
        orderItem.save()
        orderItem.toppings.set(current_toppings)
        

    print(orderItem)
    add_food_to_cart(shopping_cart,orderItem)
    
    # if(sub.has_toppings == True):
    #     # print("Sub has toppings")
    #     sub_toppings = topping.objects.filter(item_type="Sub").all()
    #     for top in sub_toppings:
    #         input_name = f"{sub.name}_{top.name}"
    #         # checks if box has been checked then modifies the topping
    #         if(request.POST.get(input_name)):
    #             orderItem.toppings.add(top)
    #             orderItem.save()

    # if(x_cheese == 'on'):
    #     cheese = topping.objects.get(name="Extra_Cheese")
    #     print(orderItem.toppings.all())
    #     order_topping = orderItem.toppings.all()
    #     print(f"toppings: {order_topping}")
    #     if(cheese not in order_topping):
    #         new_order_item = order_item(food=sub,order=shopping_cart,price=sub.price) 
    #         new_order_item.save()
    #         new_order_item.toppings.add(cheese)


        # new_order_item = order_item()
        # cheese = topping.objects.get(name="Extra_Cheese")
        # orderItem.toppings.add(cheese)
        # orderItem.save()
    
    return HttpResponseRedirect(reverse("place_order"))
    # return HttpResponseRedirect(reverse("add_to_cart",kwargs={'food_id':sub.id}))

def add_food_to_cart(shopping_cart,orderItem):
    print(f"Adding food {shopping_cart} and {orderItem}")
    orderItem.quantity += 1
    orderItem.save()
    shopping_cart.order_price += (orderItem.get_price())
    shopping_cart.save() 

# Creates a dinner platter and adds it to the shopping cart
def create_platter(request, platter_name):
    size_str = str(platter_name+"_size")
    size = request.POST[size_str]
    try:
        platter = Dinner_Platter.objects.get(name=platter_name,item_size=size)
    except Dinner_Platter.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No Platter."})
    
    return HttpResponseRedirect(reverse("add_to_cart",kwargs={'food_id':platter.id}))

# function to add item to cart that don't require any special selection
def add_to_cart(request, food_id):
    print ("adding item to cart")

    try:
        current_user = request.user
        item = Food.objects.get(pk=food_id)
        # print(item)
        shopping_cart = Order.objects.get(user=current_user,has_paid=False)
        orderItem = order_item.objects.filter(food=item,order=shopping_cart)       
    except Food.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No selection."})
    except Order.DoesNotExist:
        shopping_cart = Order(user= current_user, order_price = 0.0, has_paid=False)
        shopping_cart.save()
    except order_item.DoesNotExist:
        orderItem = order_item(food=item, order=shopping_cart, price=item.price)
        orderItem.save()

    print(orderItem)

    orderItem.quantity += 1
    orderItem.save()

    #     # Checking if food is a sub and had toppings
    # if(item.item_type == "SU"):
    #     sub = Sub.objects.get(pk=food_id)
    #     # if(sub.extra_cheese == True):
    #     #     cheese_topping = topping.objects.get(name="Extra_Cheese")
    #     #     orderItem.toppings.add(cheese_topping)
    #     #     #add the extra price to the cart
    #     #     orderItem.save()

    # # print((orderItem.price * orderItem.quantity))
    # print(orderItem.get_price())
    shopping_cart.order_price += (orderItem.get_price())
    shopping_cart.save()  
    return HttpResponseRedirect(reverse("place_order"))

# function to remove item from cart
def remove_from_cart(request, food_id):
    print ("removing item from cart")
    try:
        current_user = request.user
        item = Food.objects.get(pk=food_id)
        shopping_cart = Order.objects.get(user=current_user,has_paid=False)
        orderItem = order_item.objects.get(order=shopping_cart,food=item)
        
    except Food.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No selection."})
    except Order.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No shopping cart."})
    except order_item.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No Item in cart."})


    orderItem.quantity -= 1
    orderItem.save()

    # removing the toppings from the cart
    # try:
    #     toppings = topping.objects.filter(orders=shopping_cart, food_items = item)
    #     for top in toppings:
    #         shopping_cart.order_price -= top.price
    #         top.orders.remove(shopping_cart)
    #         top.food_items.remove(item)
        
    # except:
    #     pass

    # new_cart = shopping_cart.order_items.exclude(pk=food_id)
    # shopping_cart.order_items.set(new_cart)
    # print(orderItem.price)
    shopping_cart.order_price -= (orderItem.get_price())
    if(orderItem.quantity == 0):
        orderItem.delete()
    
    shopping_cart.save()
    return HttpResponseRedirect(reverse("cart"))

# Submits a schopping cart order to an actual order
def submit_order(request, shopping_cart_id):
    print("submitting your order")
    current_user = request.user
    try:
        cart = Order.objects.get(pk=shopping_cart_id)
    except shoppingCart.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No Order."})
    print (cart.order_items.all())
    
    cart.has_paid = True
    cart.save()
    
    return HttpResponseRedirect(reverse("index"))