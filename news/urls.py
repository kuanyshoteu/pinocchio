from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'Enigmath'
urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^api/create_post$', create_post, name='create_post_url'),
    url(r'^(?P<id>\d+)/delete/$', post_delete, name='delete'),
]