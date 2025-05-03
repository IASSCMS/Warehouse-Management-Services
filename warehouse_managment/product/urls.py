from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductCategoryViewSet, ProductViewSet, SupplierProductViewSet,
    root, product_list, product_detail, UpdateSupplierProductView
)

router = DefaultRouter()
router.register(r'categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'supplier-products', SupplierProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('update-supplier-product/', UpdateSupplierProductView.as_view(), name='update-supplier-product'),
    path('', root),
    path('list/', product_list),
    path('<int:pk>/', product_detail),
]
