from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from ..models import Product, Category
from ..serializers import ProductSerializer
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def get_product_by_code(request, product_code):
    product = get_object_or_404(Product, product_code=product_code)
    serializer = ProductSerializer(product)
    serializer.data['price'] = float(serializer.data['price'])
    return Response(serializer.data)



@api_view(['POST'])
def create_product(request):
    print("📩 Datos recibidos en el backend:", request.data)

    try:
        # Extraer los datos del request
        product_code = request.data.get('product_code')
        product_name = request.data.get('product_name')
        price = request.data.get('price')
        quantity = request.data.get('quantity')
        category_id = request.data.get('category')
        image_url = request.data.get('image_url', '')  # Asegurar que no sea None

        # Validaciones básicas
        if not all([product_code, product_name, price, quantity, category_id]):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Convertir valores al tipo correcto
        try:
            price = float(price)
            quantity = int(quantity)
            category_id = int(category_id)
        except ValueError:
            return Response({"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar que la categoría existe
        category = get_object_or_404(Category, pk=category_id)

        # Crear el producto directamente con el modelo
        product = Product.objects.create(
            product_code=product_code,
            product_name=product_name,
            price=price,
            quantity=quantity,
            category=category,
            image_url=image_url,
        )

        print("✅ Producto creado con éxito:", product.product_id)

        return Response({
            "message": "Product created successfully",
            "product_id": product.product_id,
            "product_code": product.product_code,
            "product_name": product.product_name,
            "price": product.price,
            "quantity": product.quantity,
            "category": category.category_name,
            "image_url": product.image_url
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(f"❌ Error en backend: {e}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



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