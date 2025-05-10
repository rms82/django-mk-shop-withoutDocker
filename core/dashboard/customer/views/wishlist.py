from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError
from django.db.models import Q
from django.views.generic import ListView


from dashboard.permissions import CustomerDashboardPermissionMixin


from shop.models import Product, Wishlist, ProductStatus


class WishlistOrdersView(
    LoginRequiredMixin,
    CustomerDashboardPermissionMixin,
    ListView,
):
    template_name = "dashboard/customer/wishlist.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        product_ids = Wishlist.objects.filter(user=self.request.user).values_list(
            "product", flat=True
        )

        queryset = Product.objects.filter(
            id__in=product_ids, status=ProductStatus.published.value
        )

        if order_by := self.request.GET.get("order-by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass

        if product_name := self.request.GET.get("product-name"):
            queryset = queryset.filter(
                Q(title__icontains=product_name)
                | Q(description__icontains=product_name)
            )

        return queryset
