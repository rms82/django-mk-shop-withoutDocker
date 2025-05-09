from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse

from ckeditor.fields import RichTextField

User = get_user_model()


# Create your models here.
class TitleSlugDateModel(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(allow_unicode=True, null=True, blank=True, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProductCategory(TitleSlugDateModel):
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductStatus(models.IntegerChoices):
    published = 1, "published"
    draft = 2, "draft"


class Product(TitleSlugDateModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    category = models.ManyToManyField(ProductCategory, blank=True)
    image = models.ImageField(
        upload_to="products/images/", default="products/default.jpg"
    )
    description = RichTextField()
    stock = models.PositiveIntegerField(default=0)
    status = models.IntegerField(
        choices=ProductStatus.choices, default=ProductStatus.draft.value
    )
    price = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)], default=0
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def show_raw_price(self):
        return self.price

    def show_discounted_price(self):
        discount = self.price * float(self.discount / 100)
        price = round(self.price - discount)
        return price

    def get_price(self):
        discount = self.price * float(self.discount / 100)
        price = round(self.price - discount)
        return int(price)

    def is_discounted(self):
        return self.discount != 0

    def is_published(self):
        return self.status == ProductStatus.published.value

    def get_absolute_url(self):
        return reverse("dashboard:admin:product_update", kwargs={"pk": self.pk})


def product_image_upload_to(instance, filename):
    return f"products/images/{instance.product.slug}/{filename}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=product_image_upload_to)
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.title}"

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"


class Wishlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="wishlist"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "user",
            "product",
        )

    def __str__(self):
        return f"{self.user.email} - {self.product.title}"
