from django.db import models

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)  # Clave primaria personalizada
    category_name = models.CharField(max_length=100, verbose_name="Category Name")
    category_description = models.TextField(max_length=255, blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "CATEGORY"
        managed = False
    def _str_(self):
        return self.category_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)  # Clave primaria personalizada
    product_code = models.CharField(max_length=50, unique=True, verbose_name="Product Code")
    product_name = models.CharField(max_length=100, verbose_name="Product Name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name="Category"
    )
    image_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="Image URL")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "PRODUCT"
        managed = False
    def _str_(self):
        return f"{self.product_name} ({self.product_code})"
