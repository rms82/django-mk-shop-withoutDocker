from django.views.generic import (
    TemplateView,
    UpdateView,
    ListView,
    CreateView,
    View,
    FormView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.urls import reverse_lazy
from django.http import JsonResponse

from dashboard.permissions import CustomerDashboardPermissionMixin


from order.models import Order
from . import order_query


class CustomerOrdersView(
    LoginRequiredMixin,
    CustomerDashboardPermissionMixin,
    ListView,
):
    template_name = "dashboard/customer/orders/orders_list.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)

        queryset = order_query.query_orders_status(self.request, queryset)
        queryset = order_query.query_orders_order_by(self.request, queryset)
        queryset = order_query.query_orders_coupon(self.request, queryset)

        return queryset
