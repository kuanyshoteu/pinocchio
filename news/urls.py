from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'Bilimtap'
urlpatterns = [
    url(r'^new_post$', new_post, name='new_post'),
    url(r'^api/save_post$', save_post, name='save_post'),
    url(r'^api/post_add_part$', post_add_part, name='post_add_part'),
    url(r'^api/get_posts$', get_posts, name='get_posts'),
    url(r'^sc(?P<school_id>\d+)/$', post_list, name='get_school_posts'),
    url(r'^(?P<slug>[\w-]+)$', post_detail, name='detail'),
    url(r'^post_edit/(?P<slug>[\w-]+)$', post_edit, name='post_edit'),
    url(r'^api/post_delete_part$', post_delete_part, name='post_delete_part'),
]