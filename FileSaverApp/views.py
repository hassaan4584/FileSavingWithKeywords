from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Document
from .models import Keyword

from PIL import Image
import pytesseract
import argparse
import cv2
import os

# Create your views here.


def index(request):
    # return HttpResponse("Hello, You are at start of the Document Management System.")
    return render(request, 'FileSaverApp/tinker/index.html')


def listFiles(request):
    # document = get_object_or_404(Document, pk=document_id)
    # return render(request, 'FileSaverApp/list.html', {'document': document})

    # document_list = Document.objects.order_by('-pub_date')[:5]
    # output = ', '.join([doc.file_name for doc in document_list])
    # return HttpResponse(output)

    documents_list = Document.objects.order_by('-document_name')
    context = {
        'documents_list': documents_list,
    }
    return render(request, 'FileSaverApp/list.html', context)


def documentDetail(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    document_text = document.document_text

    return render(request, 'FileSaverApp/documentDetail.html', {'document': document,
                                                                'text': document_text })


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


def extractText(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    document_text = 'abc'

    # load the example image and convert it to grayscale
    image = cv2.imread('media/' + document.file.__str__())
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    print(text)
    document_text = text
    document.file_text = text
    document.save()
    return render(request, 'FileSaverApp/documentDetail.html', {'document': document,
                                                                'text': document_text })
