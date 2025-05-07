from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from order.validators import IranianPhoneNumberValidator


USER = get_user_model()


# Create your models here.
# address
class Ostan(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    amar_code = models.IntegerField(_("Amar Code"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Ostan")
        verbose_name_plural = _("Ostans")
        ordering = ("id",)


class Shahrestan(models.Model):
    ostan = models.ForeignKey(
        Ostan,
        verbose_name=_("Ostan"),
        related_name="shahrestans",
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("Name"), max_length=255)
    amar_code = models.IntegerField(_("Amar Code"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Shahrestan")
        verbose_name_plural = _("Shahrestans")
        ordering = ("id",)


class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True)
    discount_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    max_uses = models.PositiveIntegerField(default=1)
    used_by = models.ManyToManyField(USER, related_name="used_coupons", blank=True)
    expired = models.DateTimeField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
    



class OrderStatus(models.IntegerChoices):
    pending = 1, "در انتظار پرداخت"
    processing = 2, "در حال پردازش"
    completed = 3, "اماده ارسال"
    cancelled = 4, "لغو شده"
    delivered = 5, "تحویل داده شده"


class UserAddress(models.Model):
    user = models.ForeignKey(
        USER, on_delete=models.CASCADE, related_name="user_addresses"
    )
    ostan = models.ForeignKey(
        Ostan, on_delete=models.PROTECT, related_name="ostan_addresses"
    )
    shahrestan = models.ForeignKey(
        Shahrestan, on_delete=models.PROTECT, related_name="shahrestan_addresses"
    )

    address = models.TextField()
    postal_code = models.CharField(max_length=15)
    receiver_phonenumber = models.CharField(
        max_length=12,
        validators=[
            IranianPhoneNumberValidator(),
        ],
    )


class Order(models.Model):
    user = models.ForeignKey(USER, on_delete=models.PROTECT)
    status = models.IntegerField(
        choices=OrderStatus.choices, default=OrderStatus.pending
    )
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.PROTECT,
        related_name="coupon_orders",
        null=True,
        blank=True,
    )
    total_amount = models.BigIntegerField(default=0)
    address = models.ForeignKey(
        UserAddress, on_delete=models.PROTECT, related_name="address_orders"
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"order for : {self.user.email}"

    def calculate_total_amount(self):
        order_items = self.items.all()

        return sum(item.quantity * item.price for item in order_items)

    def total_items_count(self):
        order_items = self.items.all()
        return sum(item.quantity for item in order_items)

    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "shop.Product", on_delete=models.PROTECT, related_name="order_items"
    )
    quantity = models.PositiveIntegerField()
    price = models.BigIntegerField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.user.email}-{self.product}"
