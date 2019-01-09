from django.conf.urls import url


from .views import SquadRudView, SquadAPIView

app_name = 'api_squads'
urlpatterns = [
    url(r'^$', SquadAPIView.as_view(), name='post-listcreate'),
    url(r'^(?P<pk>\d+)/$', SquadRudView.as_view(), name='post-rud')
]   