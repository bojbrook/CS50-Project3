from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("cart", views.cart_view, name="cart"),
    path("add_to_cart/<int:menu_item_id>", views.add_to_cart, name="add_to_cart"),
    path("cart/remove_from_cart/<int:menu_item_id>", views.remove_from_cart, name="remove_from_cart"),
    path("orders", views.user_orders_view, name="user_orders"),

]
