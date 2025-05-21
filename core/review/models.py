from django.db import models
from django.contrib.auth import get_user_model


USER = get_user_model()

from shop.models import Product


class ReviewStatus(models.IntegerChoices):
    PENDING = 0, "در انتظار تأیید"
    ACCEPTED = 1, "تأیید شده"
    REJECTED = 2, "رد شده"


# Create your models here.
class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    comment = models.TextField()
    status = models.IntegerField(
        choices=ReviewStatus.choices, default=ReviewStatus.PENDING.value
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.email} for {self.product.title}"
    
    def is_pending(self):
        return self.status == ReviewStatus.PENDING.value
