from django.db import IntegrityError
from django.contrib import messages

from shop.models import Product, ProductStatus


def action_product_list(request, action, selected_products):
    if action == "unpublish_selected" and selected_products:
        # Unpublish selected products
        Product.objects.filter(id__in=selected_products).update(
            status=ProductStatus.draft.value
        )
        messages.success(request, "Selected products have been unpublished.")

    elif action == "publish_selected" and selected_products:
        # Publish selected products
        Product.objects.filter(id__in=selected_products).update(
            status=ProductStatus.published.value
        )
        messages.success(request, "Selected products have been published.")

    elif action == "without_discount" and selected_products:
        # Remove discount from selected products
        Product.objects.filter(id__in=selected_products).update(discount=0)
        messages.success(request, "تخفیفات محصولات انتخابی حذف گردید.")

    elif action == "delete_selected" and selected_products:
        # Delete selected products
        try:
            Product.objects.filter(id__in=selected_products).delete()
            messages.success(request, "محصولات انتخابی با موفقیت حذف گردید.")
        except IntegrityError:
            messages.warning(request, "نمیتوان محصولات انتخابی را حذف کرد")
