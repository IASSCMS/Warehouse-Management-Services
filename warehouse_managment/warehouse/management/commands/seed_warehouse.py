from django.core.management.base import BaseCommand
from warehouse.models import Warehouse, Inventory
from product.models import Product

class Command(BaseCommand):
    help = "Seed the warehouse and inventory tables with initial data"

    def handle(self, *args, **kwargs):
        if Warehouse.objects.exists():
            self.stdout.write("Warehouses already seeded.")
            return

        w1 = Warehouse.objects.create(name="Main Warehouse", location="Colombo", capacity=10000)
        w2 = Warehouse.objects.create(name="Backup Warehouse", location="Kandy", capacity=5000)

        # Assuming product entries already exist
        p1 = Product.objects.filter(sku="SKU001").first()
        p2 = Product.objects.filter(sku="SKU002").first()

        if p1 and p2:
            Inventory.objects.create(product=p1, warehouse=w1, quantity=200)
            Inventory.objects.create(product=p2, warehouse=w2, quantity=150)

        self.stdout.write(self.style.SUCCESS("Seeded warehouse and inventory tables successfully."))
