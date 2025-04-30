from django.urls import path
from .views import (
    warehouse_inventory_list,
    warehouse_list,
    warehouse_inventory_create,
    warehouse_create
)

urlpatterns = [
    path('warehouses-with-inventory/', warehouse_inventory_list, name='warehouses-with-inventory'),
    path('warehouses/', warehouse_list, name='warehouses'),
    path('add-warehouse-inventory/', warehouse_inventory_create, name='add-warehouse-inventory'),
    path('add-warehouse/', warehouse_create, name='add-warehouse'),
]
