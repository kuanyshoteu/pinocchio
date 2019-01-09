from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import RedirectView
from datetime import datetime, timedelta

from accounts.models import *
from django.contrib.auth.models import User

def profile_list(request):
    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"
    else:
        raise Http404
        
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    else:
        raise Http404

    main_page = 'de'
    if len(MainPage.objects.all()) < 1:
        main_page = MainPage.objects.create()
    else:
        main_page = MainPage.objects.all()[0]

    study_list = []
    registered_list = []
    waiting_list = []
    zaiavka_list = []
    for prf in Profile.objects.all():
        if len(prf.squads.all()) > 0:
            study = False
            for sq in prf.squads.all():
                if datetime.now().date() >= sq.start_date:
                    study_list.append(prf)
                    study = True
                    break
            if study == False:
                registered_list.append(prf)
        else:
            waiting_list.append(prf)

    for zaiavka in Zaiavka.objects.all():
        zaiavka_list.append(zaiavka)    
    context = {
        "staff" : staff,
        "profile": profile,
        'main_page':main_page,
        "user":request.user,
        "study_list":study_list,
        "registered_list":registered_list,
        "waiting_list":waiting_list,
        "zaiavka_list":zaiavka_list,
    }
    return render(request, template_name="clients_base.html", context=context)
