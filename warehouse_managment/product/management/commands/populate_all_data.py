from django.core.management.base import BaseCommand
from product.models import ProductCategory, Product, SupplierProduct
from warehouse.models import Warehouse, WarehouseInventory, InventoryTransaction, WarehouseSupplier
from decimal import Decimal
from django.utils import timezone
import random
from datetime import timedelta


class Command(BaseCommand):
    help = 'Delete old data and populate categories, products, suppliers, warehouses, and inventory'

    def handle(self, *args, **kwargs):
        self.stdout.write("🧹 Deleting existing data...")

        # InventoryTransaction.objects.all().delete()
        # WarehouseInventory.objects.all().delete()
        # SupplierProduct.objects.all().delete()
        # Product.objects.all().delete()
        # ProductCategory.objects.all().delete()
        # WarehouseSupplier.objects.all().delete()
        # Warehouse.objects.all().delete()

        self.stdout.write("🧪 Populating new data...")

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
                product_SKU=f"SKU{i + 1:03}",
                product_name=f"{category.category_name} Product {i + 1}",
                unit_price=round(random.uniform(100, 2000), 2),
                category=category
            )
            products.append(product)

        # Warehouses (Randomly assigning warehouses to suppliers)
        warehouse_data = [
            ("Colombo Central", "6.9271° N", "79.8612° E"),
            ("Kandy Depot", "7.2906° N", "80.6337° E"),
            ("Kurunegala Rock", "7.0032° N", "80.1102° E"),
        ]
        warehouses = []
        for name, x, y in warehouse_data:
            warehouse = Warehouse.objects.create(
                warehouse_name=name,
                location_x=x,
                location_y=y,
                capacity=Decimal("100000000.00")
            )
            warehouses.append(warehouse)

        # SupplierProduct, WarehouseInventory, InventoryTransaction, WarehouseSupplier
        created_pairs = set()

        for product in products:
            # Randomly assign suppliers (not for all suppliers)
            suppliers = random.sample([101, 102, 103], k=random.randint(1, 3))  # Randomly pick 1 to 3 suppliers
            for supplier_id in suppliers:
                # SupplierProduct (Randomly create it for some suppliers)
                if random.choice([True, False]):
                    max_capacity = random.randint(300000, 600000)
                    lead_time = random.randint(3, 10)
                    SupplierProduct.objects.create(
                        supplier_id=supplier_id,
                        product=product,
                        maximum_capacity=max_capacity,
                        supplier_price=round(random.uniform(80, 1500), 2),
                        lead_time_days=lead_time
                    )
                
                # WarehouseSupplier (Randomly assign warehouses for this supplier)
                warehouse = random.choice(warehouses)  # Randomly pick one warehouse for this supplier
                if (warehouse.id, supplier_id) not in created_pairs:
                    WarehouseSupplier.objects.create(
                        warehouse=warehouse,
                        supplier_id=supplier_id
                    )
                    created_pairs.add((warehouse.id, supplier_id))

                # Inventory - ensure unique product_id and warehouse_id combination
                if not WarehouseInventory.objects.filter(warehouse=warehouse, product=product).exists():
                    quantity = Decimal(random.uniform(100000, 400000))
                    last_restocked = timezone.now() - timedelta(days=random.randint(1, 60))

                    inventory = WarehouseInventory.objects.create(
                        warehouse=warehouse,
                        product=product,
                        quantity=quantity,
                        last_restocked=last_restocked,
                        minimum_stock_level=Decimal("100000.00")
                    )

                    # Transactions
                    for _ in range(random.randint(1, 2)):
                        qty_in = Decimal(random.uniform(10000, 50000))
                        InventoryTransaction.objects.create(
                            inventory=inventory,
                            transaction_type='INCOMING',
                            quantity_change=qty_in,
                            reference_number=f"REF-{random.randint(1000,9999)}",
                            notes="Initial delivery",
                            created_by=f"Supplier {supplier_id}"
                        )

                    if random.choice([True, False]):
                        qty_out = Decimal(random.uniform(5000, 20000))
                        InventoryTransaction.objects.create(
                            inventory=inventory,
                            transaction_type='OUTGOING',
                            quantity_change=qty_out,
                            reference_number=f"OUT-{random.randint(1000,9999)}",
                            notes="Customer shipment",
                            created_by="System"
                        )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded all data!!!"))
