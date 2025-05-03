from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from decimal import Decimal
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

class MarkDeliveryReceivedView(APIView):
    def post(self, request):
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

            return Response({'status': 'updated'})
        except WarehouseInventory.DoesNotExist:
            return Response({'error': 'Inventory not found'}, status=404)
