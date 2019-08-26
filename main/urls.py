from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'Enigmath'
urlpatterns = [
    url(r'^$', main_view, name='home'),
    url(r'^about/$', about, name='about'),
    url(r'^team/$', team, name='team'),
    url(r'^pricing/$', pricing, name='pricing'),
    url(r'^login/$', login_page, name='login_page'),
    url(r'^sign_up/$', sign_up, name='sign_up'),
    url(r'^api/login/$', login_view, name='login'),
    url(r'^api/update_pswd/$', update_pswd, name='update_pswd'),
    url(r'^api/reset_pswrd/$', reset_pswrd, name='reset_pswrd'),
    url(r'^api/register/$', register_view, name='register'),
    url(r'^about/$', main_view, name='about'),
    url(r'^reset_pswrd_view/$', reset_pswrd_view, name='reset_pswrd_view'),
    url(r'^map/$', map_view, name='map'),
    url(r'^api/change_subject_url/$', ChangeSubject, name='change_subject_url'),    
    url(r'^lesson/$', hislessons, name='hislessons'),
    url(r'^search/$', search, name='search'),
    url(r'^api/map_search/$', map_search, name='map_search'),
    url(r'^api/map_search_show/$', map_search_show, name='map_search_show'),
    url(r'^api/map_filter/$', map_filter, name='map_filter'),
    url(r'^notifications/$', get_notifications, name='get_notifications'),
    url(r'^moderator/$', moderator, name='moderator'),
    url(r'^api/create_school/$', create_school, name='create_school'),
    url(r'^api/make_zaiavka/$', make_zaiavka, name='make_zaiavka'),
    url(r'^api/get_request_land/$', get_request_land, name='get_request_land'),
]