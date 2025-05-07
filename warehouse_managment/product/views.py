from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ProductCategory, Product, SupplierProduct
from .serializers import ProductCategorySerializer, ProductSerializer, SupplierProductSerializer
from django.db.models import Sum
from warehouse.models import WarehouseInventory

@api_view(['GET'])
def root(request):

    return Response({"message": "Welcome to the Product Management System!"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def product_list(request):

    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):

    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def category_list(request):

    categories = ProductCategory.objects.all()
    serializer = ProductCategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def category_detail(request, pk):

    try:
        category = ProductCategory.objects.get(pk=pk)
    except ProductCategory.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductCategorySerializer(category)
    return Response(serializer.data)


@api_view(['GET'])
def supplier_product_list(request):

    sp = SupplierProduct.objects.all()
    serializer = SupplierProductSerializer(sp, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def update_supplier_product(request):

    supplier_id = request.query_params.get('supplier_id')
    product_id = request.query_params.get('product_id')
    new_capacity = request.query_params.get('maximum_capacity')

    if not all([supplier_id, product_id, new_capacity]):
        return Response({"error": "Missing fields"}, status=400)

    try:
        sp = SupplierProduct.objects.get(supplier_id=supplier_id, product_id=product_id)
        sp.maximum_capacity = new_capacity
        sp.save()
        return Response({"status": "success"}, status=200)
    except SupplierProduct.DoesNotExist:
        return Response({"error": "SupplierProduct not found"}, status=404)

@api_view(['GET'])
def product_stock_summary(request, sku_code):
    # Optional: Validate SKU format if needed
    if not sku_code.startswith("SKU") or not sku_code[3:].isdigit():
        return Response({'error': 'Invalid SKU format'}, status=400)

    try:
        product = Product.objects.get(product_SKU=sku_code)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    total_stock = WarehouseInventory.objects.filter(product=product).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    return Response({
        "product_name": product.product_name,
        "product_SKU": product.product_SKU,
        "current_stock": float(total_stock)
    }, status=status.HTTP_200_OK)
