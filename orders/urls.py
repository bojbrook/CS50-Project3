from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("register/add_user", views.add_user, name="add_user"),

    path("place_order", views.place_order, name="place_order"),
    path("place_order/create_sub/<slug:sub_name>", views.create_sub, name="create_sub"),
    path("place_order/create_platter/<slug:platter_name>", views.create_platter, name="create_platter"),
    path("place_order/create_pizza", views.create_pizza, name="create_pizza"),


    path("cart", views.cart_view, name="cart"),
    path("cart/add_to_cart/<int:food_id>", views.add_to_cart, name="add_to_cart"),
    path("cart/remove_from_cart/<int:food_id>", views.remove_from_cart, name="remove_from_cart"),

    path("orders", views.user_orders_view, name="user_orders"),
    path("orders/submit_order/<int:shopping_cart_id>", views.submit_order, name="submit_order"),

]
