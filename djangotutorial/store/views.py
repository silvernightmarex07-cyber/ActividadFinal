from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Category, Product
from .forms import ProductForm, ProductReviewForm, SearchForm


class ProductListView(ListView):
    model = Product
    template_name = "store/product_list.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        queryset = Product.objects.filter(available=True)
        form = SearchForm(self.request.GET)
        if form.is_valid() and form.cleaned_data["query"]:
            q = form.cleaned_data["query"]
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(description__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["search_form"] = SearchForm(self.request.GET or None)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_form"] = ProductReviewForm()
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "store/product_form.html"
    success_url = reverse_lazy("store:product_list")


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "store/product_form.html"
    success_url = reverse_lazy("store:product_list")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "store/product_confirm_delete.html"
    success_url = reverse_lazy("store:product_list")


class CategoryDetailView(ListView):
    template_name = "store/product_list.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs["pk"])
        return self.category.products.filter(available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["search_form"] = SearchForm()
        return context


class AddReviewView(FormView):
    form_class = ProductReviewForm
    template_name = "store/add_review.html"

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs["pk"])
        review = form.save(commit=False)
        review.product = product
        review.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("store:product_detail", args=[self.kwargs["pk"]])
