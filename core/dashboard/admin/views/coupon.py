from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError, ValidationError
from django.db import IntegrityError
from django.db.models import Q, Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    UpdateView,
    View,
    ListView,
    DeleteView,
    UpdateView,
    CreateView,
)

from dashboard.permissions import AdminDashboardPermissionMixin
from dashboard.admin.views.query.coupon_actions import action_coupon_list
from dashboard.admin.views.query.coupon_query import (
    query_coupon_name,
    query_product_order_by,
)
from dashboard.admin.forms import AdminCouponForm
from order.models import Coupon


class AdminCouponDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    ListView,
):
    template_name = "dashboard/admin/coupon/coupon_list.html"
    paginate_by = 20
    context_object_name = "coupons"

    def get_paginate_by(self, queryset):
        try:
            page_size = int(self.request.GET.get("page-size", self.paginate_by))
            return page_size

        except ValueError:
            return self.paginate_by

    def get_queryset(self):
        queryset = Coupon.objects.annotate(used_by_count=Count("used_by")).order_by(
            "-id"
        )

        queryset = query_coupon_name(self.request, queryset)
        queryset = query_product_order_by(self.request, queryset)

        queryset = queryset.values(
            "id",
            "code",
            "discount_percent",
            "max_uses",
            "expired",
            "used_by_count",
        )
        return queryset

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        selected_coupons = request.POST.getlist("selected_coupons")

        action_coupon_list(request, action, selected_coupons)

        return redirect("dashboard:admin:coupons")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["coupon_count"] = self.get_queryset().values("id").count()

        return context


# class AdminProductDeleteDashbordView(
#     LoginRequiredMixin,
#     AdminDashboardPermissionMixin,
#     SuccessMessageMixin,
#     DeleteView,
# ):
#     queryset = Product.objects.all()
#     success_url = reverse_lazy("dashboard:admin:products")
#     success_message = "محصول با موفقیت حذف گردید"


class AdminCouponUpdateDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
):
    queryset = Coupon.objects.all()
    form_class = AdminCouponForm
    template_name = "dashboard/admin/coupon/admin_coupon_update.html"
    context_object_name = "coupon"

    success_url = reverse_lazy("dashboard:admin:coupons")
    success_message = "کد تخفیف با موفقیت اپدیت شد"


class AdminAddCouponDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    SuccessMessageMixin,
    CreateView,
):
    queryset = Coupon.objects.all()
    form_class = AdminCouponForm
    template_name = "dashboard/admin/coupon/admin_coupon_create.html"
    success_message = "کد تخفیف با موفقیت ایجاد شد"
    success_url = reverse_lazy("dashboard:admin:coupons")
