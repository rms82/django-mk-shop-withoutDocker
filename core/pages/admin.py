from django.contrib import admin

from pages.models import ContactTicket
# Register your models here.

@admin.register(ContactTicket)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_resolved')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('name', 'email', 'message')