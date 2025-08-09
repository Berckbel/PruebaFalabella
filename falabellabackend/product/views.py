from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class ProductView(APIView):

    @swagger_auto_schema(
        operation_summary="List of Products",
        operation_description="Get all products available.",
        responses={
            200: openapi.Response(description="List of products",
            schema=ProductSerializer(many=True))
        }
    )
    def get(self, request, format=None):
        try:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)