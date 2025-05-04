from django.urls import path
from .views import (
    root,
    product_list,
    product_detail,
    category_list,
    category_detail,
    supplier_product_list,
    update_supplier_product,
    product_stock_summary,
)

urlpatterns = [
    path('', root, name='root'),
    
    # Product endpoints
    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),

    # Category endpoints
    path('categories/', category_list, name='category-list'),
    path('categories/<int:pk>/', category_detail, name='category-detail'),

    # Supplier product endpoints
    path('supplier-products/', supplier_product_list, name='supplier-product-list'),
    path('supplier-products/update/', update_supplier_product, name='update-supplier-product'),
    
    # Product count endpoint
    path('product-stock-summary/<str:sku_code>/', product_stock_summary),
]
