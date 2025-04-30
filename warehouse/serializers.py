from rest_framework import serializers
from .models import Warehouse, Inventory

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('id', 'product_sku', 'product_name', 'quantity')

class InventoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('product_sku', 'product_name', 'quantity')

class WarehouseSerializer(serializers.ModelSerializer):
    inventories = InventorySerializer(many=True, read_only=True)

    class Meta:
        model = Warehouse
        fields = ('id', 'name', 'location', 'capacity', 'inventories')

class SimpleWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ('id', 'name', 'location', 'capacity')
