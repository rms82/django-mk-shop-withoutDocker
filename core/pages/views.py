from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.contrib import messages

from pages.forms import ContactForm


# Create your views here.
class HomeView(TemplateView):
    template_name = 'pages/home.html'


class AboutUsView(TemplateView):
    template_name = 'pages/about_us.html'

class ContactView(FormView):
    template_name = 'pages/contact_us.html'
    form_class = ContactForm
    success_url = reverse_lazy('pages:home')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "پیام شما به مدیران ارسال شد منتظر پاسخ باشید")
        return super().form_valid(form)