from django.urls import path

from cart import views

app_name = "cart"

urlpatterns = [
    path("", views.CartSummaryView.as_view(), name="cart_summary"),
    path("get_cart_items/", views.CartItemsView.as_view(), name="get_cart_items"),


    path("add_to_cart/", views.AddToCartView.as_view(), name="add_to_cart"),
    path("clear_cart/", views.ClearCartView.as_view(), name="clear_cart"),
    path("update_cart_quantity/", views.CartUpdateQuantityView.as_view(), name="update_cart_quantity"),
    path("delete_cart_item/", views.CartDeleteItemView.as_view(), name="delete_cart_item"),
    

]
