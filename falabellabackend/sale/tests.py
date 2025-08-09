from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from product.models import Product, Category
from client.models import Client, DocumentType
from sale.models import Sale, Billing


class SaleAndBillingAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            sku="LPT123",
            description="High performance laptop",
            price=1500.00,
            stock=5,
            category=self.category
        )
        self.doc_type = DocumentType.objects.create(name="Passport")
        self.client_obj = Client.objects.create(
            first_name="John",
            last_name="Doe",
            document_type=self.doc_type,
            document_number="123456",
            email="john@example.com",
            phone="555-1234"
        )

        self.sale = Sale.objects.create(
            product=self.product,
            product_price=1500.00,
            product_quantity=2,
            sale_total=3000.00
        )

        self.billing = Billing.objects.create(
            client=self.client_obj,
            billing_total=3000.00
        )
        self.billing.sales.add(self.sale)

    def test_get_all_sales(self):
        url = reverse("sales_list")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.sale.product.id)

    def test_get_bills_by_client_success(self):
        url = reverse("billing_list")
        response = self.client.get(url, {
            "doc_type": str(self.doc_type.id),
            "doc_number": "123456"
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(float(response.data[0]["billing_total"]), float(self.billing.billing_total))

    def test_get_bills_by_client_no_results(self):
        url = reverse("billing_list")
        response = self.client.get(url, {
            "doc_type": str(self.doc_type.id),
            "doc_number": "000000"
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
