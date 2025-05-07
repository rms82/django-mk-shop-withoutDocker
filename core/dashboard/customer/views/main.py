from django.views.generic import View, TemplateView, UpdateView
from django.db.models import Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView as AuthPasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from dashboard.permissions import CustomerDashboardPermissionMixin
from dashboard.forms import ProfileUpdateForm

from accounts.models import Profile
from order.models import Order, OrderStatus




# Create your views here.
class CustomerDashbordView(
    LoginRequiredMixin,
    CustomerDashboardPermissionMixin,
    TemplateView,
):
    template_name = "dashboard/customer/customer_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        orders = Order.objects.filter(user=self.request.user)
        status_counts = orders.aggregate(
        order_completed=Count("id", filter=Q(status=OrderStatus.delivered.value)),
        order_process=Count("id", filter=Q(status=OrderStatus.processing.value))
        )

        context["order_completed"] = status_counts["order_completed"]
        context["order_process"] = status_counts["order_process"]

        # اگر created_at داری بهتره از اون استفاده کنی برای آخرین سفارش
        context["last_order"] = orders.order_by("-created_date").first()

        return context
    


class CustomerSecurityView(
    LoginRequiredMixin,
    CustomerDashboardPermissionMixin,
    SuccessMessageMixin,
    AuthPasswordChangeView,
):
    template_name = "dashboard/customer/customer_security.html"
    success_message = "رمز عبور با موفقیت تغییر کرد"
    success_url = reverse_lazy("dashboard:customer:customer_dashboard")


class CustomerChangeDashbordView(
    LoginRequiredMixin,
    CustomerDashboardPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = "dashboard/customer/customer_change_dashboard.html"
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("dashboard:customer:change")
    success_message = "اطلاعات جدید با موفقیت ذخیره شد"

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)



