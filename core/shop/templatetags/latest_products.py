from django import template

from ..models import Product, ProductStatus

register = template.Library()


@register.inclusion_tag("includes/latest_products.html")
def show_latest_products(*args, **kwargs):
    latest_products = (
        Product.objects.filter(status=ProductStatus.published.value)
        .prefetch_related("category")
        .order_by("-created_date")[:8]
    )

    return {"latest_products": latest_products}
