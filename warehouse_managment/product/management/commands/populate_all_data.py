from django.core.management.base import BaseCommand
from product.models import ProductCategory, Product, SupplierProduct
from warehouse.models import Warehouse, WarehouseInventory,InventoryTransaction
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Delete old data and populate categories, products, suppliers, warehouses, and inventory'

    def handle(self, *args, **kwargs):
        self.stdout.write("🧹 Deleting existing data...")
        # SupplierProduct.objects.all().delete()
        # Product.objects.all().delete()
        # ProductCategory.objects.all().delete()
        # WarehouseInventory.objects.all().delete()
        # Warehouse.objects.all().delete()
        # InventoryTransaction.objects.all().delete()

        # Product categories
        category_names = ['Cinnamon', 'Pepper', 'Cardamom', 'Chili']
        categories = []
        for name in category_names:
            category = ProductCategory.objects.create(
                category_name=name,
                description=f"{name} spice"
            )
            categories.append(category)

        # Products
        products = []
        for i in range(10):
            category = random.choice(categories)
            product = Product.objects.create(
                product_name=f"{category.category_name} Product {i + 1}",
                unit_price=round(random.uniform(100, 2000), 2),
                category=category
            )
            products.append(product)

        # Warehouses
        warehouse1 = Warehouse.objects.create(
            warehouse_name="Colombo Central", location_x="6.9271° N", location_y="79.8612° E"
        )
        warehouse2 = Warehouse.objects.create(
            warehouse_name="Kandy Depot", location_x="7.2906° N", location_y="80.6337° E"
        )
        warehouse3 = Warehouse.objects.create(
            warehouse_name="Kurunegala Rock", location_x="7.0032° N", location_y="80.1102° E"
        )
        warehouses = [warehouse1, warehouse2, warehouse3]

        # Supplier products & warehouse inventory
        for product in products:
            for supplier_id in [101, 102]:
                SupplierProduct.objects.create(
                    supplier_id=supplier_id,
                    product=product,
                    maximum_capacity=random.randint(300000, 600000),
                    supplier_price=round(random.uniform(80, 1500), 2),
                    lead_time_days=random.randint(3, 10)
                )

                for warehouse in warehouses:
                    WarehouseInventory.objects.create(
                        warehouse=warehouse,
                        product=product,
                        supplier_id=supplier_id,
                        quantity=Decimal(random.uniform(100000, 400000)),
                        minimum_stock_level=Decimal("100000.00")
                    )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded all data!"))
