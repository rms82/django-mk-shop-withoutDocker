from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Review
from .forms import ReviewForm
from django.shortcuts import redirect
from django.contrib import messages


class ReviewCreateView(LoginRequiredMixin, CreateView):
    http_method_names = ["post"]
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        product = form.cleaned_data.get("product")

        messages.success(
            self.request,
            "دیدگاه شما با موفقیت ثبت شد و پس از بررسی نمایش داده خواهد شد",
        )
        return redirect("shop:product_detail", slug=product.slug)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return redirect(self.request.META.get("HTTP_REFERER"))


class ReviewDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Review
    success_message = "نظر با موفقیت حذف گردید"

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER", '/')

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user

    def handle_no_permission(self):
        messages.error(self.request, "شما اجازه حذف این نظر را ندارید.")
        return redirect(self.request.META.get("HTTP_REFERER", '/'))
