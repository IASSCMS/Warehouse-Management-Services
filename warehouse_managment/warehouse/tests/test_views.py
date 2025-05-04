from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from warehouse.models import Warehouse, WarehouseInventory, InventoryTransaction
from product.models import Product, ProductCategory

class WarehouseTests(APITestCase):
    def setUp(self):
        # Create test data
        self.category = ProductCategory.objects.create(category_name="Electronics")
        self.product = Product.objects.create(product_name="Laptop", unit_price=1000.00, category=self.category)
        self.warehouse = Warehouse.objects.create(location_x="10", location_y="20", warehouse_name="Main Warehouse")
        self.inventory = WarehouseInventory.objects.create(warehouse=self.warehouse, product=self.product, supplier_id=1, quantity=50)
        self.transaction = InventoryTransaction.objects.create(inventory=self.inventory, transaction_type='INCOMING', quantity_change=50, created_by="Test User")

    def test_warehouse_list(self):
        url = reverse('warehouse-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_warehouse_inventory_list(self):
        url = reverse('inventory-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_transaction_list(self):
        url = reverse('transaction-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_supplier_dashboard(self):
        url = reverse('supplier-dashboard') + '?supplier_id=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

 

    def test_supplier_inventory(self):
        url = reverse('supplier-inventory') + '?supplier_id=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
