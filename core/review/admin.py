from django.contrib import admin
from shop.models import Product  # فرض بر این است که Product هم در همین فایل است
from django.utils.translation import gettext_lazy as _

from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "user_email", "rating", "status", "created_at")
    list_filter = ("status", "created_at", "rating")
    search_fields = ("user__email", "product__title", "comment")
    list_editable = ("status",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "User Email"

    
    def get_status_display(self, obj):
        return obj.get_status_display()
