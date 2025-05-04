from django.views.generic import View, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView as AuthPasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from dashboard.permissions import CustomerDashboardPermissionMixin
from dashboard.forms import ProfileUpdateForm

from accounts.models import Profile


# Create your views here.
class CustomerDashbordView(
    LoginRequiredMixin,
    CustomerDashboardPermissionMixin,
    TemplateView,
):
    template_name = "dashboard/customer/customer_home.html"


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



