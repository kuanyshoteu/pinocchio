from django.conf.urls import url
from django.contrib import admin

from .views import *
from django.contrib.auth.models import User

app_name = 'accounts'
urlpatterns = [
    url(r'^api/change/$', ChangeTimeAPIToggle.as_view(), name='change-api-toggle'),
    url(r'^api/(?P<id>[\w-]+)/delete/$', DeleteZaiavkaAPIToggle.as_view(), name='deletezaiavka-api-toggle'),
    url(r'^api/(?P<id>[\w-]+)/delete2/$', DeleteFollowAPIToggle.as_view(), name='deletefollow-api-toggle'),
    url(r'^change_url/$', change_profile, name='change_url'),
    url(r'^test_url/$', test_account, name='test_url'),
    url(r'^api/change_att_url/$', ChangeAttendance, name='change_att_url'),
    url(r'^api/miss_lecture/$', miss_lecture, name='miss_lecture_url'),
    url(r'^api/present_url/$', att_present, name='present_url'),
    url(r'^api/tell_about_corruption/$', tell_about_corruption, name='tell_about_corruption'),
    url(r'^api/squad_attendance/$', squad_attendance, name='squad_attendance'),
    url(r'^api/subject_attendance/$', subject_attendance, name='subject_attendance'),
    url(r'^api/more_attendance/$', more_attendance, name='more_attendance'),
    url(r'^api/more_attendance_student/$', more_attendance_student, name='more_attendance_student'),
    url(r'^(?P<user>[\w-]+)/$', account_view, name='profile'),
]