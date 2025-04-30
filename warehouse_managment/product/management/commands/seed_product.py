from django.core.management.base import BaseCommand
from product.models import Product

class Command(BaseCommand):
    help = "Seed the product table with initial data"

    def handle(self, *args, **kwargs):
        if Product.objects.exists():
            self.stdout.write("Products already seeded.")
            return

        Product.objects.create(name="Red Chilli Powder", sku="SKU001", description="Spicy and organic", price=100)
        Product.objects.create(name="Turmeric Powder", sku="SKU002", description="Rich in curcumin", price=80)

        self.stdout.write(self.style.SUCCESS("Seeded product table successfully."))
