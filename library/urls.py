from django.conf.urls import url
from django.contrib import admin
from .views import *

app_name = 'library'
urlpatterns = [
    url(r'^api/create_lesson/$', create_lesson, name='create_lesson'),
    url(r'^api/get_library/$', get_library, name = 'get_library'),
    url(r'^api/get_folder_files/$', get_folder_files, name = 'get_folder_files'),
    url(r'^api/create_folder/$', create_folder, name = 'create_folder_url'),
    url(r'^api/rename_folder/$', rename_folder, name = 'rename_folder'),
    url(r'^api/delete_folder_url/$', delete_folder, name = 'delete_folder_url'),
    url(r'^api/file_action_url/$', file_action, name = 'file_action_url'),
    url(r'^api/paste_object_url/$', paste, name = 'paste_object_url'),
    url(r'^folder/(?P<folder_id>\d+)/$', folder_details, name='get_absolute_url'),
    url(r'^(?P<school_id>\d+)/$', school_library, name='get_school_library'),
    url(r'^$', library, name='main'),
]