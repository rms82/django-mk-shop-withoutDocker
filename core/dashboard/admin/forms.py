from django import forms
from django.contrib.auth import get_user_model

from shop.models import Product
from order.models import Coupon
from pages.models import ContactTicket

USER = get_user_model()


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].widget.attrs["class"] = "form-select"
        self.fields["status"].widget.attrs["class"] = "form-select"

        self.fields["image"].widget.attrs["class"] = "form-control"
        self.fields["description"].widget.attrs["class"] = "form-control"
        self.fields["slug"].widget.attrs["class"] = "form-control"
        self.fields["title"].widget.attrs["class"] = "form-control"
        self.fields["stock"].widget.attrs["class"] = "form-control"
        self.fields["price"].widget.attrs["class"] = "form-control"
        self.fields["discount"].widget.attrs["class"] = "form-control"

    class Meta:
        model = Product
        fields = [
            "title",
            "slug",
            "category",
            "image",
            "description",
            "stock",
            "status",
            "price",
            "discount",
        ]


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = ContactTicket
        fields = ["message", "is_resolved"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["is_resolved"].widget.attrs["class"] = "form-check-input"
        self.fields["message"].widget.attrs["class"] = "form-control"


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = USER
        fields = ["user_type", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["is_active"].widget.attrs["class"] = "form-check-input"
        self.fields["user_type"].widget.attrs["class"] = "form-select"


class AdminCouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = [
            "code",
            "discount_percent",
            "max_uses",
            "expired",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["code"].widget.attrs["class"] = "form-control"
        self.fields["discount_percent"].widget.attrs["class"] = "form-control"
        self.fields["max_uses"].widget.attrs["class"] = "form-control"
        self.fields["expired"].widget.attrs["class"] = "form-control"


