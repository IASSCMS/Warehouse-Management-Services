import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from decimal import Decimal
from collections import defaultdict
from product.models import Product, SupplierProduct, ProductCategory
from django.db.models import Sum, F
from django.db import transaction
from .models import Warehouse, WarehouseInventory, InventoryTransaction, WarehouseSupplier
from .utils.supplier_names import SUPPLIER_NAME_MAP
from .utils.mock_orders import ORDERS
from .utils.order_accept_Req import ORDER_REQUEST
from .serializers import (
    WarehouseSerializer,
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
    if not warehouse_id:
        return Response({"error": "warehouse_id is required"}, status=400)

    try:
        warehouse = Warehouse.objects.get(id=warehouse_id)
    except Warehouse.DoesNotExist:
        return Response({"error": "Warehouse not found"}, status=404)

    supplier_ids = WarehouseSupplier.objects.filter(warehouse_id=warehouse_id).values_list('supplier_id', flat=True)
    inventory_qs = WarehouseInventory.objects.filter(warehouse_id=warehouse_id).select_related('product', 'product__category')

    supplier_products = SupplierProduct.objects.filter(
        supplier_id__in=supplier_ids,
        product_id__in=inventory_qs.values_list('product_id', flat=True)
    ).values('product_id', 'supplier_id')

    product_supplier_map = defaultdict(set)
    for sp in supplier_products:
        supplier_id = sp['supplier_id']
        supplier_name = SUPPLIER_NAME_MAP.get(supplier_id, f"Supplier {supplier_id}")
        product_supplier_map[sp['product_id']].add(supplier_name)

    product_data = defaultdict(lambda: {
        "product_name": "",
        "category": "",
        "product_count": 0,
        "supplied_by": set(),
        "supplied_date": None
    })

    for item in inventory_qs:
        product_id = item.product.id
        data = product_data[product_id]

        data["product_name"] = item.product.product_name
        data["category"] = item.product.category.category_name
        data["product_count"] += float(item.quantity)
        data["supplied_by"].update(product_supplier_map.get(product_id, set()))

        if not data["supplied_date"] or item.created_at.date() > data["supplied_date"]:
            data["supplied_date"] = item.created_at.date()
    inventory_product_details = []
    for data in product_data.values():
        inventory_product_details.append({
            "product_name": data["product_name"],
            "category": data["category"],
            "supplied_by": ", ".join(sorted(data["supplied_by"])),
            "supplied_date": data["supplied_date"],
            "product_count": round(data["product_count"], 2)
        })

    result = {
        "warehouse_city": warehouse.warehouse_name,
        "capacity": float(warehouse.capacity),
        "last_restocked": inventory_qs.order_by('-last_restocked').values_list('last_restocked', flat=True).first().date() if inventory_qs.exists() else None,
        "current_stock_level": round(inventory_qs.aggregate(total=Sum('quantity'))['total'] or 0, 2),
        "inventory_product_details": inventory_product_details
    }

    return Response(result, status=200)


@api_view(['GET'])
def transaction_list(request, warehouse_id):
    transactions = InventoryTransaction.objects.all()
    if warehouse_id:
        transactions = transactions.filter(inventory__warehouse_id=warehouse_id)

    serializer = InventoryTransactionSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def supplier_dashboard(request):
    supplier_id = request.query_params.get('supplier_id')
    if not supplier_id:
        return Response({"error": "supplier_id required"}, status=400)

    warehouses = WarehouseSupplier.objects.filter(supplier_id=supplier_id).values_list('warehouse_id', flat=True)

    inventories = (
        WarehouseInventory.objects
        .filter(warehouse_id__in=warehouses)
        .select_related('product', 'warehouse')
        .filter(product__supplierproduct__supplier_id=supplier_id)
        .values(
            'product__product_name',
            'product__product_SKU',
            'warehouse__warehouse_name'
        )
        .annotate(total_quantity=Sum('quantity'))
    )

    summary = [
        {
            "product_name": item['product__product_name'],
            "SKU": item['product__product_SKU'],
            "warehouse": item['warehouse__warehouse_name'],
            "Quantity_on_hand": float(item['total_quantity']),
        }
        for item in inventories
    ]

    return Response(summary)

@api_view(['POST'])
def mark_delivery_received(request):
    data = request.data
    required_fields = ['requestId', 'product_id', 'supplier_id', 'warehouse_id', 'quantity', 'status', 'is_defective', 'quality', 'comments']


    if not all(field in data for field in required_fields):
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        quantity = Decimal(data['quantity'])
        quality = int(data['quality'])
        is_defective = str(data['is_defective']).lower() == 'true'
        request_id = data['requestId']
        status_flag = data['status']
    except Exception as e:
        return Response({'error': f'Invalid input format: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    product_id = data['product_id']
    warehouse_id = data['warehouse_id']
    supplier_id = data['supplier_id']
    comments = data['comments']
    note = f"{comments} | Quality: {quality} | Defective: {is_defective}"

    try:

        inventory = WarehouseInventory.objects.select_related('warehouse', 'product').get(
            warehouse_id=warehouse_id,
            product_id=product_id
        )
    except WarehouseInventory.DoesNotExist:
        if status_flag == "returned":
            inventory = None
        else:
            inventory = WarehouseInventory.objects.create(
                warehouse_id=warehouse_id,
                product_id=product_id,
                quantity=quantity,
                last_restocked=timezone.now(),
                minimum_stock_level=Decimal("100000.00")
            )
    else:
        if status_flag == "received":
            inventory.quantity += quantity
            inventory.last_restocked = timezone.now()
            inventory.save()

    if status_flag == "received":
        sp, created = SupplierProduct.objects.get_or_create(
            supplier_id=supplier_id,
            product_id=product_id,
            defaults={"maximum_capacity": quantity,
                      "supplier_price": 0.0}
        )
        if not created:
            sp.maximum_capacity = max(sp.maximum_capacity, inventory.quantity)
            sp.save()

    try:
        status_update_payload = {
            "status": status_flag,
            "is_defective": str(is_defective).lower(),
            "quality": quality
        }
        response = requests.post(
            f"http://localhost:8000/api/v0/supplier-request/request/{request_id}/",
            json=status_update_payload,
            timeout=5
        )
        response.raise_for_status()

        
    except requests.RequestException as e:
        return Response({
            "error": f"Delivery processed, but failed to notify external system.",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    InventoryTransaction.objects.create(
        inventory=inventory,
        transaction_type='INCOMING' if status_flag == "received" else 'RETURNED',
        quantity_change=quantity,
        reference_number=f"{status_flag.upper()}-{request_id}",
        notes=note,
        created_by=f"Warehouse {warehouse_id}"
    )
    return Response({"status": f"Delivery {status_flag} and processed successfully."}, status=status.HTTP_200_OK)




@api_view(['GET'])
def get_supplier_products(request, supplier_id):
    warehouse_ids = WarehouseSupplier.objects.filter(supplier_id=supplier_id).values_list('warehouse_id', flat=True)

    inventory_qs = WarehouseInventory.objects.filter(warehouse_id__in=warehouse_ids)

    product_ids = inventory_qs.values_list('product_id', flat=True).distinct()

    products = (
        Product.objects
        .filter(id__in=product_ids)
        .select_related('category')
        .prefetch_related('supplierproduct_set')
    )

    stock_map = {
        pid: inventory_qs.filter(product_id=pid).aggregate(total=Sum('quantity'))['total'] or 0
        for pid in product_ids
    }

    result = []
    for product in products:
        sp = product.supplierproduct_set.filter(supplier_id=supplier_id).first()
        result.append({
            "id": product.id,
            "name": product.product_name,
            "supplier_id": supplier_id,
            "lead_time_days": sp.lead_time_days if sp else None,
            "stock_level": int(stock_map.get(product.id, 0)),
        })

    return Response(result)

@api_view(['GET'])
def get_supplier_product_prices(request): 
    supplier_id = request.query_params.get('supplier_id')
    if not supplier_id:
        return Response({"error": "supplier_id required"}, status=400)

    supplier_products = (
        SupplierProduct.objects
        .filter(supplier_id=supplier_id)
        .select_related('product')
        .annotate(
            product_name=F('product__product_name'),
            SKU=F('product__product_SKU')
        )
        .values('product_name', 'SKU', 'supplier_price')
    )

    summary = [
        {
            "product_name": item['product_name'],
            "SKU": item['SKU'],
            "supplier_price": float(item['supplier_price']),
        }
        for item in supplier_products
    ]

    return Response(summary)



@api_view(['GET'])
def get_suppliers_by_category(request):
    category_name = request.query_params.get('category')
    if not category_name:
        return Response({"error": "Category parameter is required."}, status=400)

    try:
        category = ProductCategory.objects.get(category_name__iexact=category_name)
    except ProductCategory.DoesNotExist:
        return Response({"supplier_ids": []})

    product_ids = Product.objects.filter(category=category).values_list('id', flat=True)

    supplier_ids = SupplierProduct.objects.filter(product_id__in=product_ids).values_list('supplier_id', flat=True).distinct()

    return Response({"supplier_ids": list(supplier_ids)})



@api_view(['GET'])  
def order_inventory_summary(request):
    warehouse_id = request.query_params.get('warehouse_id')
    if not warehouse_id:
        return Response({"error": "warehouse_id is required"}, status=400)

    product_ids = {p["product_id"] for order in ORDERS for p in order["products"]}

    products = Product.objects.filter(id__in=product_ids).in_bulk()
    product_id_to_name = {pid: prod.product_name for pid, prod in products.items()}

    enriched_orders = [
        {
            "order_id": order["order_id"],
            "products": [
                {
                    "product_name": product_id_to_name.get(p["product_id"], "Unknown Product"),
                    "product_count": p["product_count"]
                } for p in order["products"]
            ]
        } for order in ORDERS
    ]

    inventory_summary_qs = WarehouseInventory.objects.filter(
        warehouse_id=warehouse_id,
        product_id__in=product_ids
    ).values('product_id').annotate(available_count=Sum('quantity'))

    inventory_summary = [
        {
            "product_name": product_id_to_name.get(row["product_id"], "Unknown Product"),
            "available_count": int(row["available_count"])
        } for row in inventory_summary_qs
    ]

    return Response({
        "orders": enriched_orders,
        "inventory": inventory_summary
    })



"""pip install httpx 


import httpx
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from product.models import Product
from warehouse.models import WarehouseInventory

ORDER_SERVICE_URL = "http://order-service/api/v0/orders/warehouse/{warehouse_id}?minimal=True"

@api_view(['GET'])
def order_inventory_summary(request):
    warehouse_id = request.query_params.get('warehouse_id')
    if not warehouse_id:
        return Response({"error": "Missing warehouse_id in query params"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 🔗 Fetch order data from order management service
        response = httpx.get(ORDER_SERVICE_URL.format(warehouse_id=warehouse_id), timeout=5.0)
        response.raise_for_status()
        orders = response.json()
    except httpx.RequestError as exc:
        return Response({"error": f"Request error: {exc}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except httpx.HTTPStatusError as exc:
        return Response({"error": f"Order service error: {exc.response.status_code}"}, status=exc.response.status_code)

    # 🔍 Collect all unique product IDs from fetched orders
    product_ids = {p["product_id"] for order in orders for p in order["products"]}

    # 📦 Fetch product names from DB
    products = Product.objects.in_bulk(product_ids)
    product_id_to_name = {pid: p.product_name for pid, p in products.items()}

    # 🧾 Enrich order data
    enriched_orders = [
        {
            "order_id": order["order_id"],
            "products": [
                {
                    "product_name": product_id_to_name.get(p["product_id"], "Unknown Product"),
                    "product_count": p["product_count"]
                } for p in order["products"]
            ]
        } for order in orders
    ]

    # 📊 Inventory summary only for this warehouse
    inventory_data = WarehouseInventory.objects.filter(
        warehouse_id=warehouse_id,
        product_id__in=product_ids
    ).values('product_id').annotate(available_count=Sum('quantity'))

    inventory_summary = [
        {
            "product_name": product_id_to_name.get(item["product_id"], "Unknown Product"),
            "available_count": int(item["available_count"])
        } for item in inventory_data
    ]

    return Response({
        "orders": enriched_orders,
        "inventory": inventory_summary
    }, status=status.HTTP_200_OK)
"""

@api_view(['POST'])
def handle_order_status(request): #After order is accepted or rejected
    data = request.data

    warehouse_id = data.get("warehouse_id")
    order_id = data.get("order_id")
    status_flag = data.get("status")

    if status_flag == "rejected":
        print(f"Order {order_id} was rejected.")
        return Response({
            "order_id": order_id,
            "message": "Order rejected. No changes made to inventory."
        }, status=status.HTTP_200_OK)

    if status_flag == "accepted":
        try:
            warehouse = Warehouse.objects.get(id=warehouse_id)
        except Warehouse.DoesNotExist:
            return Response({
                "error": f"Warehouse with id {warehouse_id} not found."
            }, status=status.HTTP_404_NOT_FOUND)

        for item in data.get("products", []):
            product_name = item["product_name"]
            product_count = Decimal(item["product_count"])

            try:
                product = Product.objects.get(product_name=product_name)
                inventory = WarehouseInventory.objects.get(
                    warehouse=warehouse,
                    product=product
                )
                if inventory.quantity < product_count:
                    return Response({
                        "error": f"Not enough stock for {product_name}"
                    }, status=status.HTTP_400_BAD_REQUEST)

                inventory.quantity -= product_count
                inventory.save()
            except Product.DoesNotExist:
                return Response({
                    "error": f"Product '{product_name}' not found."
                }, status=status.HTTP_404_NOT_FOUND)
            except WarehouseInventory.DoesNotExist:
                return Response({
                    "error": f"No inventory for product '{product_name}' in warehouse {warehouse_id}."
                }, status=status.HTTP_404_NOT_FOUND)

        status_payload = {
            "status": "Accepted",
            "warehouse_location": {
                "latitude": warehouse.location_x,
                "longitude": warehouse.location_y
            }
        }

        try:
            response = requests.post(
                f"http://localhost:8000/api/v0/orders/{order_id}/status/",
                json=status_payload,
                timeout=5 
            )
            response.raise_for_status() 
        except requests.RequestException as e:
            return Response({
                "error": "Order was accepted and inventory updated, but failed to notify external system.",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "order_id": order_id,
            "message": "Order accepted. Inventory updated and status sent."
        }, status=status.HTTP_200_OK)

    return Response({
        "error": "Invalid status. Must be 'accepted' or 'rejected'."
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def process_order(request):
    order_data = request.data

    warehouse_id = order_data.get('warehouse_id')
    status = order_data.get('status')
    products = order_data.get('products')

    if status == "rejected":
        print("Order rejected")
        return Response({"message": "Order rejected"}, status=200)

    if status != "accepted":
        return Response({"error": "Invalid status"}, status=400)

    with transaction.atomic():
        inventory_updates = []
        product_names = [p['product_name'] for p in products]

        inventory_qs = WarehouseInventory.objects.filter(
            warehouse_id=warehouse_id,
            product__product_name__in=product_names
        ).select_related('product') 

        product_map = {p['product_name']: p['product_count'] for p in products}
        
        for inventory in inventory_qs:
            product_name = inventory.product.product_name
            product_count = product_map.get(product_name)

            if inventory.quantity < product_count:
                return Response({
                    "error": f"Not enough stock for product: {product_name}"
                }, status=400)

            inventory.quantity = F('quantity') - product_count
            inventory_updates.append(inventory)

        WarehouseInventory.objects.bulk_update(inventory_updates, ['quantity'])

    return Response({"message": "Order processed successfully"}, status=200)


@api_view(['POST'])
def add_supplier_product(request):
    data = request.data
    warehouse_id = data.get("warehouse_id")
    supplier_id = data.get("supplier_id")
    product_id = data.get("product_id")
    supplier_price = data.get("supplier_price")

    if not all([warehouse_id, supplier_id, product_id, supplier_price]):
        return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

    ws_exists = WarehouseSupplier.objects.filter(
        warehouse_id=warehouse_id,
        supplier_id=supplier_id
    ).exists()

    if not ws_exists:
        WarehouseSupplier.objects.create(
            warehouse_id=warehouse_id,
            supplier_id=supplier_id
        )

    sp, created = SupplierProduct.objects.get_or_create(
        supplier_id=supplier_id,
        product_id=product_id,
        defaults={
            "supplier_price": Decimal(supplier_price),
            "maximum_capacity": Decimal("0.00"),  # default
            "lead_time_days": 5  # default
        }
    )

    if not created:
        sp.supplier_price = Decimal(supplier_price)
        sp.save()
        message = "SupplierProduct updated with new price."
    else:
        message = "SupplierProduct created."

    return Response({
        "supplier_product_id": sp.id,
        "message": message
    }, status=status.HTTP_200_OK)