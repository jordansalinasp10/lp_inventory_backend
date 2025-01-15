from django.contrib import admin
from django.urls import path
from inventory.views.products import getProducts

urlpatterns = [
    path('admin/', admin.site.urls),
    path( 'products/', getProducts, name='getProducts'),
]
