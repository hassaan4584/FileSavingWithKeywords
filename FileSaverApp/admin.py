from django.contrib import admin

from .models import Document, Keyword, DocumentCategory

# Register your models here.

admin.site.register(Document)
admin.site.register(Keyword)
admin.site.register(DocumentCategory)


