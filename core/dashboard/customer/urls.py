from django.urls import path, include

from dashboard.customer import views


app_name = "customer"

urlpatterns = [
    path("", views.CustomerDashbordView.as_view(), name="customer_dashboard"),
    path("security/", views.CustomerSecurityView.as_view(), name="security"),
    path("change/", views.CustomerChangeDashbordView.as_view(), name="change"),

    # addresses
    path("shahrestan/", views.GetShahrestan.as_view(), name="get_shahrestan"),
    path("address/", views.CustomerAddressesView.as_view(), name="address_list"),
    path("address/add/", views.CustomerCreateAddressDashbordView.as_view(), name="address_create"),
    path("address/<int:pk>/update/", views.CustomerUpdateAddressDashbordView.as_view(), name="address_update"),

    # orders
    path("orders/", views.CustomerOrdersView.as_view(), name="orders"),


]

