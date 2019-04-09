from django.shortcuts import render, redirect
from accounts.models import *
from .models import *
from accounts.forms import *
from squads.models import Squad
from subjects.models import *

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from itertools import chain
from django.views.generic import ListView

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )
from django.contrib.auth.models import User
from constants import *


def loaderio(request):
    context = {
    }
    return render(request, "loaderio.txt", context)

def main_view(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
        return redirect(profile.get_absolute_url())    

    form = EmptyForm(request.POST or None)
    if form.is_valid():
        if request.POST.get('username') and request.POST.get('password'):
            for profile in Profile.objects.all():
                if profile.mail == request.POST.get('username') or profile.phone == request.POST.get('username'):
                    user = authenticate(username=str(profile.user.username), password=str(request.POST.get('password')))
                    if user:
                        login(request, user)
                        return HttpResponseRedirect(profile.get_absolute_url())

    context = {
        'main':True,
        'form':form,
    }
    return render(request, "main.html", context)

def hislessons(request):
    profile = get_profile(request)
    res = []
    lesson_now = False
    classwork = []
    if is_profi(profile, 'Teacher'):
        hissubjects = profile.teachers_subjects.all()
    else:
        hissubjects = profile.hissubjects.all()

    context = {
        "profile":profile,
        'classwork':classwork,
        'homeworks':res,
        'lesson_now':lesson_now,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'), 
    }
    return render(request, "profile/classwork.html", context)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse

def login_view(request):
    if request.GET.get('username') and request.GET.get('password'):
        found = False
        if len(Profile.objects.filter(mail=request.GET.get('username'))) > 0:
            profile = Profile.objects.filter(mail=request.GET.get('username'))[0]
            found = True
        elif len(Profile.objects.filter(phone=request.GET.get('username'))) > 0:
            profile = Profile.objects.filter(mail=request.GET.get('username'))[0]
            found = True

        if found:
            print(request.GET.get('password'),profile.user.username)
            user = authenticate(username=str(profile.user.username), password=str(request.GET.get('password')))
            login(request, user)
    data = {
    }
    return JsonResponse(data)

def register_view(request):
    if request.GET.get('first_name') and request.GET.get('second_name') and request.GET.get('school') and request.GET.get('phone') and request.GET.get('mail') and request.GET.get('password1') and request.GET.get('password2'):
        if request.GET.get('password1') == request.GET.get('password2'):
            new_id = User.objects.order_by("id").last().id + 1
            user = User.objects.create(username='user' + str(new_id), password=request.GET.get('password1'))
            new_user = authenticate(username = user.username, password=request.GET.get('password1'))
            login(request, user)
            profile = Profile.objects.get(user = user)
            profile.first_name = request.GET.get('first_name')
            profile.second_name = request.GET.get('second_name')
            profile.school = request.GET.get('school')
            profile.phone = request.GET.get('phone')
            profile.mail = request.GET.get('mail')
            profile.save()
    data = {
    }
    return JsonResponse(data)

def ChangeSubject(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('id'):
        subject = Subject.objects.get(id = int(request.GET.get('id')))
        if request.GET.get('text'):
            subject.text = request.GET.get('text')
        if request.GET.get('title'):
            subject.title = request.GET.get('title')
        if request.GET.get('cost'):
            subject.cost = request.GET.get('cost')
        subject.save()
                    
    data = {
    }
    return JsonResponse(data)

def SaveZaiavka(request):
    profile = Profile.objects.get(user = request.user.id)
    only_teachers(profile)
    if request.GET.get('name'):
        if request.GET.get('phone'):
            zaiavka = Zaiavka.objects.create(name=request.GET.get('name'), phone=request.GET.get('phone'))
    data = {
    }
    return JsonResponse(data)

def contacts_view(request):
    profile = get_profile(request)
    context = {
        "profile":profile,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'), 
    }
    return render(request, "contacts.html", context)

