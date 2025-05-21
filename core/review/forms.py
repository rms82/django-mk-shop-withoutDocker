from django import forms
from .models import Review, ReviewStatus

from shop.models import Product, ProductStatus


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["product", "rating", "comment"]

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")

        # Check if the product exists and is published
        try:
            Product.objects.get(id=product.id, status=ProductStatus.published.value)
        except Product.DoesNotExist:
            raise forms.ValidationError("این محصول وجود ندارد")
        

        return cleaned_data
