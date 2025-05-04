from django.db import IntegrityError
from django.contrib import messages


from order.models import Coupon


def action_coupon_list(request, action, selected_coupons):
    if action == "unpublish_selected" and selected_coupons:
        # Unpublish selected products
        pass

    # elif action == "publish_selected" and selected_products:
    #     # Publish selected products
    #     Product.objects.filter(id__in=selected_products).update(
    #         status=ProductStatus.published.value
    #     )
    #     messages.success(request, "Selected products have been published.")

    # elif action == "without_discount" and selected_products:
    #     # Remove discount from selected products
    #     Product.objects.filter(id__in=selected_products).update(discount=0)
    #     messages.success(request, "تخفیفات محصولات انتخابی حذف گردید.")

    elif action == "delete_selected" and selected_coupons:
        # Delete selected products
        try:

            Coupon.objects.filter(id__in=selected_coupons).delete()
            messages.success(request, "کد های انتخابی با موفقیت حذف گردید.")
        except IntegrityError:
            messages.warning(request, "نمیتوان کد های انتخابی را حذف کرد")
