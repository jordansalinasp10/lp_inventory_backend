from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from ..models import Product
from ..serializers import ProductSerializer
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    for product in serializer.data:
        product['price'] = float(product['price'])
    return Response(serializer.data)


@api_view(['GET'])
def get_product_by_code(request, product_code):
    # Utilizamos get_object_or_404 para manejar automáticamente el error 404
    product = get_object_or_404(Product, product_code=product_code)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['POST'])
@csrf_exempt
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['PUT'])
def update_product(request, product_code):
    try:
        product = Product.objects.get(product_code=product_code)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_product(request, product_code):
    try:
        product = Product.objects.get(product_code=product_code)
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)