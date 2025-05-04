from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse

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
    description = models.TextField()
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
