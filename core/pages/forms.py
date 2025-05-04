from django import forms

from pages.models import ContactTicket

class ContactForm(forms.ModelForm):
    class Meta:
            model = ContactTicket
            fields = ['name', 'email', 'message']