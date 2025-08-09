from django.db import models
from product.models import Product
from client.models import Client

# Create your models here.
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    product_price = models.DecimalField(max_digits=20, decimal_places=2)
    product_quantity = models.IntegerField()

    sale_total = models.DecimalField(max_digits=20, decimal_places=2)
    sale_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Sale {self.id} - Product: {self.product.name}"
    
class Billing(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    sales = models.ManyToManyField(Sale, related_name="sales")
    billing_total = models.DecimalField(max_digits=20, decimal_places=2)
    billing_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Billing {self.id} - Total: {self.billing_total} - Date: {self.billing_date}"