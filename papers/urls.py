from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'papers'
urlpatterns = [
    url(r'^create_course/$', course_create, name='create_course_url'),
    url(r'^api/addgroup/$', AddGroup, name='add-group-toggle'),
    url(r'^api/change_name_url/$', rename_lesson, name = 'change_name_url'),
    url(r'^api/delete_paper_url/$', delete_paper, name = 'delete_paper_url'),
    url(r'^api/delete_lesson_url/$', delete_lesson, name = 'delete_lesson_url'),
    url(r'^api/new_task_url/$', NewTask, name='new_task_url'),
    url(r'^api/add_task_url/$', AddTask, name='add_task_url'),
    url(r'^api/add_subtheme_url/$', AddSubtheme, name='add_subtheme_url'),
    url(r'^api/add_paper_url/$', AddPaper, name='add_paper_url'),
    url(r'^api/add_lesson_url/$', add_lesson, name='add_lesson_url'),
    url(r'^api/new_comment/$', new_comment, name='new_comment_url'),
    url(r'^api/comment_like/$', like_comment, name='like_url'),
    url(r'^api/comment_dislike/$', dislike_comment, name='dislike_url'),
    url(r'^api/estimate_lesson/$', estimate_lesson, name='estimate_lesson_url'),
    url(r'^lesson(?P<lesson_id>\d+)/$', lesson_details, name='lesson_absolute_url'),
    url(r'^estimate_lesson(?P<lesson_id>\d+)/$', estimate_lesson_page, name='estimate_lesson_page'),
    url(r'^(?P<paper_id>\d+)/$', paper_details, name='paper_absolute_url'),
    url(r'^course(?P<course_id>\d+)/$', course_details, name='course_absolute_url'),
    url(r'^course_info/(?P<course_id>\d+)/$', course_seller, name='course_seller_url'),
    url(r'^course_update(?P<course_id>\d+)/$', course_update, name='course_update_url'),
    url(r'^api/delete_course_url/$', delete_course, name = 'delete_course_url'),
    url(r'^api/check_paper_url/$', check_paper, name = 'check_paper_url'),
    url(r'^api/pay_for_course/$', pay_for_course, name = 'pay_for_course'),
]