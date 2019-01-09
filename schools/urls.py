from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'Enigmath'
urlpatterns = [
    url(r'^$', school_list, name='list'),
    url(r'^create/$', school_create, name='create'),
    url(r'^(?P<id>\d+)/$', school_detail, name='detail'),
    url(r'^api/change_curator_url/$', change_curator, name='change_curator_url'),
    url(r'^(?P<id>\d+)/edit/$', school_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', school_delete, name='delete'),
]