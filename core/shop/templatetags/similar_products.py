from django import template

from ..models import Product, ProductStatus

register = template.Library()


@register.inclusion_tag("includes/similar_products.html")
def show_similar_products(product_obj, *args, **kwargs):
    categoty = product_obj.category.all()
    similar_products = (
        Product.objects.filter(
            status=ProductStatus.published.value, category__in=categoty
        )
        .prefetch_related("category")
        .order_by("-created_date")[:4]
    )

    return {"similar_products": similar_products}
