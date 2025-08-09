from django.urls import path
from .views import getDocumentTypes, getClientData

urlpatterns = [
    path('client-data', getClientData, name='get_client_data'),
    path('document-types/', getDocumentTypes, name='get_document_types'),
]
