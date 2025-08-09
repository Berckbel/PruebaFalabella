from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from product.models import Product, Category


class ProductViewTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Calzado")

        self.product1 = Product.objects.create(
            name="Sport shoes",
            sku="ZAP001",
            description="Sport shoes to run",
            price=59.99,
            stock=10,
            category=self.category
        )

        self.product2 = Product.objects.create(
            name="leather Boots",
            sku="BOT001",
            description="Mountain leather boots",
            price=120.00,
            stock=5,
            category=self.category
        )

    def test_get_all_products_returns_correct_data(self):
        url = reverse('product_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)

        for product in response.data:
            self.assertIn('id', product)
            self.assertIn('name', product)
            self.assertIn('sku', product)
            self.assertIn('description', product)
            self.assertIn('price', product)
            self.assertIn('stock', product)
            self.assertIn('category', product) 

        product_names = [p['name'] for p in response.data]
        self.assertIn("Sport shoes", product_names)
        self.assertIn("leather Boots", product_names)
