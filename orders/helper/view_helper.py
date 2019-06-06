from ..models import order_item, topping, Order
FILE_NAME = "view_helper:"

def add_item_to_cart(shopping_cart,orderItem):
    print(f"Adding food {shopping_cart} and {orderItem}")
    orderItem.quantity += 1
    orderItem.save()
    shopping_cart.order_price += (orderItem.get_price())
    shopping_cart.save() 

# returns true
def check_order_items(order_filter,used_toppings):
    """[summary]
    Checks if an order_item exist and has the correct configuration of toppings
    Arguments:
        order_filter {Queryset<order_items>} -- A query set of order_items
        used_toppings {array} -- a lits of toppings being used 

    Returns:
        bool  -- return an True if it exists ortherwise returns False
    """
    print(len(set(topping.objects.filter(pk__in=used_toppings))))
    tops = topping.objects.filter(pk__in=used_toppings)
    for item in order_filter:
        orderItem = item
        if(set(item.toppings.all()) == set(tops)):
            print(f"print we have a match {item}")
            # orderItem = item
            return item
    return None

def create_new_sub(order,sub,price,toppings=[]):
    """[summary]
        Creates new order_item for a sub with its given toppings
    Arguments:
        order {order_item} -- order for the order_item to be added to
        food {food} -- food item that an order item is tied to
        price {Float} -- price of the food item
    
    Keyword Arguments:
        toppings {list} -- [description] (default: {[]})
    
    Returns:
        [type] -- [description]
    """
    orderItem = order_item(food=sub,order=order,price=price)
    orderItem.save()
    orderItem.toppings.set(toppings)
    return orderItem

def get_pizza_price(pizza,num_toppings):
    if pizza.size == "L" :
        return pizza.price + (2 * num_toppings)
    else:
        if num_toppings == 2:
            return pizza.price + 2.5
        return pizza.price + (1 * num_toppings) + (.5 * (int)(num_toppings/3))

def create_new_pizza(order,pizza,toppings=[]):
    price = get_pizza_price(pizza,len(toppings))
    orderItem = order_item(food=pizza,order=order,price=price)
    orderItem.save()
    orderItem.toppings.set(toppings)
    return orderItem