from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'Enigmath'
urlpatterns = [
    url(r'^$', main_view, name='home'),
    url(r'^about/$', main_view, name='about'),
    url(r'^api/login/$', login_view, name='login'),
    url(r'^api/register/$', register_view, name='register'),
    url(r'^contacts/$', contacts_view, name='contacts'),
    url(r'^map/$', map_view, name='map'),
    url(r'^api/change_subject_url/$', ChangeSubject, name='change_subject_url'),    
    url(r'^save_zaiavka_url/$', SaveZaiavka, name='save_zaiavka_url'),    
    url(r'^lesson/$', hislessons, name='hislessons'),
    url(r'^search/$', search, name='search'),
    url(r'^notifications/$', get_notifications, name='get_notifications'),
]