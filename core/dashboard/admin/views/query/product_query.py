from django.core.exceptions import FieldError, ValidationError

from shop.models import ProductStatus


# query
def query_product_category(request, queryset):
    if category := request.GET.get("category"):
        try:
            queryset = queryset.filter(category__id=category)
        except ValueError:
            pass

    return queryset


def query_product_order_by(request, queryset):
    if order_by := request.GET.get("order-by"):
        try:
            queryset = queryset.order_by(order_by)
        except FieldError:
            pass

    return queryset


def query_product_name(request, queryset):
    if product_name := request.GET.get("product-name"):
        queryset = queryset.filter(
            Q(title__icontains=product_name) | Q(description__icontains=product_name)
        )

    return queryset


def query_product_status(request, queryset):
    if ispublished := request.GET.get("ispublished"):
        if ispublished == "1":
            queryset = queryset.filter(status=ProductStatus.published.value)
        elif ispublished == "0":
            queryset = queryset.filter(status=ProductStatus.draft.value)
    
    return queryset
