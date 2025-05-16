from django.contrib import admin
from .models import Warehouse, WarehouseInventory, InventoryTransaction, SupplierProduct

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'warehouse_name', 'location_x', 'location_y', 'created_at')

@admin.register(WarehouseInventory)
class WarehouseInventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'warehouse', 'product', 'quantity', 'last_restocked', 'minimum_stock_level')
    list_filter = ('warehouse', 'product')

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'inventory', 'transaction_type', 'quantity_change', 'created_at', 'created_by')
    list_filter = ('transaction_type', 'created_by')

@admin.register(SupplierProduct)
class SupplierProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier_id', 'product', 'warehouse', 'maximum_capacity', 'supplier_price', 'lead_time_days')
    list_filter = ('warehouse', 'supplier_id')
    search_fields = ('supplier_id', 'product__product_name')
    