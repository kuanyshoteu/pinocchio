from django.conf.urls import url
from django.contrib import admin

from .views import *

app_name = 'Bilimtap'
urlpatterns = [
    url(r'^new_post$', new_post, name='new_post'),
    url(r'^api/save_post$', save_post, name='save_post'),
    url(r'^api/get_posts$', get_posts, name='get_posts'),
    url(r'^sc(?P<school_id>\d+)/$', post_list, name='get_school_posts'),
    url(r'^(?P<slug>[\w-]+)$', post_detail, name='detail'),
    url(r'^post_edit/(?P<slug>[\w-]+)$', post_edit, name='post_edit'),
    url(r'^post_delete/(?P<slug>[\w-]+)$', post_delete, name='post_delete'),
    url(r'^api/post_new_comment$', post_new_comment, name='post_new_comment'),
    url(r'^api/post_like_object$', post_like_object, name='post_like_object'),
    url(r'^api/get_post$', get_post, name='get_post'),
    url(r'^api/get_comments$', get_comments, name='get_comments'),
]