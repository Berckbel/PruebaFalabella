from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from client.models import Client, DocumentType


class ClientAPITest(APITestCase):

    def setUp(self):
        doc_type = DocumentType.objects.create(name="Cédula de ciudadanía")

        self.client1 = Client.objects.create(
            first_name="Juan",
            last_name="Pérez",
            document_type=doc_type,
            document_number="12345678",
            email="juan@example.com",
            phone="3001234567"
        )
        self.client2 = Client.objects.create(
            first_name="María",
            last_name="Gómez",
            document_type=doc_type,
            document_number="87654321",
            email="maria@example.com",
            phone="3017654321"
        )

    def test_get_client_data_returns_all_clients(self):
        url = reverse('get_client_data')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)

        first_client = response.data[0]
        self.assertIn('id', first_client)
        self.assertIn('first_name', first_client)
        self.assertIn('last_name', first_client)
        self.assertIn('email', first_client)
        self.assertIn('phone', first_client)

        first_names = [c['first_name'] for c in response.data]
        self.assertIn("Juan", first_names)
        self.assertIn("María", first_names)


class DocumentTypeAPITest(APITestCase):

    def setUp(self):
        self.type1 = DocumentType.objects.create(name="Cedula")
        self.type2 = DocumentType.objects.create(name="Pasaporte")

    def test_get_document_types_returns_all_types(self):
        url = reverse('get_document_types')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        first_type = response.data[0]
        self.assertIn('id', first_type)
        self.assertIn('name', first_type)

        names = [t['name'] for t in response.data]
        self.assertIn("Cedula", names)
        self.assertIn("Pasaporte", names)
