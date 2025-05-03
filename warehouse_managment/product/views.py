from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView  # ✅ Add this
from .models import ProductCategory, Product, SupplierProduct
from .serializers import ProductCategorySerializer, ProductSerializer, SupplierProductSerializer
from rest_framework import viewsets


@api_view(['GET'])
def root(request):
    """
    Root endpoint for the product management system.
    """
    return Response({"message": "Welcome to the Product Management System!"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def product_list(request):
    """
    List all products.
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    """
    Retrieve a product by ID.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(product)
    return Response(serializer.data)

class UpdateSupplierProductView(APIView):
    def post(self, request):
        supplier_id = request.data.get('supplier_id')
        product_id = request.data.get('product_id')
        new_capacity = request.data.get('maximum_capacity')

        try:
            sp = SupplierProduct.objects.get(supplier_id=supplier_id, product_id=product_id)
            sp.maximum_capacity = new_capacity
            sp.save()
            return Response({"status": "success"})
        except SupplierProduct.DoesNotExist:
            return Response({"error": "SupplierProduct not found"}, status=404)

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SupplierProductViewSet(viewsets.ModelViewSet):
    queryset = SupplierProduct.objects.all()
    serializer_class = SupplierProductSerializer
