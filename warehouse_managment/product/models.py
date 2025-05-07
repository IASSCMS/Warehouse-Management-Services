from django.db import models

class ProductCategory(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'product_category'

class Product(models.Model):
    product_SKU = models.CharField(max_length=30, unique=True, default='SKU000')
    product_name = models.CharField(max_length=60)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product'

class SupplierProduct(models.Model):
    supplier_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    maximum_capacity = models.IntegerField()
    supplier_price = models.DecimalField(max_digits=10, decimal_places=2)
    lead_time_days = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'supplier_product'
        unique_together = (('supplier_id', 'product'),)

