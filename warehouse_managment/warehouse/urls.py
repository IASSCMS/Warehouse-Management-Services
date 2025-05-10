from django.urls import path
from .views import (
    warehouse_list,
    transaction_list,
    mark_delivery_received,
    get_supplier_products,
    supplier_dashboard,
    get_suppliers_by_category,
    warehouse_inventory_list,
    order_inventory_summary,
    handle_order_status,
    add_supplier_product,
    get_supplier_product_prices
)

urlpatterns = [
    # Returns a list of all warehouses
    path('warehouses/', warehouse_list, name='warehouse-list'),

    # Returns a list of all warehouse inventory records
    path('inventory/', warehouse_inventory_list, name='inventory-by-warehouse'),
    
    # Returns a list of all inventory transactions (incoming deliveries etc.)
    path('transactions/warehouse/<int:warehouse_id>/', transaction_list, name='transaction-list'), 
       
    # GET endpoint to return a dashboard summary for a supplier
    # Includes product names, stock quantity, last restocked date, and warehouse info
    # Requires supplier_id in query params (?supplier_id=...)
    path('supplier-dashboard/', supplier_dashboard, name='supplier-dashboard'),

    # POST endpoint to mark a delivery as received by a warehouse
    # Updates inventory and logs transaction, and also calls product service
    path('mark-delivery-received/', mark_delivery_received, name='mark-delivery'),

    # GET endpoint to return current inventory items for a specific supplier
    # Requires supplier_id in query params (?supplier_id=...)
    path('suppliers/<int:supplier_id>/products', get_supplier_products, name='supplier-products'),

    # GET suppliers by category
    path('suppliers-by-category', get_suppliers_by_category, name='suppliers-by-category'),
    
    # GET Product counts and names by orders
    path('order-inventory-summary/', order_inventory_summary),
    
    # POST endpoint to accept or reject an order request and update inventory
    path('order/handle/', handle_order_status, name='handle_order_status'),
    # POST endpoint to add or update a supplier product
    path("/supplier-product/add_or_update/", add_supplier_product, name="update_supplier_product"),
    
    # GET endpoint to get supplier product prices
    path('supplier-product/prices/', get_supplier_product_prices, name='get_supplier_product_prices'),
]


