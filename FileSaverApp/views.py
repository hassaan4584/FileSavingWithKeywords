from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Document
from .models import Keyword

# Create your views here.


def index(request):
    return HttpResponse("Hello, You are at start of the Document Management System.")


def listFiles(request):
    # document = get_object_or_404(Document, pk=document_id)
    # return render(request, 'FileSaverApp/list.html', {'document': document})

    # document_list = Document.objects.order_by('-pub_date')[:5]
    # output = ', '.join([doc.file_name for doc in document_list])
    # return HttpResponse(output)

    documents_list = Document.objects.order_by('-file_name')[:5]
    context = {
        'documents_list': documents_list,
    }
    return render(request, 'FileSaverApp/list.html', context)


def documentDetail(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    return render(request, 'FileSaverApp/documentDetail.html', {'document': document})


def searchDocuments(request):

    searchText = request.GET.get('q')
    if searchText is None:
        return render(request, 'FileSaverApp/search.html')

    searchResults = Document.objects.filter(file_name__icontains=searchText)

    searchList = list(searchResults)

    keywordSearchResults = Keyword.objects.filter(keyword__icontains=searchText)
    for key in keywordSearchResults:
        if key.document not in searchResults:
            searchList.append(key.document)



    return render(request, 'FileSaverApp/search.html', {'documents_list':searchList})

