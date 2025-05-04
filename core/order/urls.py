from django.urls import path

from order import views

app_name = "order"

urlpatterns = [
    path("", views.OrderSummaryView.as_view(), name="order_summary"),
    path("<int:pk>/complete/", views.OrderCompleteView.as_view(), name="order_complete"),
    path("coupon_validation/", views.CouponValidationView.as_view(), name="coupon_validation"),


]
