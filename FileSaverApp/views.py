from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Document

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def listFiles(request, document_id):
    # document = get_object_or_404(Document, pk=document_id)
    # return render(request, 'FileSaverApp/list.html', {'document': document})

    # document_list = Document.objects.order_by('-pub_date')[:5]
    # output = ', '.join([doc.file_name for doc in document_list])
    # return HttpResponse(output)

    documents_list = Document.objects.order_by('-pub_date')[:5]
    context = {
        'documents_list': documents_list,
    }
    return render(request, 'FileSaverApp/list.html', context)


def documentDetail(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    return render(request, 'FileSaverApp/documentDetail.html', {'document': document})