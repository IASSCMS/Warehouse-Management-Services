from django.contrib import admin
from .models import ProductCategory, Product, SupplierProduct

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'description')
    search_fields = ('category_name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'unit_price', 'category', 'created_at', 'updated_at')
    search_fields = ('product_name',)
    list_filter = ('category',)

@admin.register(SupplierProduct)
class SupplierProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier_id', 'product', 'maximum_capacity', 'supplier_price', 'lead_time_days')
    list_filter = ('supplier_id',)
