from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect

from dashboard.permissions import AdminDashboardPermissionMixin

from review.models import Review, ReviewStatus


class AdminReviewView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    ListView,
):
    template_name = "dashboard/admin/reviews/admin_review_list.html"
    context_object_name = "reviews"
    paginate_by = 10

    def get_queryset(self):
        queryset = Review.objects.select_related("product", "user").order_by("status")
        return queryset


class AdminReviewDeleteDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    SuccessMessageMixin,
    DeleteView,
):
    queryset = Review.objects.all()
    success_url = reverse_lazy("dashboard:admin:reviews")
    success_message = "نظر با موفقیت حذف گردید"


class AdminReviewAcceptDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    View,
):
    def get(self, request, pk, *args, **kwargs):
        review = get_object_or_404(Review, pk=pk)
        review.status = ReviewStatus.ACCEPTED.value
        review.save()

        messages.success(request, "نظر با موفقیت تایید شد")

        return redirect("dashboard:admin:reviews")


class AdminReviewRejectDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    View,
):
    def get(self, request, pk, *args, **kwargs):
        review = get_object_or_404(Review, pk=pk)
        review.status = ReviewStatus.REJECTED.value
        review.save()

        messages.error(request, "نظر با موفقیت رد شد")

        return redirect("dashboard:admin:reviews")
