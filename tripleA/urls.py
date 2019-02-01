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
from accounts.views import (login_view, register_view, logout_view)
from main.views import(main_view)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^register/', register_view, name='register'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^profile/', include("accounts.urls", namespace='accounts')),
    url(r'^groups/', include("squads.urls", namespace='squads')),
    url(r'^schools/', include("schools.urls", namespace='schools')),
    url(r'^subjects/', include("subjects.urls", namespace='subjects')),
    url(r'^papers/', include("papers.urls", namespace='papers')),
    url(r'^tasks/', include("tasks.urls", namespace='tasks')),
    url(r'^docs/', include("docs.urls", namespace='docs')),
    url(r'^clients/', include("clients_base.urls", namespace='clients')),
    url(r'^library/', include("library.urls", namespace='library')),
    url(r'^news/', include("news.urls", namespace='news')),
    url(r'^api/squads/', include('squads.api.urls', namespace='api-squads')),
    url(r'^documents/', include("documents.urls", namespace='documents')),
    url(r'^', include("main.urls", namespace='main')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
