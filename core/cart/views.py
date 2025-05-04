from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http.response import JsonResponse

from cart.cart import Cart


# Create your views here.
class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        cart_obj = Cart(request)

        product_id = request.POST.get("product_id")
        if product_id:
            cart_obj.add_product(product_id)

            if request.user.is_authenticated:
                cart_obj.cart_to_db(request.user)

        return JsonResponse({"cart_obj": cart_obj.cart["items"]})


class ClearCartView(View):
    def post(self, request, *args, **kwargs):
        cart_obj = Cart(request)
        cart_obj.clear()

        if request.user.is_authenticated:
            cart_obj.cart_to_db(request.user)

        return JsonResponse({"cart_obj": cart_obj.cart["items"]})


class CartUpdateQuantityView(View):
    def post(self, request, *args, **kwargs):
        cart_obj = Cart(request)

        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")

        if product_id and quantity:
            cart_obj.update_product_quantity(product_id, int(quantity))

            if request.user.is_authenticated:
                cart_obj.cart_to_db(request.user)

        return JsonResponse({"cart_obj": cart_obj.cart["items"]})


class CartDeleteItemView(View):
    def post(self, request, *args, **kwargs):
        cart_obj = Cart(request)

        product_id = request.POST.get("product_id")


        if product_id:
            cart_obj.delete_product_item(product_id)

            if request.user.is_authenticated:
                cart_obj.cart_to_db(request.user)

        return JsonResponse({"cart_obj": cart_obj.cart["items"]})


class CartSummaryView(TemplateView):
    template_name = "cart/cart_summary.html"


class CartItemsView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        items = [
            {
                "product_id": item["product_id"],
                "title": item["product_obj"].title,
                "price": item["product_obj"].price,
                "image": item["product_obj"].image.url,
                "quantity": item["quantity"],
                "total_price": item["total_price"],
            }
            for item in cart.get_items()
        ]
        cart_total_price = sum(item["quantity"] * item["price"] for item in items)
        items_count = cart.cart_total_items()

        return JsonResponse(
            {
                "items": items,
                "cart_total_price": cart_total_price,
                "items_count": items_count,
            }
        )
