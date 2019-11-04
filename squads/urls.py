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
    url(r'^api/add_student_url/$', add_student, name='add_student_url'),
    url(r'^api/change_office/(?P<id>\d+)/$', change_office, name='change_office'),
    url(r'^(?P<slug>[\w-]+)/edit/$', squad_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', squad_delete, name='delete'),

    url(r'^api/schedule/(?P<id>\d+)/$', squad_schedule, name='squad_schedule_url'),
    url(r'^api/subject_list/(?P<id>\d+)/$', subject_list, name='subject_list'),
    url(r'^api/add_subject_url/$', add_subject, name='add_subject_url'),
    url(r'^api/delete_subject_url/$', delete_subject, name='delete_subject_url'),
    url(r'^api/change_schedule_url/(?P<id>\d+)/$', change_schedule, name='change_schedule_url'),
    url(r'^api/delete_lesson_url/(?P<id>\d+)/$', delete_lesson, name='delete_lesson_url'),
    url(r'^api/change_lecture_cabinet/$', change_lecture_cabinet, name='change_lecture_cabinet'),    
    url(r'^api/get_page_students/(?P<id>\d+)/$', get_page_students, name='get_page_students'),    
    url(r'^api/hint_students_group/(?P<id>\d+)/$', hint_students_group, name='hint_students_group'),    
    url(r'^api/const_create_lectures/(?P<id>\d+)/$', const_create_lectures, name='const_create_lectures'),

    url(r'^api/update_cards_money/$', update_cards_money, name='update_cards_money'),
    url(r'^api/get_student_discounts/$', get_student_discounts, name='get_student_discounts'),
    url(r'^api/set_student_discounts/$', set_student_discounts, name='set_student_discounts'),
]