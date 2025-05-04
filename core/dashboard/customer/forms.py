from django import forms
from django.contrib.auth import get_user_model


from order.models import UserAddress, Shahrestan, Ostan


USER = get_user_model()


class UserAddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["ostan"].widget.attrs["class"] = "form-select"
        self.fields["address"].widget.attrs["class"] = "form-control"
        self.fields["postal_code"].widget.attrs["class"] = "form-control"
        self.fields["receiver_phonenumber"].widget.attrs["class"] = "form-control"

    def clean_shahrestan(self):
        shahrestan = self.cleaned_data["shahrestan"]
        ostan = self.cleaned_data["ostan"]

        if shahrestan.ostan != ostan:
            raise forms.ValidationError(
                "شهر و ا��تان با این شهر و ا��تان یکسان نمی‌شوند"
            )

        return shahrestan

    class Meta:
        model = UserAddress
        fields = [
            "ostan",
            "shahrestan",
            "address",
            "postal_code",
            "receiver_phonenumber",
        ]
