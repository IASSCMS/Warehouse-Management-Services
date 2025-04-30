from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Warehouse, Inventory
from .serializers import (
    WarehouseSerializer,
    SimpleWarehouseSerializer,
    InventoryCreateSerializer
)

@api_view(['GET'])
def warehouse_inventory_list(request):
    warehouses = Warehouse.objects.prefetch_related('inventories').all()
    serializer = WarehouseSerializer(warehouses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    serializer = SimpleWarehouseSerializer(warehouses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def warehouse_inventory_detail(request, warehouse_id):
    try:
        warehouse = Warehouse.objects.prefetch_related('inventories').get(id=warehouse_id)
    except Warehouse.DoesNotExist:
        return Response({"error": "Warehouse not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = WarehouseSerializer(warehouse)
    return Response(serializer.data)

@api_view(['POST'])
def warehouse_create(request):
    serializer = SimpleWarehouseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def warehouse_inventory_create(request):
    warehouse_id = request.data.get('warehouse_id')
    try:
        warehouse = Warehouse.objects.get(id=warehouse_id)
    except Warehouse.DoesNotExist:
        return Response({'error': 'Warehouse not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = InventoryCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(warehouse=warehouse)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
