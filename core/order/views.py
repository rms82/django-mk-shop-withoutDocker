from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, View
from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone

import requests
import json


from cart.cart import Cart
from cart.models import Cart as CartModel
from order.forms import OrderCreateForm, Coupon
from order.models import Order, UserAddress, OrderItem, OrderStatus
from order.permissions import OrderCompletePermission

# Create your views here.


class OrderSummaryView(LoginRequiredMixin, FormView):
    template_name = "order/order_summary.html"
    form_class = OrderCreateForm

    def dispatch(self, request, *args, **kwargs):
        cart_object = Cart(request)
        if cart_object.is_empty():
            return redirect("pages:home")

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request  # Pass the entire request to the form
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart_object = CartModel.objects.get(user=self.request.user)
        context["order_total_price"] = cart_object.calculate_total_price()
        context["user_addresses"] = UserAddress.objects.filter(user=self.request.user)

        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        cart_object = CartModel.objects.get(user=self.request.user)
        cart_items = cart_object.cart_items.all()

        address_id = cleaned_data.get("address_id")
        coupon = cleaned_data.get("coupon", None)

        order = self.create_order(address_id)
        order_items = self.create_orderitems(order, cart_items)

        self.apply_coupon(order, coupon)
        self.clear_cart(cart_items)

        self.success_url = reverse_lazy("order:order_complete", kwargs={"pk": order.pk})

        return super().form_valid(form)

    def create_order(self, address_id):
        order = Order.objects.create(
            user=self.request.user,
            address_id=address_id,
        )

        return order

    def create_orderitems(self, order, cart_items):
        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price(),
            )
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)

        return order_items

    def clear_cart(self, cart_items):
        cart_items.delete()
        Cart(self.request).clear()

    def apply_coupon(self, order, coupon):
        total_amount = order.calculate_total_amount()

        if coupon:
            total_amount -= round((coupon.discount_percent * total_amount) / 100)
            coupon.used_by.add(self.request.user)
            order.coupon = coupon
            coupon.save()

        order.total_amount = total_amount
        order.save()


class OrderCompleteView(LoginRequiredMixin, OrderCompletePermission, TemplateView):
    template_name = "order/order_success.html"

    def post(self, request, *args, **kwargs):
        # درگاه پرداخت بصورت امتحانی
        # data = {
        #     "merchant_id": "sth",
        #     "amount": "1000",
        #     "callback_url": "http://example.com/verify",
        #     "description": "Transaction description.",
        #     "metadata": {"mobile": "09123456789", "email": "info@example.com"},
        # }
        # response = requests.post(
        #     "https://sandbox.zarinpal.com/pg/v4/payment/request.json", data=json.dumps(data)
        # )

        # درگه پرداخت بصورت امتخانی موفقیت آمیز است
        # print(response.json())

        
        order = get_object_or_404(Order, pk=self.kwargs['pk'], user=self.request.user)
        order.status = OrderStatus.processing.value
        order.save()

        messages.success(self.request, 'پرداخت با موفقیت انجام شد . سفارش شما ثبت شد')

        return redirect("pages:home")


class CouponValidationView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        coupon = self.request.POST.get("coupon", None)

        success = True
        message = "کد تخفیف با موفقیت اعمال شد"

        if not coupon:
            success = False
            message = "لطفا مقدار کد تخفیف را وارد کنید."

        else:
            try:
                coupon = Coupon.objects.get(code=coupon)

                if self.request.user in coupon.used_by.all():
                    message = "شما قبلا این کد را استفاده کرده اید."
                    success = False

                elif coupon.used_by.count() >= coupon.max_uses:
                    message = "کد تخفیف به محدودیت استفاده کاربران رسیده است"
                    success = False

                elif coupon.expired and coupon.expired < timezone.now():
                    message = "مهلت استفاده از این کد به پایان رسیده است"
                    success = False

            except Coupon.DoesNotExist:
                message = "کد تخفیف معتبر نیست"
                success = False

        return JsonResponse(
            {
                "success": success,
                "message": message,
            }
        )
