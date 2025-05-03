from django.test import TestCase
from rest_framework.test import APIClient
from .models import Warehouse, WarehouseInventory, InventoryTransaction
from product.models import ProductCategory, Product

class WarehouseTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = ProductCategory.objects.create(category_name="Grains")
        self.product = Product.objects.create(product_name="Rice", unit_price=50, category=self.category)
        self.warehouse = Warehouse.objects.create(location_x="6.9271", location_y="79.8612", warehouse_name="Colombo")
        self.inventory = WarehouseInventory.objects.create(
            warehouse=self.warehouse,
            product=self.product,
            supplier_id=2,
            quantity=10
        )

    def test_mark_delivery_received(self):
        url = "/api/warehouse/mark-delivery-received/"
        data = {
            "supplier_id": 2,
            "product_id": self.product.id,
            "quantity": "20"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.inventory.refresh_from_db()
        self.assertEqual(float(self.inventory.quantity), 30.0)
        self.assertTrue(InventoryTransaction.objects.filter(inventory=self.inventory).exists())

    def test_get_supplier_inventory(self):
        url = "/api/warehouse/supplier-inventory/?supplier_id=2"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['supplier_id'], 2)
