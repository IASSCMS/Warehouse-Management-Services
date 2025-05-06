from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from decimal import Decimal
import requests
from product.models import Product, SupplierProduct, ProductCategory
from django.db.models import Sum
from .models import Warehouse, WarehouseInventory, InventoryTransaction
from .serializers import (
    WarehouseSerializer,
    WarehouseInventorySerializer,
    InventoryTransactionSerializer,
)

@api_view(['GET'])
def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    serializer = WarehouseSerializer(warehouses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def warehouse_inventory_list(request):
    inventory = WarehouseInventory.objects.all()
    serializer = WarehouseInventorySerializer(inventory, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def transaction_list(request):
    transactions = InventoryTransaction.objects.all()
    serializer = InventoryTransactionSerializer(transactions, many=True)
    return Response(serializer.data)

# 1. Supplier Dashboard
@api_view(['GET'])
def supplier_dashboard(request):
    supplier_id = request.query_params.get('supplier_id')
    if not supplier_id:
        return Response({"error": "supplier_id required"}, status=400)

    inventory = WarehouseInventory.objects.filter(supplier_id=supplier_id)
    summary = []
    for item in inventory:
        summary.append({
            "product": item.product.product_name,
            "quantity": float(item.quantity),
            "last_restocked": item.last_restocked,
            "warehouse": item.warehouse.warehouse_name,
        })
    return Response(summary)

# 2. Mark Delivery Received
@api_view(['POST'])
def mark_delivery_received(request):
    supplier_id = request.data.get('supplier_id')
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')

    if not all([supplier_id, product_id, quantity]):
        return Response({'error': 'Missing fields'}, status=400)

    try:
        inventory = WarehouseInventory.objects.get(
            supplier_id=supplier_id,
            product_id=product_id
        )
    except WarehouseInventory.DoesNotExist:
        return Response({'error': 'Inventory not found'}, status=404)

    inventory.quantity += Decimal(quantity)
    inventory.last_restocked = timezone.now()
    inventory.save()

    InventoryTransaction.objects.create(
        inventory=inventory,
        transaction_type='INCOMING',
        quantity_change=quantity,
        reference_number="DELIVERY",
        created_by=f"Supplier {supplier_id}"
    )

    # Internal API call to update product max capacity
    try:
        response = requests.post(
            "http://localhost:8000/api/product/update-supplier-product/",
            json={
                "supplier_id": supplier_id,
                "product_id": product_id,
                "maximum_capacity": inventory.quantity
            }
        )
        if response.status_code == 200:
            return Response({"status": "Delivery recorded and product updated"})
        else:
            return Response({"warning": "Delivery recorded but product update failed"}, status=202)
    except Exception as e:
        return Response({"error": f"Delivery recorded but product update call failed: {str(e)}"}, status=500)

# 3. Supplier's Products View
@api_view(['GET'])
def get_supplier_products(request, supplier_id):
    # Filter inventory by supplier
    inventory = WarehouseInventory.objects.filter(supplier_id=supplier_id)

    if not inventory.exists():
        return Response([], status=status.HTTP_200_OK)

    # Group by product
    result = []
    product_ids = inventory.values_list('product_id', flat=True).distinct()

    for product_id in product_ids:
        product = Product.objects.filter(id=product_id).first()
        if not product:
            continue

        stock_level = inventory.filter(product_id=product_id).aggregate(
            total=Sum('quantity')
        )['total'] or 0

        result.append({
            "id": product.id,
            "name": product.product_name,
            "supplier_id": supplier_id,
            "lead_time_days": 5,  # CASE
            "stock_level": int(stock_level),
        })

    return Response(result, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_suppliers_by_category(request):
    category_name = request.query_params.get('category')

    if not category_name:
        return Response({"error": "Category parameter is required."}, status=400)

    try:
        category = ProductCategory.objects.get(category_name__iexact=category_name)
    except ProductCategory.DoesNotExist:
        return Response({"supplier_ids": []}, status=200)

    # Get product IDs in this category
    product_ids = Product.objects.filter(category=category).values_list('id', flat=True)

    # Find unique supplier_ids from WarehouseInventory with these products
    supplier_ids = WarehouseInventory.objects.filter(
        product_id__in=product_ids
    ).values_list('supplier_id', flat=True).distinct()

    return Response({"supplier_ids": list(supplier_ids)}, status=200)

