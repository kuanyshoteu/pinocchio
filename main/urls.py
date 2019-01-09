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
    url(r'^api/city/$', CityAPIToggle.as_view(), name='city_api_url'),
    url(r'^api/filial/$', FilialAPIToggle.as_view(), name='filial_api_url'),
    url(r'^api/subject/$', SubjectAPIToggle.as_view(), name='subject_api_url'),
    url(r'^(?P<slug>[\w-]+)/delete-trener/$', trener_delete, name='delete_trener'),
    url(r'^(?P<slug>[\w-]+)/update-trener/$', trener_update, name='update_trener'),
    url(r'^api/change_subject_url/$', ChangeSubject, name='change_subject_url'),    
    url(r'^save_zaiavka_url/$', SaveZaiavka, name='save_zaiavka_url'),    
]