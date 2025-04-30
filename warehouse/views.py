from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Warehouse
from .serializers import WarehouseSerializer, SimpleWarehouseSerializer

@api_view(['GET'])
def warehouse_inventory_list(request):
    # List warehouses + inventories
    warehouses = Warehouse.objects.prefetch_related('inventories').all()
    serializer = WarehouseSerializer(warehouses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def warehouse_list(request):
    # List warehouses without inventories
    warehouses = Warehouse.objects.all()
    serializer = SimpleWarehouseSerializer(warehouses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def warehouse_inventory_create(request):
    # Create warehouse + inventories together
    serializer = WarehouseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def warehouse_create(request):
    # Create warehouse only
    serializer = SimpleWarehouseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
