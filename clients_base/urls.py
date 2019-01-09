from django.conf.urls import url
from django.contrib import admin

from .views import (
    profile_list,
    )

app_name = 'Enigmath'
urlpatterns = [
    url(r'^$', profile_list, name='profile_list'),
]