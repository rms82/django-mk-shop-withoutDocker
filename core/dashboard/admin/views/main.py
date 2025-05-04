from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView as AuthPasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    UpdateView,
    View,
)

from dashboard.permissions import AdminDashboardPermissionMixin
from dashboard.forms import ProfileUpdateForm
from accounts.models import Profile


class AdminDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    TemplateView,
):
    template_name = "dashboard/admin/dashboard_admin_home.html"


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

