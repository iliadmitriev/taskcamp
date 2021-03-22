from django.contrib import admin
from .models import Document


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'uploaded', 'document', 'title']
    readonly_fields = ['id', 'uploaded']
    fields = ['id', 'uploaded', 'document', 'title', 'description']
    search_fields = ['title', 'description']


admin.site.register(Document, DocumentAdmin)
