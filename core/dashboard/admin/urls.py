from django.urls import path, include

from dashboard.admin import views


app_name = "admin"

urlpatterns = [
    path("", views.AdminDashbordView.as_view(), name="admin_dashboard"),
    path("security/", views.AdminSecurityView.as_view(), name="security"),
    path("change/", views.AdminChangeDashbordView.as_view(), name="change"),


    # products
    path("products/", views.AdminProductDashbordView.as_view(), name="products"),
    path("products/add/", views.AdminAddProductDashbordView.as_view(), name="add_product"),
    path("products/<int:pk>/edit/", views.AdminProductUpdateDashbordView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", views.AdminProductDeleteDashbordView.as_view(), name="product_delete"),


    # tickets
    path("tickets/", views.AdminTicketDashbordView.as_view(), name="tickets"),
    path("tickets/<int:pk>/edit/", views.AdminTicketUpdateDashbordView.as_view(), name="ticket_update"),
    path("tickets/<int:pk>/delete/", views.AdminTicketDeleteDashbordView.as_view(), name="ticket_delete"),


    # users
    path("users/", views.AdminUsersDashbordView.as_view(), name="users"),
    path("users/<int:pk>/edit/", views.AdminUserUpdateDashbordView.as_view(), name="user_update"),
    path("users/<int:pk>/delete/", views.AdminUserDeleteDashbordView.as_view(), name="user_delete"),
    
    
    # coupons
    path("coupons/", views.AdminCouponDashbordView.as_view(), name="coupons"),
    path("coupons/add/", views.AdminAddCouponDashbordView.as_view(), name="add_coupon"),
    path("coupons/<int:pk>/edit/", views.AdminCouponUpdateDashbordView.as_view(), name="coupon_update"),

]
