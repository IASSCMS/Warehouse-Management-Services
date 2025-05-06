from django.core.management.base import BaseCommand
from warehouse.models import Warehouse, WarehouseInventory
from product.models import Product
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populate warehouses and their inventory'

    def handle(self, *args, **kwargs):
        # Create a couple of warehouses
        warehouse1, _ = Warehouse.objects.get_or_create(
            location_x="6.9271° N", location_y="79.8612° E", warehouse_name="Colombo Central"
        )
        warehouse2, _ = Warehouse.objects.get_or_create(
            location_x="7.2906° N", location_y="80.6337° E", warehouse_name="Kandy Depot"
        )
        warehouse3, _ = Warehouse.objects.get_or_create(
            location_x="7.0032° N", location_y="80.1102° E", warehouse_name="Kurunegala Rock"
        )

        # Assign random inventory to each product from each supplier
        products = Product.objects.all()

        for product in products:
            for supplier_id in [101, 102]:
                for warehouse in [warehouse1, warehouse2, warehouse3]:
                    WarehouseInventory.objects.update_or_create(
                        warehouse=warehouse,
                        product=product,
                        supplier_id=supplier_id,
                        defaults={
                            'quantity': Decimal(random.uniform(100000, 400000)),
                            'minimum_stock_level': Decimal("100000.00")
                        }
                    )

        self.stdout.write(self.style.SUCCESS('✅ Warehouses and inventory populated.'))
