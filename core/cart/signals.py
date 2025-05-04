from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.dispatch import receiver

from cart.cart import Cart



@receiver(user_logged_out)
def user_loggout(sender, user, request, *args, **kwargs):
    cart = Cart(request)
    cart.cart_to_db(user)


@receiver(user_logged_in)
def user_login(sender, user, request, *args, **kwargs):
    cart = Cart(request)
    cart.cart_from_db(user)
    