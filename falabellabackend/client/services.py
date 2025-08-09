from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from sale.models import Billing
import pandas as pd
import io
from django.http import HttpResponse

def client_fidelization():
    today = timezone.now().date()
    one_month_ago = today - timedelta(days=30)

    clientes = (
        Billing.objects
        .filter(billing_date__gte=one_month_ago)
        .values("client__id", "client__first_name", "client__last_name", "client__document_number")
        .annotate(billing_total=Sum("billing_total"))
        .filter(billing_total__gt=5000000)
        .order_by("-billing_total")
    )

    return list(clientes)


def export_fidelization(request):
    data = client_fidelization()
    df = pd.DataFrame(
        data,
    )

    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, engine="openpyxl", header=["Client id", "First name", "Last name", "Document number", "Billing total"])
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="clients_fidelization.xlsx"'
    return response
