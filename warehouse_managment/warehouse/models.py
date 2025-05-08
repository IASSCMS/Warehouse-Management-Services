from django.db import models
from product.models import Product

class Warehouse(models.Model):
    location_x = models.CharField(max_length=64)
    location_y = models.CharField(max_length=64)
    warehouse_name = models.CharField(max_length=100, blank=True)
    capacity = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'warehouse'

class WarehouseInventory(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    last_restocked = models.DateTimeField(blank=True, null=True)
    minimum_stock_level = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'warehouse_inventory'
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=0),
                name='positive_quantity'
            )
        ]

class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('INCOMING', 'Incoming'),
        ('OUTGOING', 'Outgoing'),
        ('ADJUSTMENT', 'Adjustment'),
    ]

    inventory = models.ForeignKey(WarehouseInventory, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity_change = models.DecimalField(max_digits=10, decimal_places=2)
    reference_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    class Meta:
        db_table = 'inventory_transactions'

class WarehouseSupplier(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    supplier_id = models.IntegerField()

    class Meta:
        db_table = 'warehouse_supplier'
        unique_together = (('warehouse', 'supplier_id'),)
        
