from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductCategoryViewSet, ProductViewSet, SupplierProductViewSet, UpdateSupplierProductView

router = DefaultRouter()
router.register(r'categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'supplier-products', SupplierProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('update-supplier-product/', UpdateSupplierProductView.as_view()),
]
