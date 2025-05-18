from django import template

from ..models import Product, ProductStatus

register = template.Library()


@register.inclusion_tag("includes/slider_products.html")
def show_slider_products(*args, **kwargs):
    
    slider_products = (
        Product.objects.filter(
            status=ProductStatus.published.value,
            show_in_slide=True,
        )
        .order_by("-created_date")[:4]
    )

    return {"slider_products": slider_products}
