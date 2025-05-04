from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError, ValidationError
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DeleteView,
    UpdateView,
)

from dashboard.permissions import AdminDashboardPermissionMixin
from dashboard.admin.forms import TicketUpdateForm
from pages.models import ContactTicket


class AdminTicketUpdateDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = "dashboard/admin/ticket/admin_ticket_update.html"

    form_class = TicketUpdateForm
    context_object_name = "ticket"
    queryset = ContactTicket.objects.all()

    success_url = reverse_lazy("dashboard:admin:tickets")
    success_message = "تیکت با موفقیت اپدیت شد"


class AdminTicketDeleteDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    SuccessMessageMixin,
    DeleteView,
):
    queryset = ContactTicket.objects.all()
    success_url = reverse_lazy("dashboard:admin:tickets")
    success_message = "تیکت با موفقیت حذف گردید"


class AdminTicketDashbordView(
    LoginRequiredMixin,
    AdminDashboardPermissionMixin,
    ListView,
):
    template_name = "dashboard/admin/ticket/admin_tickets.html"
    context_object_name = "tickets"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket_count"] = self.get_queryset().count()

        return context

    def get_queryset(self):
        queryset = ContactTicket.objects.order_by("-created_at")

        if ticket_name := self.request.GET.get("ticket-name"):
            queryset = queryset.filter(
                Q(name__icontains=ticket_name) | Q(email__icontains=ticket_name)
            )

        if isresolved := self.request.GET.get("isresolved"):
            try:
                queryset = queryset.filter(is_resolved=isresolved)
            except ValidationError:
                pass

        return queryset

