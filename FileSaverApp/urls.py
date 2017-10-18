from django.conf.urls import url

from . import views

app_name = 'FileSaverApp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^(?P<document_id>[0-9]+)list/$', views.listFiles, name='list'), # http://127.0.0.1:8000/FileSaverApp/1list/
    url(r'^list/$', views.listFiles, name='list'),
    url(r'^search/$', views.searchDocuments, name='search'),
    url(r'^(?P<document_id>[0-9]+)/$', views.documentDetail, name='detail'),

]
