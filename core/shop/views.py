from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import FieldError
from shop.models import Product, ProductCategory, ProductStatus, Wishlist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse


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

        context["categories"] = ProductCategory.objects.all()

        if self.request.user.is_authenticated:
            user_wishlist = Wishlist.objects.filter(user=self.request.user).values_list('product_id', flat=True)
            context['wishlist_ids'] = list(user_wishlist)
        else:
            context['wishlist_ids'] = []

        return context


class ProductDetailView(DetailView):
    template_name = "shop/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(status=ProductStatus.published.value)


class ProductWishlistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id", None)
        msg = "اطلاعات صحیح نمیباشد"
        success = False

        if product_id:
            product = get_object_or_404(Product, id=product_id)
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=request.user, product=product
            )

            if not created:
                wishlist_item.delete()
                msg = "از علاقه‌مندی‌ها حذف شد."
                success = False
            else:
                msg = "به علاقه‌مندی‌ها اضافه شد."
                success = True

        return JsonResponse({"message": msg, "success": success})
