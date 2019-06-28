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
def certificate(request):
    context = {
    }
    return render(request, "certificate.txt", context)
def certificate2(request):
    context = {
    }
    return render(request, "certificate2.txt", context)

def main_view(request):
    if request.user.is_authenticated:
        print(request.user.id)
        profile = Profile.objects.get(user = request.user.id)
        return redirect(profile.get_absolute_url())    

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
        "schools_all":School.objects.all(),
        "url":School.objects.first().get_landing(),
        'is_trener':is_trener,
        "is_manager":is_manager,
        "is_director":is_director, 
        'main':True,
        "subjects":SubjectCategory.objects.all(),
        "ages":SubjectAge.objects.all(),        
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
    res = 'error'
    if request.GET.get('username') and request.GET.get('password'):
        found = False
        if len(Profile.objects.filter(mail=request.GET.get('username'))) > 0:
            profile = Profile.objects.filter(mail=request.GET.get('username'))[0]
            found = True
        elif len(Profile.objects.filter(phone=request.GET.get('username'))) > 0:
            profile = Profile.objects.filter(mail=request.GET.get('username'))[0]
            found = True
        if found:
            res = 'login'
            user = authenticate(username=str(profile.user.username), password=str(request.GET.get('password')))
        try:
            login(request, user)
        except Exception as e:
            res = 'error'

    data = {
        'res':res,
    }
    return JsonResponse(data)

def register_view(request):
    res = 'ok'
    if request.GET.get('name')and request.GET.get('phone') and request.GET.get('password1') and request.GET.get('password2'):
        if request.GET.get('password1') == request.GET.get('password2'):
            if len(Profile.objects.filter(mail=request.GET.get('phone'))) == 0 and len(Profile.objects.filter(phone=request.GET.get('phone'))) == 0:
                new_id = User.objects.order_by("id").last().id + 1
                user = User.objects.create(username='user' + str(new_id), password=request.GET.get('password1'))
                new_user = authenticate(username = user.username, password=request.GET.get('password1'))
                login(request, user)
                profile = Profile.objects.get(user = user)
                profile.first_name = request.GET.get('name')
                if '@' in request.GET.get('phone'):
                    profile.phone = request.GET.get('mail')
                else:
                    profile.mail = request.GET.get('phone')
                profile.save()
            else:
                res = 'second_user'
        else:
            res = 'not_equal_password'

    data = {
        'res':res,
    }
    return JsonResponse(data)

def login_social(request):
    if request.GET.get('status'):
        if request.GET.get('status') == 'facebook':
            pass
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
        i = 0
        categories = SubjectCategory.objects.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        ages = SubjectAge.objects.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        schools = School.objects.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        for category in categories:
            res.append([category.title, 'category'])
            i+=1
            if i == 10:
                break
        for age in ages:
            res.append([age.title, 'age'])
            i+=1
            if i == 10:
                break
        for school in schools:
            res.append([school.title, 'school'])
            i+=1
            if i == 10:
                break
    data = {
        "res":res,
    }
    return JsonResponse(data)
def map_filter(request):
    schools = School.objects.all()
    subject = False
    age = False
    print(request.GET.get('age'), request.GET.get('subject'))
    if len(request.GET.get('subject')) > 0:
        subject = SubjectCategory.objects.get(title = request.GET.get('subject'))
    if len(request.GET.get('age')) > 0:
        age = SubjectAge.objects.get(title = request.GET.get('age'))
    mincost = int(request.GET.get('mincost')) - 1
    maxcost = int(request.GET.get('maxcost')) + 1
    if subject and age:
        schools = schools.filter(average_cost__gt=mincost,average_cost__lt=maxcost,school_subject_categories=subject,school_subject_ages=age)
    elif subject:
        schools = schools.filter(school_subject_categories=subject,average_cost__gt=mincost,average_cost__lt=maxcost)
    elif age:
        schools = schools.filter(school_subject_ages=age,average_cost__gt=mincost,average_cost__lt=maxcost)
    else:
        schools = schools.filter(average_cost__gt=mincost,average_cost__lt=maxcost)

    options = []
    coordinates = []
    res = []
    i = 0
    for school in schools:
        coordinates.append([float(school.latitude), float(school.longtude)])
        point = {
            "properties": {"id":school.id,},
        }
        options.append(point)
        image_url = ''
        if school.image_icon:
            image_url = school.image_icon.url
        res.append([school.id, school.title, image_url, school.school_offices.first().address])
        i+=1
        if i == 15:
            break
    data = {
        'options':options,
        'coordinates':coordinates,
        'res':res,
    }
    return JsonResponse(data)

def map_search_show(request):
    text = request.GET.get('text')
    res = []
    if text != '':
        qs = SubjectCategory.objects.filter(title=text)
        if len(qs) > 0:
            schools = qs[0].schools.all()
        else:
            qs = SubjectAge.objects.filter(title=text)
            if len(qs) > 0:
                schools = qs[0].schools.all()
            else:
                kef = 1
                if len(text) > 6:
                    kef = 4
                similarity=TrigramSimilarity('title', text)
                schools = School.objects.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        i = 0
        for school in schools:
            image_url = ''
            if school.image_icon:
                image_url = school.image_icon.url
            res.append([school.id, school.title, image_url, school.school_offices.first().address, school.slogan])
            i+=1
            if i == 10:
                break
    else:
        schools = EliteSchools.objects.first().schools.all()
        for school in schools:
            image_url = ''
            if school.image_icon:
                image_url = school.image_icon.url
            res.append([school.id, school.title, image_url, school.school_offices.first().address, school.slogan])
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
    profile.skill.notifications_number = 0
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
        "schools_all":School.objects.all(),
        "url":School.objects.first().get_landing(),
        'is_trener':is_trener,
        "is_manager":is_manager,
        "is_director":is_director, 
        "subjects":SubjectCategory.objects.all(),
        "ages":SubjectAge.objects.all(),
    }
    return render(request, "map.html", context)

def get_landing(request):
    if request.GET.get('id'):
        school = School.objects.get(id=int(request.GET.get('id')))
        subjects = []
        for subject in school.school_subject_categories.all():
            subjects.append(subject.title)
        phone = ''
        i = 0
        for p in school.phones[0]:
            phone += p
            if i == 10:
                break
            i += 1
        data = {
            'title':school.title,
            'address':school.school_offices.first().address,
            'region':school.school_offices.first().region,
            'offices':school.offices,
            'phone':phone,
            'phones':school.phones,
            'worktime':school.worktime,
            'subjects':subjects,
            'site':school.site,
            'landing_url':school.landing(),
        }
        return JsonResponse(data)
    else:
        return 0

def get_phone(request):
    if request.GET.get('id'):
        school = School.objects.get(id=int(request.GET.get('id')))
        data = {
            'phone':school.phones,
        }
        return JsonResponse(data)
    else:
        return 0
