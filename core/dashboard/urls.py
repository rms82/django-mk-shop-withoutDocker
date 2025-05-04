from django.urls import path, include

from dashboard import views


app_name = "dashboard"

urlpatterns = [
    path("", views.RedirectToDashbordView.as_view(), name="redirect_dashboard"),
    path("admin/", include('dashboard.admin.urls')),
    path("customer/", include('dashboard.customer.urls')),
    path('reset-image/', views.ResetProfileImageView.as_view(), name='reset_profile_image'),


]
