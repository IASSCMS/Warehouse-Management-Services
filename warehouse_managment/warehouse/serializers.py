from rest_framework import serializers
from .models import Warehouse, WarehouseInventory, InventoryTransaction, WarehouseSupplier

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

class WarehouseInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseInventory
        fields = '__all__'

class InventoryTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTransaction
        fields = '__all__'
        
class WarehouseSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseSupplier
        fields = ['id', 'name', 'location']
