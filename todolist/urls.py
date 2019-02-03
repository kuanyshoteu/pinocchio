from django.conf.urls import url

from .views import *

app_name = 'todolist'
urlpatterns = [
    url(r'^new-card/$', new_card, name = 'new_card'),
    url(r'^delete-card/$', delete_card, name = 'delete_card'),
    url(r'^delete-column/$', delete_column, name = 'delete_column'),
    url(r'^delete-board/$', delete_board, name = 'delete_board'),
    url(r'^new-column/$', new_column, name = 'new_column'),
    url(r'^new-board/$', new_board, name = 'new_board'),
    url(r'^(?P<card_id>\d+)/(?P<card_slug>[\w-]+)/$', view_card, name='card'),
    url(r'^drop/$', drop),
    url(r'^api/change_text_url/$', ChangeCardText, name='change_card_text_url'),    
    url(r'^api/add_user_url/$', AddUser, name='add_user_url'),    
    url(r'^api/add_metka_url/$', AddMetka, name='add_metka_url'),    
    url(r'^$', index, name = 'main'),
]
