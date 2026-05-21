from django.contrib import admin
from .models import Category, Product, ProductReview


class ProductInline(admin.TabularInline):
    model = Product
    fields = ["name", "price", "stock", "available"]
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "stock", "available", "created_at"]
    list_filter = ["available", "category", "created_at"]
    list_editable = ["price", "stock", "available"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = "created_at"


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "author_name", "rating", "created_at"]
    list_filter = ["rating", "created_at"]
    search_fields = ["author_name", "comment"]
