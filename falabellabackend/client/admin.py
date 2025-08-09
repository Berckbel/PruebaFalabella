from django.contrib import admin
from django.urls import path
from .models import Client, DocumentType
from .services import export_fidelization

class ClienteAdmin(admin.ModelAdmin):
    change_list_template = "admin/clients_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("export-fidelization/", self.admin_site.admin_view(export_fidelization), name="export_fidelization"),
        ]
        return custom_urls + urls

# Register your models here.
admin.site.register(DocumentType)
admin.site.register(Client, ClienteAdmin)
