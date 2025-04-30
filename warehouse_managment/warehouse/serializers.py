from rest_framework import serializers
from .models import Warehouse, Inventory
from product.models import Product

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'sku']

class InventorySerializer(serializers.ModelSerializer):
    product = ProductMiniSerializer()
    warehouse = WarehouseSerializer()

    class Meta:
        model = Inventory
        fields = ['id', 'product', 'warehouse', 'quantity', 'last_updated']
