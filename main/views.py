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
from django.utils import timezone

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )
from django.contrib.auth.models import User
from constants import *
from schools.models import School

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

    is_trener = False
    is_manager = False
    is_director = False
    profile = None
    if request.user.is_authenticated:
        profile = get_profile(request)
        is_trener = is_profi(profile, 'Teacher')
        is_manager = is_profi(profile, 'Manager')
        is_director = is_profi(profile, 'Director')
    context = {
        "profile":profile,
        "schools":EliteSchools.objects.first().schools.all(),
        "url":School.objects.first().get_landing(),
        'is_trener':is_trener,
        "is_manager":is_manager,
        "is_director":is_director, 
        'main':True,
        'form':form,
    }
    return render(request, "map.html", context)

def hislessons(request):
    profile = get_profile(request)
    res = []
    lesson_now = False
    classwork = []
    if is_profi(profile, 'Teacher'):
        hissubjects = profile.hissquads.all()
    else:
        hissubjects = profile.squads.all()

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

from django.contrib.postgres.search import TrigramSimilarity
def map_search(request):
    text = request.GET.get('text')
    res = []
    if text != '':
        kef = 1
        if len(text) > 4:
            kef = 4
        similarity=TrigramSimilarity('title', text)
        schools = School.objects.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        i = 0
        for school in schools:
            image_url = ''
            if school.image_icon:
                image_url = school.image_icon.url
            res.append([school.id, school.title, image_url, school.address])
            i+=1
            if i == 10:
                break
    else:
        schools = EliteSchools.objects.first().schools.all()
        for school in schools:
            image_url = ''
            if school.image_icon:
                image_url = school.image_icon.url
            res.append([school.id, school.title, image_url, school.address])
    data = {
        "res":res,
    }
    return JsonResponse(data)

def search(request):
    profile = get_profile(request)
    school=profile.schools.first()
    res_profiles = []
    res_subjects = []
    res_squads = []
    res_courses = []
    text = request.GET.get('text')
    kef = 1
    if len(text) > 4:
        kef = 4
    if text != '':
        similarity=TrigramSimilarity('first_name', text)
        profiles = school.people.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        similarity=TrigramSimilarity('title', text)
        subjects = school.school_subjects.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        squads = school.groups.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        courses = school.school_courses.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        i = 0
        for profile in profiles:
            image_url = ''
            if profile.image:
                image_url = profile.image.url
            res_profiles.append([profile.first_name, profile.get_absolute_url(), image_url])
            i+=1
            if i == 4:
                break
        i = 0
        for subject in subjects:
            image_url = ''
            if subject.image_icon:
                image_url = subject.image_icon.url
            res_subjects.append([subject.title, subject.get_absolute_url(), image_url])
            i+=1
            if i == 4:
                break
        i = 0
        for squad in squads:
            image_url = ''
            if squad.image_icon:
                image_url = squad.image_icon.url
            res_squads.append([squad.title, squad.get_absolute_url(), image_url])
            i+=1
            if i == 4:
                break
        i = 0
        for course in courses:
            image_url = ''
            if course.image:
                image_url = course.image.url
            res_courses.append([course.title, course.get_absolute_url(), image_url])
            i+=1
            if i == 4:
                break

    data = {
        "res_profiles":res_profiles,
        "res_subjects":res_subjects,
        "res_squads":res_squads,
        "res_courses":res_courses,
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

def get_notifications(request):
    profile = Profile.objects.get(user = request.user.id)
    timezone.now()
    res = []
    i = 0
    profile.notifications_number = 0
    profile.save()
    for school in profile.schools.all():
        for notif in school.notifications.filter():
            i += 1
            res.append([notif.author_profile.first_name, notif.image_url, notif.itstype, notif.url, notif.text, notif.timestamp.strftime('%d %B %Yг. %H:%M')])
            if i == 4:
                break
    data = {
        'res':res
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

def map_view(request):
    is_trener = False
    is_manager = False
    is_director = False
    profile = None
    if request.user.is_authenticated:
        profile = get_profile(request)
        is_trener = is_profi(profile, 'Teacher')
        is_manager = is_profi(profile, 'Manager')
        is_director = is_profi(profile, 'Director')
    context = {
        "profile":profile,
        "schools":EliteSchools.objects.first().schools.all(),
        "url":School.objects.first().get_landing(),
        'is_trener':is_trener,
        "is_manager":is_manager,
        "is_director":is_director, 
    }
    return render(request, "map.html", context)

def get_landing(request):
    if request.GET.get('id'):
        school = School.objects.get(id=int(request.GET.get('id')))
        data = {
            'title':school.title,
            'address':school.address,
            'phones':school.phones,
            'worktime':school.worktime,
        }
        return JsonResponse(data)
    else:
        return 0
