from django.db import models
from django.contrib.auth import get_user_model

from shop.models import Product

USER = get_user_model()


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(USER, on_delete=models.CASCADE, related_name="cart")

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def calculate_total_price(self):
        cart_items = self.cart_items.all()

        return sum(item.quantity * item.product.get_price() for item in cart_items)

    def __str__(self):
        return f"cart for : {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
