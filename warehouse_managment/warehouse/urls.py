from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WarehouseViewSet, WarehouseInventoryViewSet, InventoryTransactionViewSet

router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)
router.register(r'inventory', WarehouseInventoryViewSet)
router.register(r'transactions', InventoryTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
