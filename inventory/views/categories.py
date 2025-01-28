from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from ..models import Category
from ..serializers import CategorySerializer
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_category_by_id(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    serializer = CategorySerializer(category)
    return Response(serializer.data,status=status.HTTP_200_OK)
