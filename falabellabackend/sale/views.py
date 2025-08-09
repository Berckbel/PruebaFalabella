from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Sale, Billing
from .serializers import SaleSerializer, BillSerializer

import pandas as pd
import io
from django.http import HttpResponse
from .models import Billing

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class SaleView(APIView):

    @swagger_auto_schema(
        operation_summary="List of Sales",
        operation_description="Get all sales available.",
        responses={
            200: openapi.Response(description="List of sales",
            schema=SaleSerializer(many=True))
        }
    )
    def get(self, request, format=None):
        try:
            sales = Sale.objects.all()
            serializer = SaleSerializer(sales, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema(
    method='get',
    operation_description="Get all billing data by client filtered.",
    responses={200: BillSerializer(many=True)},
    manual_parameters=[
        openapi.Parameter("doc_type", openapi.IN_QUERY, description="Document type", type=openapi.TYPE_STRING),
        openapi.Parameter("doc_number", openapi.IN_QUERY, description="Document number", type=openapi.TYPE_STRING),
    ]
)
@api_view(['GET'])
def getBillsByClient(request):
    doc_type = request.query_params.get("doc_type")
    doc_number = request.query_params.get("doc_number")
    try:
        bills = Billing.objects.filter(client__document_number=doc_number, client__document_type=doc_type)
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def exportData(request, doc_type, doc_number):
    try:
        bills = Billing.objects.filter(
            client__document_number=doc_number,
            client__document_type=doc_type
        ).prefetch_related("sales", "sales__product")
        
        if not bills.exists():
            return HttpResponse("No se encontraron facturas", status=404)

        data = []
        for bill in bills:
            for sale in bill.sales.all():
                data.append({
                    "Bill ID": bill.id,
                    "Date": bill.billing_date,
                    "Client": f"{bill.client.first_name} {bill.client.last_name}",
                    "Product": sale.product.name,
                    "Unit Price": sale.product_price,
                    "Quantity": sale.product_quantity,
                    "Total Sale": sale.sale_total
                })

        df = pd.DataFrame(data)

        buffer = io.StringIO()
        df.to_csv(buffer, index=False, encoding="utf-8-sig")
        buffer.seek(0)

        response = HttpResponse(buffer.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="facturas_{doc_number}.csv"'
        return response

    except Exception as e:
        return HttpResponse(f"Error interno: {str(e)}", status=500)