from django.urls import path
from . import views

urlpatterns = [
    path("", views.root, name="warehouse_root"),
    path('warehouses/', views.warehouse_list, name='warehouse-list'),
    path('warehouses/<int:pk>/', views.warehouse_detail, name='warehouse-detail'),
    path('inventory/', views.inventory_list, name='inventory-list'),
    path('inventory/<int:pk>/', views.inventory_detail, name='inventory-detail'),
]