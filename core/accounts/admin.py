from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser, Profile


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "id",
        "user_type",
        "is_staff",
        "is_active",
        "is_verified",
        "is_superuser",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "user_type",
    )
    search_fields = ("email",)
    ordering = ("-id",)

    fieldsets = (
        ("general", {"fields": ("email", "password", 'user_type')}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    'user_type',
                    "password1",
                    "password2",
                    "is_verified",
                    "is_active",
                ),
            },
        ),
    )


@admin.register(Profile)
class CustomUserProfile(admin.ModelAdmin):
    list_display = (
        "user",
        "id",
        "fullname",
    )

    ordering = ("-id",)

