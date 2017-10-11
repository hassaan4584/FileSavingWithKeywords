from django.conf.urls import url

from . import views

app_name = 'FileSaverApp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<document_id>[0-9]+)list/$', views.listFiles, name='list'),
    url(r'^a$', views.index, name='index'),

]