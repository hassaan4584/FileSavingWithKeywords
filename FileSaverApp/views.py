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
    # output = ', '.join([doc.document_name for doc in document_list])
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

    searchResults = Document.objects.filter(document_name__icontains=searchText)

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


    addressee = findAddressee(text)
    subject = findSubjectLine(text)



    return render(request, 'FileSaverApp/documentDetail.html', {'document': document,
                                                                'text': document_text,
                                                                'addressee': addressee,
                                                                'subjectLine': subject})



# Helper Functions

def findAddressee(text):
    # find name of the person/team to which the letter is directed to

    addressee = "Unable to find the name of the person this document us addressed to."
    startIndex = text.lower().find("dear ")
    offset = 5
    if startIndex == -1:
        startIndex = text.lower().find("dear")
        offset = 4
    if startIndex != -1 :
        endIndex = text.find(",\n")
        if endIndex == -1:
            endIndex = text.find("\n")

        if endIndex != -1 :
            addressee = "This document is addressed to ";
            addressee += text[startIndex+offset:endIndex].upper();

    return addressee


    # find subject of the document
def findSubjectLine(text):

    subjectLine = "Unable to find subject line in the document"
    possibleSubjectHeadings = ["subject:", "subjectline:", "subject line:"]

    startIndex = -1
    for i in range(0, possibleSubjectHeadings.__len__()):
        startIndex = text.lower().find(possibleSubjectHeadings[i])
        offset = possibleSubjectHeadings[i].__len__()
        if startIndex != -1:
            startIndex += offset
            endIndex = text.find('\n')
            if endIndex > startIndex:
                subjectLine = text[startIndex:endIndex]
                return subjectLine

        startIndex = -1;


    return subjectLine