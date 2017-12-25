from django.db import models

# Create your models here.
def get_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/pdfs/<document_type>/<filename>
    return 'pdfs/{0}/{1}'.format(instance.document_type, filename)

class Document(models.Model):
    document_name = models.CharField(max_length=200)
    document_type = models.CharField(max_length=100, default='General')
    file = models.FileField(upload_to=get_directory_path)
    document_text = models.CharField(max_length=2000, default='')

    def __str__(self):
        return self.document_name



class Keyword(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=200)

    def __str__(self):
        return self.keyword


