from django.http import JsonResponse

from inventory.models import Product


def getProducts(request):
    if request.method == "GET":
        products = Product.objects.all()
        return JsonResponse(list(products.values()), safe=False)