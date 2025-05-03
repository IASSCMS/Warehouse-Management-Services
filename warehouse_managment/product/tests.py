from django.test import TestCase
from rest_framework.test import APIClient
from .models import Product, SupplierProduct, ProductCategory

class UpdateSupplierProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = ProductCategory.objects.create(category_name="Spices")
        self.product = Product.objects.create(product_name="Pepper", unit_price=100, category=self.category)
        self.supplier_product = SupplierProduct.objects.create(
            supplier_id=1,
            product=self.product,
            maximum_capacity=50,
            supplier_price=80.00
        )

    def test_update_supplier_product_success(self):
        url = "/api/product/update-supplier-product/"
        data = {
            "supplier_id": 1,
            "product_id": self.product.id,
            "maximum_capacity": 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.supplier_product.refresh_from_db()
        self.assertEqual(self.supplier_product.maximum_capacity, 100)

    def test_update_supplier_product_missing_fields(self):
        url = "/api/product/update-supplier-product/"
        data = {
            "supplier_id": 1,
            "product_id": self.product.id
            # Missing maximum_capacity
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
