from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from shop.models import ProductCategory, Product, ProductStatus, ProductImage


# Register your models here.
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        'id',
    )

    ordering = ("-id",)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  
    max_num = 7  


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "slug",
        "id",
        "title",
        "stock",
        "status",
        "price",
        "discount",
    )
    list_filter = ['status',]
    search_fields = ['title', 'description']
    inlines = [ProductImageInline]

    ordering = ("-id",)

    actions = ['change_status_to_draft', 'change_status_to_published']

    def change_status_to_draft(self, request, queryset):
        queryset.update(status=ProductStatus.draft.value)
        self.message_user(request, _("Selected products have been marked as draft."))
    change_status_to_draft.short_description = _("Mark selected products as draft")

    def change_status_to_published(self, request, queryset):
        queryset.update(status=ProductStatus.published.value)
        self.message_user(request, _("Selected products have been marked as published."))
    change_status_to_published.short_description = _("Mark selected products as published")


    