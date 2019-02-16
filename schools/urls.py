from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'schools'
urlpatterns = [
    url(r'^crm/$', school_crm, name='crm'),
    url(r'^requests/$', school_requests, name='requests'),
    url(r'^recalls/$', school_recalls, name='recalls'),
    url(r'^info/$', school_info, name='info'),
    url(r'^teachers/$', school_teachers, name='teachers'),
    url(r'^courses/$', school_courses, name='courses'),
    url(r'^rating/$', school_rating, name='rating'),
    url(r'^api/register_to_school/$', register_to_school, name='register_to_school'),
    url(r'^(?P<id>\d+)/edit/$', school_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', school_delete, name='delete'),
]