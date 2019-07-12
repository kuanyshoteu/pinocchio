from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'Enigmath'
urlpatterns = [
    url(r'^$', main_view, name='home'),
    url(r'^about/$', main_view, name='about'),
    url(r'^api/login/$', login_view, name='login'),
    url(r'^api/login_social/$', login_social, name='login_social'),
    url(r'^api/register/$', register_view, name='register'),
    url(r'^contacts/$', contacts_view, name='contacts'),
    url(r'^map/$', map_view, name='map'),
    url(r'^api/change_subject_url/$', ChangeSubject, name='change_subject_url'),    
    url(r'^save_zaiavka_url/$', SaveZaiavka, name='save_zaiavka_url'),    
    url(r'^lesson/$', hislessons, name='hislessons'),
    url(r'^search/$', search, name='search'),
    url(r'^api/map_search/$', map_search, name='map_search'),
    url(r'^api/map_search_show/$', map_search_show, name='map_search_show'),
    url(r'^api/map_filter/$', map_filter, name='map_filter'),
    url(r'^notifications/$', get_notifications, name='get_notifications'),
    url(r'^moderator/$', moderator, name='moderator'),
]