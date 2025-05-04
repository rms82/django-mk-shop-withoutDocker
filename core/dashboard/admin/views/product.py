from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError, ValidationError
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import redirect
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
from dashboard.admin.forms import ProductForm
from shop.models import Product, ProductCategory, ProductStatus
from dashboard.admin.views.query.product_query import (
    query_product_name,
    query_product_category,
    query_product_status,
    query_product_order_by,
)
from dashboard.admin.views.query.product_actions import action_product_list


class AdminProductDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    ListView,
):
    template_name = "dashboard/admin/product/admin_products.html"
    paginate_by = 20
    context_object_name = "products"

    def get_queryset(self):
        queryset = Product.objects.order_by("-id").prefetch_related("category")

        queryset = query_product_name(self.request, queryset)
        queryset = query_product_category(self.request, queryset)
        queryset = query_product_order_by(self.request, queryset)
        queryset = query_product_status(self.request, queryset)

        return queryset

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        selected_products = request.POST.getlist("selected_products")

        action_product_list(request, action, selected_products)

        return redirect("dashboard:admin:products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["product_count"] = self.get_queryset().count()
        context["categories"] = ProductCategory.objects.all()

        return context


class AdminProductDeleteDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    SuccessMessageMixin,
    DeleteView,
):
    queryset = Product.objects.all()
    success_url = reverse_lazy("dashboard:admin:products")
    success_message = "محصول با موفقیت حذف گردید"


class AdminProductUpdateDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
):
    queryset = Product.objects.all()
    form_class = ProductForm
    template_name = "dashboard/admin/product/admin_product_update.html"
    context_object_name = "product"

    success_url = reverse_lazy("dashboard:admin:products")
    success_message = "محصول با موفقیت اپدیت شد"


class AdminAddProductDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    SuccessMessageMixin,
    CreateView,
):
    queryset = Product.objects.all()
    form_class = ProductForm
    template_name = "dashboard/admin/product/admin_product_create.html"
    success_message = "محصول با موفقیت ایجاد شد"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
