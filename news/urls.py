from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'Enigmath'
urlpatterns = [
    url(r'^api/create_post$', create_post, name='create_post_url'),
    url(r'^delete/$', post_delete, name='delete'),
    url(r'^(?P<school_id>\d+)/$', post_list, name='get_school_posts'),
    url(r'^$', news, name='list'),
]