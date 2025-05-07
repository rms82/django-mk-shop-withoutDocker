from django.core.exceptions import FieldError, ValidationError

from order.models import OrderStatus,Order


# query


def query_orders_order_by(request, queryset):
    if order_by := request.GET.get("order-by"):
        try:
            queryset = queryset.order_by(order_by)
        except FieldError:
            pass

    return queryset



def query_orders_status(request, queryset):
    if status := request.GET.get("status"):
        if status == "1":
            queryset = queryset.filter(status=OrderStatus.pending.value)
        elif status == "2":
            queryset = queryset.filter(status=OrderStatus.processing.value)
        elif status == "3":
            queryset = queryset.filter(status=OrderStatus.completed.value)
        elif status == "4":
            queryset = queryset.filter(status=OrderStatus.cancelled.value)
        elif status == "5":
            queryset = queryset.filter(status=OrderStatus.delivered.value)
    
    return queryset


def query_orders_coupon(request, queryset):
    if status := request.GET.get("coupon"):
        if status == "1":
            queryset = queryset.exclude(coupon=None)
        elif status == "0":
            queryset = queryset.filter(coupon=None)
        
    
    return queryset
