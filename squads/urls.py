from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'Enigmath'
urlpatterns = [
    url(r'^$', squad_list, name='list'),
    url(r'^create/$', squad_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', squad_detail, name='detail'),
    url(r'^api/calendar_url/$', calendar_change, name='calendar_url'),
    url(r'^api/add_paper_url/$', add_paper, name='add_paper_url'),
    url(r'^api/change_curator_url/$', change_curator, name='change_curator_url'),
    url(r'^api/set_time_url/$', set_time, name='set_time_url'),
    url(r'^api/change_start_url/$', change_start, name='change_start_url'),
    url(r'^api/change_end_url/$', change_end, name='change_end_url'),
    url(r'^api/add_student_url/$', add_student, name='add_student_url'),
    url(r'^(?P<slug>[\w-]+)/edit/$', squad_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/videos/$', squad_videos, name='videos_url'),
    url(r'^(?P<slug>[\w-]+)/lessons/$', squad_lessons, name='lessons_url'),
    url(r'^(?P<slug>[\w-]+)/delete/$', squad_delete, name='delete'),
]