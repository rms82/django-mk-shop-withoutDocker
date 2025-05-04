from django.core.exceptions import FieldError, ValidationError
from django.db.models import Q

from shop.models import ProductStatus


# query


def query_product_order_by(request, queryset):
    if order_by := request.GET.get("order-by"):
        try:
            queryset = queryset.order_by(order_by)
        except FieldError:
            pass

    return queryset


def query_coupon_name(request, queryset):
    if coupon_name := request.GET.get("coupon-name"):
        queryset = queryset.filter(code__icontains=coupon_name)

    return queryset
