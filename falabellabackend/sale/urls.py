from django.urls import path
from .views import SaleView, getBillsByClient, exportData

urlpatterns = [
    path('', SaleView.as_view(), name='sales_list'),
    path('bills/', getBillsByClient, name='billing_list'),
    path('export-data/<str:doc_type>/<str:doc_number>/', exportData, name='export_data'),
]
