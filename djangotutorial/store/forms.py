from django import forms
from .models import Product, ProductReview


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "name", "slug", "description", "price", "stock", "available"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ["author_name", "rating", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3}),
            "rating": forms.RadioSelect(choices=ProductReview.RATING_CHOICES),
        }


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        label="Buscar",
        widget=forms.TextInput(attrs={"placeholder": "Buscar productos..."}),
    )
