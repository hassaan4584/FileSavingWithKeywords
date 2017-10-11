from django.db import models

# Create your models here.

class Document(models.Model):
    file_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    file = models.FileField(upload_to="pdfs/")

    def __str__(self):
        return self.file_name


class Keywords(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.keyword


