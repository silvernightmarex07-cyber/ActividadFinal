from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("create/", views.ProductCreateView.as_view(), name="product_create"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("<int:pk>/update/", views.ProductUpdateView.as_view(), name="product_update"),
    path("<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),
    path("<int:pk>/review/", views.AddReviewView.as_view(), name="add_review"),
    path("category/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),
]
