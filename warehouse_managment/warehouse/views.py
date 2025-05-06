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
    warehouse_id = request.query_params.get('warehouse_id')

    if warehouse_id:
        inventory = WarehouseInventory.objects.filter(warehouse_id=warehouse_id)
    else:
        inventory = WarehouseInventory.objects.all()

    serializer = WarehouseInventorySerializer(inventory, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def transaction_list(request):
    warehouse_id = request.query_params.get('warehouse_id')
    transactions = InventoryTransaction.objects.all()
    if warehouse_id:
        transactions = transactions.filter(inventory__warehouse_id=warehouse_id)

    serializer = InventoryTransactionSerializer(transactions, many=True)
    return Response(serializer.data)


# 4. Supplier Dashboard
@api_view(['GET'])
def supplier_dashboard(request):
    supplier_id = request.query_params.get('supplier_id')
    warehouse_id = request.query_params.get('warehouse_id')

    if not supplier_id:
        return Response({"error": "supplier_id required"}, status=400)

    inventory = WarehouseInventory.objects.filter(supplier_id=supplier_id)
    if warehouse_id:
        inventory = inventory.filter(warehouse_id=warehouse_id)

    summary = []
    for item in inventory:
        summary.append({
            "product": item.product.product_name,
            "quantity": float(item.quantity),
            "last_restocked": item.last_restocked,
        })
    return Response(summary)


@api_view(['POST'])
def mark_delivery_received(request):
    supplier_id = request.query_params.get('supplier_id')
    product_id = request.query_params.get('product_id')
    warehouse_id = request.query_params.get('warehouse_id')
    quantity = request.query_params.get('quantity')

    if not all([supplier_id, product_id, quantity, warehouse_id]):
        return Response({'error': 'Missing fields'}, status=400)

    try:
        inventory = WarehouseInventory.objects.get(
            supplier_id=supplier_id,
            product_id=product_id,
            warehouse_id=warehouse_id
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

    supplier_product, created = SupplierProduct.objects.get_or_create(
        supplier_id=supplier_id,
        product_id=product_id,
        defaults={"maximum_capacity": inventory.quantity}
    )
    if not created:
        supplier_product.maximum_capacity = inventory.quantity
        supplier_product.save()

    return Response({"status": "Delivery recorded and product updated"}, status=200)


@api_view(['GET'])
def get_supplier_products(request, supplier_id):
    inventory = WarehouseInventory.objects.filter(supplier_id=supplier_id)

    if not inventory.exists():
        return Response([], status=status.HTTP_200_OK)

    result = []
    product_ids = inventory.values_list('product_id', flat=True).distinct()

    for product_id in product_ids:
        product = Product.objects.filter(id=product_id).first()
        if not product:
            continue

        stock_level = inventory.filter(product_id=product_id).aggregate(
            total=Sum('quantity')
        )['total'] or 0


        supplier_product = SupplierProduct.objects.filter(
            product=product, supplier_id=supplier_id
        ).first()
        lead_time_days = supplier_product.lead_time_days if supplier_product else None

        result.append({
            "id": product.id,
            "name": product.product_name,
            "supplier_id": supplier_id,
            "lead_time_days": lead_time_days,
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

    product_ids = Product.objects.filter(category=category).values_list('id', flat=True)

    supplier_ids = WarehouseInventory.objects.filter(
        product_id__in=product_ids
    ).values_list('supplier_id', flat=True).distinct()

    return Response({"supplier_ids": list(supplier_ids)}, status=200)

