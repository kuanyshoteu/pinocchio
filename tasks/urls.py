from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'Enigmath'
urlpatterns = [
    url(r'^delete/$', task_delete, name='delete'),
    url(r'^api/change_answer_url/$', ChangeAnswer, name='change_answer_url'),
    url(r'^api/change_text_url/$', ChangeText, name='change_text_url'),
]