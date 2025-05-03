from django.core.management.base import BaseCommand
from product.models import ProductCategory, Product, SupplierProduct
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populate product categories, products, and supplier products'

    def handle(self, *args, **kwargs):
        # Define categories
        categories = [
            'Cinnamon', 'Pepper', 'Cloves', 'Cardamom', 'Nutmeg',
            'Turmeric', 'Coriander', 'Mustard Seed', 'Fennel', 'Fenugreek'
        ]

        # Create categories
        cat_objs = []
        for cat in categories:
            obj, _ = ProductCategory.objects.get_or_create(category_name=cat)
            cat_objs.append(obj)

        # Create products
        products = []
        for i, cat in enumerate(cat_objs):
            product = Product.objects.create(
                product_name=f"{cat.category_name} Premium Grade",
                unit_price=Decimal(random.uniform(5, 20)).quantize(Decimal("0.01")),
                category=cat
            )
            products.append(product)

        # Simulate SupplierProduct entries
        for product in products:
            for supplier_id in [101, 102]:  # Simulate two suppliers
                SupplierProduct.objects.update_or_create(
                    supplier_id=supplier_id,
                    product=product,
                    defaults={
                        'maximum_capacity': random.randint(500, 1000),
                        'supplier_price': Decimal(random.uniform(4, 15)).quantize(Decimal("0.01")),
                        'lead_time_days': random.randint(2, 7)
                    }
                )

        self.stdout.write(self.style.SUCCESS('✅ Product categories, products, and supplier products populated.'))
