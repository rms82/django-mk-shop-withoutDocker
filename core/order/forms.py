from django import forms


from django.utils import timezone

from order.models import Order, UserAddress, Coupon


class OrderCreateForm(forms.Form):
    coupon = forms.CharField(required=False)
    address_id = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        # Remove request from kwargs before initializing form fields
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_coupon(self):
        coupon = self.cleaned_data["coupon"]

        if coupon == "":
            return None

        if coupon:
            try:
                coupon = Coupon.objects.get(code=coupon)

                if self.request.user in coupon.used_by.all():
                    raise forms.ValidationError("شما قبلا این کد را استفاده کرده اید.")

                if coupon.used_by.count() >= coupon.max_uses:
                    raise forms.ValidationError(
                        "کد تخفیف به محدودیت استفاده کاربران رسیده است"
                    )

                if coupon.expired and coupon.expired < timezone.now():
                    raise forms.ValidationError(
                        "مهلت استفاده از این کد به پایان رسیده است"
                    )
            except Coupon.DoesNotExist:
                raise forms.ValidationError("کد تخفیف معتبر نیست")

        return coupon

    def clean_address_id(self):
        address_id = self.cleaned_data["address_id"]

        try:
            address_obj = UserAddress.objects.get(id=address_id, user=self.request.user)
        except UserAddress.DoesNotExist:
            raise forms.ValidationError("آدرس نامعتبر میباشد")

        return address_id
