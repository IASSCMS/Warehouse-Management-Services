from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from product.models import Product, ProductCategory, SupplierProduct

class ProductTests(APITestCase):
    def setUp(self):
        # Create test data
        self.category = ProductCategory.objects.create(category_name="Electronics")
        self.product = Product.objects.create(product_name="Laptop", unit_price=1000.00, category=self.category)
        self.supplier_product = SupplierProduct.objects.create(supplier_id=1, product=self.product, maximum_capacity=100, supplier_price=900.00)

    def test_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_product_detail(self):
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_name'], "Laptop")

    def test_category_list(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_category_detail(self):
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['category_name'], "Electronics")


    def test_update_supplier_product(self):
        url = reverse('update-supplier-product')
        data = {
            'supplier_id': 1,
            'product_id': self.product.id,
            'maximum_capacity': 150
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Missing fields")

        # Update to use query parameters
        url = f"{url}?supplier_id=1&product_id={self.product.id}&maximum_capacity=150"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.supplier_product.refresh_from_db()
        self.assertEqual(self.supplier_product.maximum_capacity, 150)

    def test_supplier_product_list(self):
        # Test without product_id
        url = reverse('supplier-product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['supplier_id'], 1)
        self.assertEqual(float(response.data[0]['supplier_price']), float(self.supplier_product.supplier_price))
   