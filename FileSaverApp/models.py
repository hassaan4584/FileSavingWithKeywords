from django.db import models

# Create your models here.

class Document(models.Model):
    document_name = models.CharField(max_length=200)
    document_type = models.CharField(max_length=100, default='General')
    file = models.FileField(upload_to="pdfs/")
    document_text = models.CharField(max_length=2000, default='')

    def __str__(self):
        return self.file_name


class Keyword(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=200)

    def __str__(self):
        return self.keyword


