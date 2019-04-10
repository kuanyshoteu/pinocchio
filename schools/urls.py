from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'schools'
urlpatterns = [
    url(r'^crm/$', school_crm, name='crm'),
    url(r'^crm_reg/$', school_crm_reg, name='crm_reg'),
    url(r'^students/$', school_students, name='students'),
    url(r'^info/$', school_info, name='info'),
    url(r'^teachers/$', school_teachers, name='teachers'),
    url(r'^courses/$', school_courses, name='courses'),
    url(r'^rating/$', school_rating, name='rating'),
    url(r'^api/edit_card/$', edit_card, name='edit_card_url'),
    url(r'^api/add_card/$', add_card, name='add_card_url'),
    url(r'^api/move_card/$', move_card, name='move_card_url'),
    url(r'^api/save_card_as_user/$', save_card_as_user, name='save_card_as_user'),
    url(r'^api/crm_option_url/$', crm_option, name='crm_option_url'),
    url(r'^(?P<id>\d+)/edit/$', school_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', school_delete, name='delete'),
]