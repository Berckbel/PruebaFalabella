from rest_framework import serializers
from .models import Sale, Billing
from client.serializers import ClientSerializer
from product.serializers import ProductSerializer

class SaleSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = (
            "id",
            "product",
            "product_price",
            "product_quantity",
            "sale_total",
            "sale_date",
        )

class BillSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    sales = SaleSerializer(many=True, read_only=True)

    class Meta:
        model = Billing
        fields = (
            "id",
            "client",
            "sales",
            "billing_total",
            "billing_date",
        )
