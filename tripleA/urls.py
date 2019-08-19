"""tripleA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from accounts.views import (logout_view, confirm_email)
from papers.views import courses
from main.views import(main_view, loaderio, handler404)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^profile/', include("accounts.urls", namespace='accounts')),
    url(r'^groups/', include("squads.urls", namespace='squads')),
    url(r'^schools/', include("schools.urls", namespace='schools')),
    url(r'^subjects/', include("subjects.urls", namespace='subjects')),
    url(r'^papers/', include("papers.urls", namespace='papers')),
    url(r'^tasks/', include("tasks.urls", namespace='tasks')),
    url(r'^todolist/', include("todolist.urls", namespace='todolist')),
    url(r'^library/', include("library.urls", namespace='library')),
    url(r'^news/', include("news.urls", namespace='news')),
    url(r'^courses/$', courses, name='courses'),        
    url(r'^api/squads/', include('squads.api.urls', namespace='api-squads')),
    url(r'^documents/', include("documents.urls", namespace='documents')),
    url(r'^loaderio-3614d85f1228305eef28963b2654a5ae', loaderio, name='loaderio'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^confirm/', confirm_email, name="confirm_email"),
    url(r'^', include("main.urls", namespace='main')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.conf.urls import (handler400, handler403, handler404, handler500)

handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(r'^static/(?P<path>.*)$', document_root=settings.STATIC_ROOT)
