from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Warehouse, Inventory
from .serializers import WarehouseSerializer, InventorySerializer

@api_view(['GET'])
def root(request):
    """
    Root endpoint for the warehouse system.
    """
    return Response({"message": "Welcome to the Warehouse Management System!"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def warehouse_list(request):
    """
    List all warehouses.
    """
    warehouses = Warehouse.objects.all()
    serializer = WarehouseSerializer(warehouses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def warehouse_detail(request, pk):
    """
    Retrieve a warehouse by ID.
    """
    try:
        warehouse = Warehouse.objects.get(pk=pk)
    except Warehouse.DoesNotExist:
        return Response({'error': 'Warehouse not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = WarehouseSerializer(warehouse)
    return Response(serializer.data)

@api_view(['GET'])
def inventory_list(request):
    """
    List all inventory records.
    """
    inventory = Inventory.objects.select_related('product', 'warehouse').all()
    serializer = InventorySerializer(inventory, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def inventory_detail(request, pk):
    """
    Retrieve a single inventory record by ID.
    """
    try:
        inventory = Inventory.objects.get(pk=pk)
    except Inventory.DoesNotExist:
        return Response({'error': 'Inventory not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = InventorySerializer(inventory)
    return Response(serializer.data)
