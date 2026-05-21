from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Category, Product, ProductReview


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics", slug="electronics", description="Gadgets and devices"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Electronics")
        self.assertEqual(self.category.slug, "electronics")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Electronics")

    def test_category_absolute_url(self):
        url = self.category.get_absolute_url()
        self.assertEqual(url, reverse("store:category_detail", args=[self.category.pk]))

    def test_category_verbose_name_plural(self):
        self.assertEqual(str(Category._meta.verbose_name_plural), "Categorías")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Books", slug="books")
        self.product = Product.objects.create(
            category=self.category,
            name="Django Guide",
            slug="django-guide",
            description="A comprehensive guide to Django",
            price=29.99,
            stock=10,
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Django Guide")
        self.assertEqual(self.product.price, 29.99)
        self.assertEqual(self.product.stock, 10)
        self.assertTrue(self.product.available)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Django Guide")

    def test_product_absolute_url(self):
        url = self.product.get_absolute_url()
        self.assertEqual(url, reverse("store:product_detail", args=[self.product.pk]))

    def test_product_default_ordering(self):
        Product.objects.create(
            category=self.category,
            name="Another Book",
            slug="another-book",
            description="Another book",
            price=9.99,
            stock=5,
        )
        products = Product.objects.all()
        self.assertEqual(products[0].name, "Another Book")


class ProductReviewModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Clothing", slug="clothing")
        self.product = Product.objects.create(
            category=category,
            name="T-Shirt",
            slug="t-shirt",
            description="Cotton t-shirt",
            price=19.99,
            stock=50,
        )
        self.review = ProductReview.objects.create(
            product=self.product,
            author_name="John",
            rating=5,
            comment="Excellent product!",
        )

    def test_review_creation(self):
        self.assertEqual(self.review.author_name, "John")
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, "Excellent product!")

    def test_review_str(self):
        expected = "John - T-Shirt (5/5)"
        self.assertEqual(str(self.review), expected)

    def test_rating_choices(self):
        invalid_choices = [0, 6, -1]
        for rating in invalid_choices:
            with self.assertRaises(ValidationError):
                review = ProductReview(
                    product=self.product,
                    author_name="Jane",
                    rating=rating,
                    comment="test",
                )
                review.full_clean()


class ProductListViewTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Test Cat", slug="test-cat")
        for i in range(3):
            Product.objects.create(
                category=category,
                name=f"Product {i}",
                slug=f"product-{i}",
                description=f"Description {i}",
                price=10.00 + i,
                stock=5,
            )

    def test_view_url_exists(self):
        response = self.client.get("/store/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse("store:product_list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("store:product_list"))
        self.assertTemplateUsed(response, "store/product_list.html")

    def test_view_displays_products(self):
        response = self.client.get(reverse("store:product_list"))
        for i in range(3):
            self.assertContains(response, f"Product {i}")

    def test_view_context_contains_categories(self):
        response = self.client.get(reverse("store:product_list"))
        self.assertIn("categories", response.context)
        self.assertIn("search_form", response.context)


class ProductDetailViewTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Test", slug="test")
        self.product = Product.objects.create(
            category=category,
            name="Test Product",
            slug="test-product",
            description="A test",
            price=15.00,
            stock=3,
        )

    def test_detail_view_returns_product(self):
        response = self.client.get(
            reverse("store:product_detail", args=[self.product.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["product"].name, "Test Product")

    def test_detail_view_404_for_invalid_pk(self):
        response = self.client.get(
            reverse("store:product_detail", args=[9999])
        )
        self.assertEqual(response.status_code, 404)


class ProductCreateViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Tools", slug="tools")

    def test_create_view_get(self):
        response = self.client.get(reverse("store:product_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "store/product_form.html")

    def test_create_view_post_creates_product(self):
        data = {
            "category": self.category.id,
            "name": "New Tool",
            "slug": "new-tool",
            "description": "A brand new tool",
            "price": "49.99",
            "stock": 20,
            "available": True,
        }
        response = self.client.post(reverse("store:product_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(slug="new-tool").exists())


class ProductUpdateViewTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Garden", slug="garden")
        self.product = Product.objects.create(
            category=category,
            name="Old Name",
            slug="old-name",
            description="Old desc",
            price=5.00,
            stock=10,
        )

    def test_update_view_get(self):
        response = self.client.get(
            reverse("store:product_update", args=[self.product.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_update_view_post_updates_product(self):
        data = {
            "category": self.product.category.id,
            "name": "New Name",
            "slug": "new-name",
            "description": "Updated desc",
            "price": "15.00",
            "stock": 25,
            "available": True,
        }
        response = self.client.post(
            reverse("store:product_update", args=[self.product.pk]), data
        )
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "New Name")


class ProductDeleteViewTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Delete", slug="delete")
        self.product = Product.objects.create(
            category=category,
            name="Delete Me",
            slug="delete-me",
            description="To be deleted",
            price=1.00,
            stock=1,
        )

    def test_delete_view_get(self):
        response = self.client.get(
            reverse("store:product_delete", args=[self.product.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "store/product_confirm_delete.html")

    def test_delete_view_post_deletes_product(self):
        response = self.client.post(
            reverse("store:product_delete", args=[self.product.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(slug="delete-me").exists())


class SearchFormTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Search", slug="search")
        Product.objects.create(
            category=category,
            name="Red Shirt",
            slug="red-shirt",
            description="A red shirt",
            price=10.00,
            stock=5,
        )
        Product.objects.create(
            category=category,
            name="Blue Pants",
            slug="blue-pants",
            description="Blue pants",
            price=20.00,
            stock=3,
        )

    def test_search_finds_matching_products(self):
        response = self.client.get(reverse("store:product_list"), {"query": "shirt"})
        self.assertContains(response, "Red Shirt")
        self.assertNotContains(response, "Blue Pants")

    def test_search_empty_returns_all(self):
        response = self.client.get(reverse("store:product_list"), {"query": ""})
        self.assertContains(response, "Red Shirt")
        self.assertContains(response, "Blue Pants")


class CategoryDetailViewTest(TestCase):
    def setUp(self):
        self.cat1 = Category.objects.create(name="Cat A", slug="cat-a")
        self.cat2 = Category.objects.create(name="Cat B", slug="cat-b")
        Product.objects.create(
            category=self.cat1,
            name="A Product",
            slug="a-product",
            description="In cat A",
            price=5.00,
            stock=2,
        )
        Product.objects.create(
            category=self.cat2,
            name="B Product",
            slug="b-product",
            description="In cat B",
            price=8.00,
            stock=3,
        )

    def test_category_filter(self):
        response = self.client.get(
            reverse("store:category_detail", args=[self.cat1.pk])
        )
        self.assertContains(response, "A Product")
        self.assertNotContains(response, "B Product")


class AddReviewViewTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Rev", slug="rev")
        self.product = Product.objects.create(
            category=category,
            name="Reviewable",
            slug="reviewable",
            description="A product for review",
            price=100.00,
            stock=1,
        )

    def test_add_review_get(self):
        response = self.client.get(
            reverse("store:add_review", args=[self.product.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "store/add_review.html")

    def test_add_review_post_creates_review(self):
        data = {"author_name": "Alice", "rating": 4, "comment": "Great!"}
        response = self.client.post(
            reverse("store:add_review", args=[self.product.pk]), data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.product.reviews.count(), 1)
        self.assertEqual(self.product.reviews.first().author_name, "Alice")
