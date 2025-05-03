from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WarehouseViewSet, WarehouseInventoryViewSet, InventoryTransactionViewSet,
    MarkDeliveryReceivedView, SupplierInventoryView, SupplierDashboardView
)

router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)
router.register(r'inventory', WarehouseInventoryViewSet)
router.register(r'transactions', InventoryTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('mark-delivery-received/', MarkDeliveryReceivedView.as_view(), name='mark-delivery'),
    path('supplier-inventory/', SupplierInventoryView.as_view(), name='supplier-inventory'),
    path('supplier-dashboard/', SupplierDashboardView.as_view()),
]
