from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WarehouseViewSet,
    WarehouseInventoryViewSet,
    InventoryTransactionViewSet,
    SupplierInventoryView,
    MarkDeliveryReceivedView,
)

router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)
router.register(r'inventories', WarehouseInventoryViewSet)
router.register(r'transactions', InventoryTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('supplier-inventory/', SupplierInventoryView.as_view(), name='supplier-inventory'),
    path('delivery-received/', MarkDeliveryReceivedView.as_view()),

]