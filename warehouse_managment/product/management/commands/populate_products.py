from django.core.management.base import BaseCommand
from product.models import ProductCategory, Product
import random

class Command(BaseCommand):
    help = 'Seed product categories and 1000 products'

    def handle(self, *args, **kwargs):
        category_names = [
            'Cinnamon', 'Pepper', 'Cardamom', 'Chili'
        ]

        self.stdout.write("Creating categories...")
        categories = []
        for name in category_names:
            cat, created = ProductCategory.objects.get_or_create(
                category_name=name,
                defaults={'description': f'{name} spice'}
            )
            categories.append(cat)

        self.stdout.write("Creating 10 products...")
        Product.objects.all().delete()
        for i in range(10):
            category = random.choice(categories)
            Product.objects.create(
                product_name=f"{category.category_name} Product {i+1}",
                unit_price=round(random.uniform(100, 2000), 2),
                category=category
            )

        self.stdout.write(self.style.SUCCESS('✅ Seeded 4 categories and 10 products!'))
