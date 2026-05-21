from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField("nombre", max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField("descripción", blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:category_detail", args=[self.pk])


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products",
        verbose_name="categoría"
    )
    name = models.CharField("nombre", max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField("descripción")
    price = models.DecimalField("precio", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("stock", default=0)
    available = models.BooleanField("disponible", default=True)
    created_at = models.DateTimeField("fecha de creación", auto_now_add=True)
    updated_at = models.DateTimeField("fecha de actualización", auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.pk])


class ProductReview(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews",
        verbose_name="producto"
    )
    author_name = models.CharField("nombre del autor", max_length=100)
    rating = models.IntegerField("puntuación", choices=RATING_CHOICES)
    comment = models.TextField("comentario", blank=True)
    created_at = models.DateTimeField("fecha de creación", auto_now_add=True)

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author_name} - {self.product.name} ({self.rating}/5)"
