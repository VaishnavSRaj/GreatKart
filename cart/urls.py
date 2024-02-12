from django.urls import path
from . import views


urlpatterns = [
    path("", views.cart, name="cart"),
    path("add_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove_cart/<int:product_id>/<int:cart_item_id>/", views.remove_cart, name="remove_cart"),
    path("delete_item/<int:product_id>/<int:cart_item_id>/", views.delete_cart_item, name="delete_cart_item"),
   
]
