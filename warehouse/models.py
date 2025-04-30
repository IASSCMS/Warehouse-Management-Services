from django.db import models

class Warehouse(models.Model):
    objects = None
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Inventory(models.Model):
    warehouse = models.ForeignKey(Warehouse, related_name='inventories', on_delete=models.CASCADE)
    product_sku = models.CharField(max_length=50)
    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('warehouse', 'product_sku')

    def __str__(self):
        return f"{self.product_name} ({self.product_sku})"
