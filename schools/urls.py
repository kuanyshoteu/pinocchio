from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'schools'
urlpatterns = [
    url(r'^$', school_detail, name='detail'),
    url(r'^rating/$', school_rating, name='rating'),
    url(r'^manager/$', manager_page, name='manager_page'),
    url(r'^api/register_to_school/$', register_to_school, name='register_to_school'),
    url(r'^(?P<id>\d+)/edit/$', school_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', school_delete, name='delete'),
]