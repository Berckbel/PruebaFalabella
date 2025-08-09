from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Client, DocumentType
from .serializers import DocumentTypeSerializer
from .serializers import ClientSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='get',
    operation_description="Get All Clients.",
    responses={200: ClientSerializer(many=True)},
)
@api_view(['GET'])
def getClientData(request):
    try:
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@swagger_auto_schema(
    method='get',
    operation_description="Get All Document Types.",
    responses={200: DocumentTypeSerializer(many=True)},
)
@api_view(['GET'])
def getDocumentTypes(request):
    try:
        types = DocumentType.objects.all()
        serializer = DocumentTypeSerializer(types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
