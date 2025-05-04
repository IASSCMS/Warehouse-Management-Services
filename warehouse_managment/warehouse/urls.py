from django.urls import path
from .views import (
    warehouse_list,
    warehouse_inventory_list,
    transaction_list,
    mark_delivery_received,
    supplier_inventory,
    supplier_dashboard
)

urlpatterns = [
    # Returns a list of all warehouses
    path('warehouses/', warehouse_list, name='warehouse-list'),

    # Returns a list of all warehouse inventory records
    path('inventory/', warehouse_inventory_list, name='inventory-list'),

    # Returns a list of all inventory transactions (incoming deliveries etc.)
    path('transactions/', transaction_list, name='transaction-list'),

    # POST endpoint to mark a delivery as received by a warehouse
    # Updates inventory and logs transaction, and also calls product service
    path('mark-delivery-received/', mark_delivery_received, name='mark-delivery'),

    # GET endpoint to return current inventory items for a specific supplier
    # Requires supplier_id in query params (?supplier_id=...)
    path('supplier-inventory/', supplier_inventory, name='supplier-inventory'),

    # GET endpoint to return a dashboard summary for a supplier
    # Includes product names, stock quantity, last restocked date, and warehouse info
    # Requires supplier_id in query params (?supplier_id=...)
    path('supplier-dashboard/', supplier_dashboard, name='supplier-dashboard'),
]
