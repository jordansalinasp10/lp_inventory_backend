from django.urls import path
from .views import products

urlpatterns = [
    path('products/', products.get_products, name='get_products'),
    path('products/create/', products.create_product, name='create_product'),
    path('products/<str:product_code>/', products.get_product_by_code, name='get_product_by_code'),
    path('products/<str:product_code>/update/', products.update_product, name='update_product'),
    path('products/<str:product_code>/delete/', products.delete_product, name='delete_product'),
]