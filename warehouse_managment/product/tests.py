from django.test import TestCase
from .models import Product

class ProductModelTest(TestCase):
    def test_create_product(self):
        product = Product.objects.create(
            name="Test Product",
            sku="SKU123",
            description="Test description",
            price=100.00
        )
        self.assertEqual(product.name, "Test Product")
