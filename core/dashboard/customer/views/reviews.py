from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


from dashboard.permissions import CustomerDashboardPermissionMixin


from shop.models import Product, ProductStatus
from review.models import Review, ReviewStatus


class ReviewView(
    LoginRequiredMixin,
    CustomerDashboardPermissionMixin,
    ListView,
):
    template_name = "dashboard/customer/customer_reviews.html"
    context_object_name = "reviews"
    paginate_by = 10

    def get_queryset(self):
        queryset = Review.objects.filter(
            user=self.request.user, status=ReviewStatus.ACCEPTED.value
        ).select_related('product')

        return queryset
