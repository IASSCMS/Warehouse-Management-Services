from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from decimal import Decimal
import requests  # for internal call
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

# 1. Dashboard Summary (current stock count, last restock, total value)
class SupplierDashboardView(APIView):
    def get(self, request):
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

# 2. Mark delivery received by warehouse
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
        except WarehouseInventory.DoesNotExist:
            return Response({'error': 'Inventory not found'}, status=404)

        # Update inventory
        inventory.quantity += Decimal(quantity)
        inventory.last_restocked = timezone.now()
        inventory.save()

        # Record transaction
        InventoryTransaction.objects.create(
            inventory=inventory,
            transaction_type='INCOMING',
            quantity_change=quantity,
            reference_number="DELIVERY",
            created_by=f"Supplier {supplier_id}"
        )

        # 3. Call product service to update SupplierProduct max capacity
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

# 4. View current stock of supplier's warehouse only
class SupplierInventoryView(APIView):
    def get(self, request):
        supplier_id = request.query_params.get('supplier_id')
        if not supplier_id:
            return Response({"error": "supplier_id required"}, status=400)
        
        inventory = WarehouseInventory.objects.filter(supplier_id=supplier_id)
        serializer = WarehouseInventorySerializer(inventory, many=True)
        return Response(serializer.data)
