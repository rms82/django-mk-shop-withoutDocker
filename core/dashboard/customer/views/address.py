from django.views.generic import (
    TemplateView,
    UpdateView,
    ListView,
    CreateView,
    View,
    FormView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.urls import reverse_lazy
from django.http import JsonResponse

from dashboard.permissions import CustomerDashboardPermissionMixin
from dashboard.customer.forms import UserAddressForm

from order.models import UserAddress, Ostan, Shahrestan


# Create your views here.
class CustomerAddressesView(
    LoginRequiredMixin,
    CustomerDashboardPermissionMixin,
    ListView,
):
    template_name = "dashboard/customer/address/address_list.html"
    context_object_name = "addresses"

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


class CustomerCreateAddressDashbordView(
    LoginRequiredMixin,
    CustomerDashboardPermissionMixin,
    SuccessMessageMixin,
    CreateView,
):
    queryset = UserAddress.objects.all()
    form_class = UserAddressForm
    template_name = "dashboard/customer/address/address_create.html"
    success_message = "آدرس با موفقیت ایجاد شد"
    success_url = reverse_lazy("dashboard:customer:address_list")

    def form_valid(self, form):
        user = self.request.user
        address_count = UserAddress.objects.filter(user=user).count()

        if address_count >= 3:
            messages.warning(self.request, "تعداد آدرس های مجاز 10 عدد میباشد ")
            return self.form_invalid(form)
        
        form.instance.user = user  # Set the user
        return super().form_valid(form)


class GetShahrestan(View):
    def get(self, request):
        ostan_id = request.GET.get("ostan_id")

        if not ostan_id:
            return JsonResponse({"shahrestans": []})

        try:
            shahrestans = Shahrestan.objects.filter(ostan_id=int(ostan_id))
        except ValueError:
            return JsonResponse({"shahrestans": []})

        return JsonResponse({"shahrestans": list(shahrestans.values("id", "name"))})



class CustomerUpdateAddressDashbordView(
    LoginRequiredMixin,
    CustomerDashboardPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
):
    form_class = UserAddressForm
    template_name = "dashboard/customer/address/address_update.html"
    success_message = "آدرس با موفقیت آپدیت شد"
    success_url = reverse_lazy("dashboard:customer:address_list")
    context_object_name = "address"
    

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
    
