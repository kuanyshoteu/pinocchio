from django.conf.urls import url
from django.contrib import admin
from .views import *

app_name = 'library'
urlpatterns = [
    url(r'^api/create_lesson/$', create_lesson, name='create_lesson'),
    url(r'^api/get_library/$', get_library, name = 'get_library'),
    url(r'^api/show_lesson/$', show_lesson, name = 'show_lesson'),
    url(r'^api/get_folder_files/$', get_folder_files, name = 'get_folder_files'),
    url(r'^api/create_folder/$', create_folder, name = 'create_folder_url'),
    url(r'^api/rename_folder/$', rename_folder, name = 'rename_folder'),
    url(r'^api/delete_folder_url/$', delete_folder, name = 'delete_folder_url'),
    url(r'^api/file_action_url/$', file_action, name = 'file_action_url'),
    url(r'^api/paste_to_folder/$', paste, name = 'paste_to_folder'),
    url(r'^api/save_task/$', save_task, name = 'save_task'),
    url(r'^api/get_all_tasks/$', get_all_tasks, name = 'get_all_tasks'),
    url(r'^api/delete_subtheme/$', delete_subtheme, name = 'delete_subtheme'),
    url(r'^api/add_task_to_subtheme/$', add_task_to_subtheme, name = 'add_task_to_subtheme'),
    url(r'^api/save_paper_title/$', save_paper_title, name = 'save_paper_title'),
    url(r'^api/move_subtheme_url/$', move_subtheme, name = 'move_subtheme_url'),
    url(r'^api/move_paper/$', move_paper, name = 'move_paper'),
    url(r'^folder/(?P<folder_id>\d+)/$', folder_details, name='get_absolute_url'),
    url(r'^(?P<school_id>\d+)/$', school_library, name='get_school_library'),
    url(r'^$', library, name='main'),
]