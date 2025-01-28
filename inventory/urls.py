from django.urls import path
from unicodedata import category

from .views import products, image, categories

urlpatterns = [
    path('products/', products.get_products, name='get_products'),
    path('products/create/', products.create_product, name='create_product'),
    path('products/<str:product_code>/', products.get_product_by_code, name='get_product_by_code'),
    path('products/<str:product_code>/update/', products.update_product, name='update_product'),
    path('products/<str:product_code>/delete/', products.delete_product, name='delete_product'),

    path('image/update/<str:sku>', image.upload_product_image, name='upload-product-image'),
    path('image/<str:sku>', image.get_signed_product_image, name='get_product_image'),

    path('categories/', categories.get_categories, name='get_categories'),
    path('categories/<str:category_id>/',categories.get_category_by_id, name = 'get_categories')

]