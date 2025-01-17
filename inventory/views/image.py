from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from inventory.models import Product
from inventory.utils import upload_image_to_azure, generate_signed_url

@csrf_exempt
@api_view(['POST'])
def upload_product_image(request, sku):
    product = get_object_or_404(Product, product_code=sku)
    image_file = request.FILES.get('image') # Verifica si se ha enviado un archivo
    if not image_file:
        return Response({"error": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST)

    image_url = upload_image_to_azure(image_file, sku)
    print(f"IMAGEN URL {image_url}")
    try:
        with transaction.atomic():
            product.image_url = image_url
            product.save()
    except Exception as e:
        print(f"Error al guardar el producto: {e}")
    return Response({"message": "Image uploaded successfully.", "image_url": image_url}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_signed_product_image(request, sku):
    product = get_object_or_404(Product, product_code=sku)

    if not product.image_url:
        return Response({"error": "No image found for this product."}, status=status.HTTP_404_NOT_FOUND)

    try:
        # Genera una URL firmada para el archivo
        signed_url = generate_signed_url(sku)

        return Response({"signed_image_url": signed_url}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

