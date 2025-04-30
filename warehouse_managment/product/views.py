from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

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
