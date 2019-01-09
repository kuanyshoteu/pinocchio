from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'Enigmath'
urlpatterns = [
    url(r'^$', subject_list, name='list'),
    url(r'^create/$', subject_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', subject_detail, name='detail'),
    url(r'^api/change_schedule_url/(?P<id>\d+)/$', change_schedule, name='change_schedule_url'),
    url(r'^api/delete_squad_url/$', delete_squad, name='delete_squad_url'),
    url(r'^api/add_paper_url/$', add_paper, name='add_paper_url'),
    url(r'^api/add_squad_url/$', add_squad, name='add_squad_url'),
    url(r'^api/change_teacher_url/$', change_teacher, name='change_teacher_url'),
    url(r'^api/change_start_url/$', change_start, name='change_start_url'),
    url(r'^api/change_end_url/$', change_end, name='change_end_url'),
    url(r'^(?P<slug>[\w-]+)/edit/$', subject_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/videos/$', subject_videos, name='videos_url'),
    url(r'^(?P<slug>[\w-]+)/lessons/$', subject_lessons, name='lessons_url'),
    url(r'^(?P<slug>[\w-]+)/delete/$', subject_delete, name='delete'),
    url(r'^api/schedule/(?P<id>\d+)/$', subject_schedule, name='subject_schedule_url'),
    url(r'^api/squad_list/(?P<id>\d+)/$', squad_list, name='squad_list'),
]