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
    url(r'^api/change_filter_option/(?P<id>\d+)/$', change_filter_option, name='change_filter_option'),
    url(r'^api/change_level/(?P<id>\d+)/$', change_level, name='change_level'),
    url(r'^api/change_age/(?P<id>\d+)/$', change_age, name='change_age'),
    url(r'^(?P<slug>[\w-]+)/edit/$', subject_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', subject_delete, name='delete'),
    url(r'^api/searching_subjects/$', searching_subjects, name='searching_subjects'),
    url(r'^api/make_public/$', make_public, name='make_public'),
    url(r'^api/make_public_cost/$', make_public_cost, name='make_public_cost'),
]