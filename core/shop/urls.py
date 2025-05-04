from django.urls import path, re_path

from shop import views


app_name = "shop"

urlpatterns = [
    path("product_list/", views.ProductListView.as_view(), name="product_list"),
    re_path(r'product/(?P<slug>[-\w]+)/', views.ProductDetailView.as_view(), name="product_detail"),

]

