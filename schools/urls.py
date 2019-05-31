from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'schools'
urlpatterns = [
    url(r'^crm/$', school_crm, name='crm'),
    url(r'^crm_reg/$', school_crm_reg, name='crm_reg'),
    url(r'^students/$', school_students, name='students'),
    url(r'^info/$', school_info, name='info'),
    url(r'^salaries/$', school_salaries, name='salaries'),
    url(r'^courses/$', school_courses, name='courses'),
    url(r'^rating/$', school_rating, name='rating'),
    url(r'^payments/$', school_payments, name='payments'),
    url(r'^api/edit_card/$', edit_card, name='edit_card_url'),
    url(r'^api/add_card/$', add_card, name='add_card_url'),
    url(r'^api/move_card/$', move_card, name='move_card_url'),
    url(r'^api/save_card_as_user/$', save_card_as_user, name='save_card_as_user'),
    url(r'^api/crm_option_url/$', crm_option, name='crm_option_url'),
    url(r'^api/salary_url/$', save_salary, name='salary_url'),
    url(r'^api/save_job_salary/$', save_job_salary, name='save_job_salary'),
    url(r'^api/delete_card/$', delete_card, name='delete_card_url'),
    url(r'^api/open_card_url/$', open_card, name='open_card_url'),
    url(r'^api/show_free_cards/$', show_free_cards, name='show_free_cards'),
    url(r'^api/get_card_squads/$', get_card_squads, name='get_card_squads'),
    url(r'^(?P<id>\d+)/edit/$', school_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', school_delete, name='delete'),
]