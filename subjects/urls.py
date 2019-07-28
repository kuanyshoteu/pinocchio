from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'Enigmath'
urlpatterns = [
    url(r'^$', subject_list, name='list'),
    url(r'^create/$', subject_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', subject_detail, name='detail'),
    url(r'^api/add_paper_url/$', add_paper, name='add_paper_url'),
    url(r'^api/remove_lesson/$', remove_lesson, name='remove_lesson'),
    url(r'^api/change_category/(?P<id>\d+)/$', change_category, name='change_category'),
    url(r'^api/change_age/(?P<id>\d+)/$', change_age, name='change_age'),
    url(r'^(?P<slug>[\w-]+)/edit/$', subject_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', subject_delete, name='delete'),
]