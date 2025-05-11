from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView as AuthPasswordChangeView
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    UpdateView,
    View,
)
from django.db.models import Q, Count

from dashboard.permissions import AdminDashboardPermissionMixin
from dashboard.forms import ProfileUpdateForm
from accounts.models import Profile, UserType
from shop.models import Product, ProductStatus
from order.models import Order, OrderStatus
from pages.models import ContactTicket


USER = get_user_model()


class AdminDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    TemplateView,
):
    template_name = "dashboard/admin/dashboard_admin_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["last_product"] = Product.objects.last()

        product_counts = Product.objects.aggregate(
            published_count=Count("id", filter=Q(status=ProductStatus.published.value))
        )
        order_counts = Order.objects.aggregate(
            processing_count=Count("id", filter=Q(status=OrderStatus.processing.value))
        )
        user_counts = USER.objects.aggregate(
            customer_count=Count("id", filter=Q(user_type=UserType.customer.value))
        )
        ticket_counts = ContactTicket.objects.aggregate(
            unresolved_count=Count("id", filter=Q(is_resolved=False))
        )

        context["published_products"] = product_counts["published_count"]
        context["processing_orders"] = order_counts["processing_count"]
        context["registered_users"] = user_counts["customer_count"]
        context["unresolved_tickets"] = ticket_counts["unresolved_count"]

        return context


class AdminSecurityView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    SuccessMessageMixin,
    AuthPasswordChangeView,
):
    template_name = "dashboard/admin/admin_security.html"
    success_message = "رمز عبور با موفقیت تغییر کرد"
    success_url = reverse_lazy("dashboard:admin:admin_dashboard")


class AdminChangeDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = "dashboard/admin/admin_change_dashboard.html"
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("dashboard:admin:change")
    success_message = "اطلاعات با موفقیت تغییر کرد"

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)
