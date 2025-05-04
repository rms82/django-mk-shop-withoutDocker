from django.contrib import admin

from order.models import Coupon, UserAddress, Order, OrderItem, Ostan, Shahrestan

admin.site.register(Ostan)
admin.site.register(Shahrestan)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percent", "max_uses", "expired", "created_date")
    list_filter = ("expired", "created_date")
    search_fields = ("code",)


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "postal_code", "receiver_phonenumber")
    # list_filter = ("state", "city")
    search_fields = (
        "user__username",

        "address",
        "postal_code",
        "receiver_phonenumber",
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_amount", "created_date")
    list_filter = ("status", "created_date")
    search_fields = ("user__username", "address__city")
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")
    list_filter = ("created_date",)
    search_fields = ("order__id", "product__name")


# Register your models here.
