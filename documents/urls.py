from django.conf.urls import url
from django.contrib import admin
from .views import *

app_name = 'Enigmath'
urlpatterns = [
    url(r'^api/change_name_url/$', change_name, name = 'change_name_url'),
    url(r'^api/delete_folder_url/$', delete_folder, name = 'delete_folder_url'),
    url(r'^api/file_action_url/$', file_action, name = 'file_action_url'),
    url(r'^api/paste_object_url/$', paste, name = 'paste_object_url'),
    url(r'^api/create_docfolder/$', create_docfolder, name = 'create_docfolder_url'),
    url(r'^(?P<folder_id>\d+)/$', folder_details, name='get_absolute_url'),
    url(r'^$', documents, name='main'),
]