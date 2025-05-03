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
    path('mark-delivery/', MarkDeliveryReceivedView.as_view()),
    path('supplier-stock/', SupplierInventoryView.as_view()),
    path('supplier-dashboard/', SupplierDashboardView.as_view()),
]
