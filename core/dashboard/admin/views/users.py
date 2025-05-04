from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError, ValidationError
from django.db.models import Q, ProtectedError
from django.urls import reverse_lazy
from django.views.generic import (
    View,
    ListView,
    UpdateView,
    DeleteView,
)

from dashboard.permissions import AdminDashboardPermissionMixin
from dashboard.admin.forms import UserUpdateForm
from accounts.models import Profile, UserType


USER = get_user_model()


class AdminUsersDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    ListView,
):
    template_name = "dashboard/admin/users/admin_user_list.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users_count"] = self.get_queryset().count()

        return context

    def get_queryset(self):
        queryset = Profile.objects.filter(
            user__user_type=UserType.customer.value
        ).values("id", "user__email")

        return queryset


class AdminUserUpdateDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = "dashboard/admin/users/admin_user_edit.html"

    form_class = UserUpdateForm
    context_object_name = "user"
    queryset = USER.objects.filter(user_type=UserType.customer.value)

    success_url = reverse_lazy("dashboard:admin:users")
    success_message = "تیکت با موفقیت اپدیت شد"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_types"] = UserType.choices

        return context


class AdminUserDeleteDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    SuccessMessageMixin,
    DeleteView,
):
    queryset = USER.objects.filter(user_type=UserType.customer.value)
    success_url = reverse_lazy("dashboard:admin:users")
    success_message = "کاربر با موفقیت حذف گردید"

    def form_valid(self, form):
        try:
            self.object = self.get_object()
            success_url = self.get_success_url()
            self.object.delete()
            messages.success(self.request, self.success_message)
            return redirect(success_url)
        except ProtectedError:
            error_message = "نمیتوان این کاربر را حذف کرد"
            messages.error(self.request, error_message)
            return redirect(self.get_success_url())
