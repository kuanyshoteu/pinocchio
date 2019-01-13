from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'schools'
urlpatterns = [
    url(r'^$', school_detail, name='detail'),
    url(r'^rating/$', school_rating, name='rating'),
    url(r'^manager/$', manager_page, name='manager_page'),
    url(r'^api/change_curator_url/$', change_curator, name='change_curator_url'),
    url(r'^(?P<id>\d+)/edit/$', school_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', school_delete, name='delete'),
]