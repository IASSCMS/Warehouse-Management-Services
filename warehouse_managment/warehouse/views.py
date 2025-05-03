from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Warehouse, WarehouseInventory, InventoryTransaction
from .serializers import (
    WarehouseSerializer,
    WarehouseInventorySerializer,
    InventoryTransactionSerializer,
)

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class WarehouseInventoryViewSet(viewsets.ModelViewSet):
    queryset = WarehouseInventory.objects.all()
    serializer_class = WarehouseInventorySerializer

class InventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer

class SupplierInventoryView(APIView):
    def get(self, request):
        supplier_id = request.query_params.get('supplier_id')
        if not supplier_id:
            return Response({"error": "supplier_id is required"}, status=400)
        
        inventory = WarehouseInventory.objects.filter(supplier_id=supplier_id)
        serializer = WarehouseInventorySerializer(inventory, many=True)
        return Response(serializer.data)