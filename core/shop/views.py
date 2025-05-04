from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.core.exceptions import FieldError
from shop.models import Product, ProductCategory, ProductStatus


# Create your views here.
class ProductListView(ListView):
    template_name = "shop/product_list.html"
    paginate_by = 9
    context_object_name = "products"

    def get_paginate_by(self, queryset):
        LIST_PAGE_SIZE = ["9", "18", "27", "45"]

        page_size = self.request.GET.get("page-size", self.paginate_by)

        return int(page_size) if page_size in LIST_PAGE_SIZE else self.paginate_by

    def get_queryset(self):
        queryset = (
            Product.objects.filter(status=ProductStatus.published.value)
            .order_by("-id")
            .prefetch_related("category")
        )

        if category := self.request.GET.get("category"):
            try:
                queryset = queryset.filter(category__id=category)
            except ValueError:
                pass

        if min_price := self.request.GET.get("min-price"):
            try:
                queryset = queryset.filter(price__gte=min_price)
            except ValueError:
                pass

        if max_price := self.request.GET.get("max-price"):
            try:
                queryset = queryset.filter(price__lte=max_price)
            except ValueError:
                pass

        if product_name := self.request.GET.get("product-name"):
            queryset = queryset.filter(
                Q(title__icontains=product_name)
                | Q(description__icontains=product_name)
            )

        if order_by := self.request.GET.get("order-by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context["product_count"] = self.get_queryset().count()
        context["categories"] = ProductCategory.objects.all()

        return context


class ProductDetailView(DetailView):
    template_name = "shop/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(status=ProductStatus.published.value)
