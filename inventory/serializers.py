from rest_framework import serializers

from .utils import generate_signed_url
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'category_name', 'category_description']


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        fields = ['product_code', 'product_name', 'price', 'quantity', 'category', 'image_url']

    def get_image_url(self, obj):
        return generate_signed_url(obj.product_code,obj.image_url, 5)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['price'] = float(representation['price'])
        return representation
