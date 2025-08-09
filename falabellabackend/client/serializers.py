from rest_framework import serializers
from .models import Client, DocumentType

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            "id",
            "first_name",
            "last_name",
            "document",
            "document_number",
            "email",
            "phone",
        )

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = (
            "id",
            "name",
        )