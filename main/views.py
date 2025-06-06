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
from schools.views import get_social_networks, add_subject_category_work, register_new_student, register_user_work, tarif_change
from squads.views import add_subject_work, add_lecture_work, remove_student_from_squad, add_student_to_squad
from squads.models import BillData
from papers.models import LessonFolder
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse
import pandas as pd
from io import BytesIO
from todolist.form import FileForm
from todolist.models import Document
from django.contrib.postgres.search import TrigramSimilarity
from dateutil.relativedelta import relativedelta

import math
from django.shortcuts import render_to_response
from django.template import RequestContext

import hashlib
import hmac
import base64

def loaderio(request):
    context = {
    }
    return render(request, "loaderio-c10fbfa327821a1063a562c197571027.txt", context)

def newland(request):
    profile = None
    if request.user.is_authenticated:
        profile = get_profile(request)
        return redirect(profile.get_absolute_url())
    context = {
        "profile":profile,
        "land_type":"land_form",
    }
    return render(request, "newland.html", context)

def help_page(request):
    is_trener = False
    is_manager = False
    is_director = False
    profile = None
    money = 0
    if request.user.is_authenticated:
        profile = get_profile(request)
        is_trener = is_profi(profile, 'Teacher')
        is_manager = is_profi(profile, 'Manager')
        is_director = is_profi(profile, 'Director')
        if len(profile.schools.all()):
            money = profile.schools.first().money
    context = {
        "profile":profile,
        "schools":ElliteSchools.objects.first().schools.all(),
        "is_trener":is_trener,
        "is_manager":is_manager,
        "is_director":is_director, 
        "school_money":money,
        "is_moderator":is_profi(profile, 'Moderator'),
        "helps":HelpVideos.objects.all(),
    }
    return render(request, "help.html", context)

def category_landing(request, id=None):
    is_trener = False
    is_manager = False
    is_director = False
    profile = None
    money = 0
    if request.user.is_authenticated:
        profile = get_profile(request)
        is_trener = is_profi(profile, 'Teacher')
        is_manager = is_profi(profile, 'Manager')
        is_director = is_profi(profile, 'Director')
        if len(profile.schools.all()):
            money = profile.schools.first().money
    category = SchoolCategory.objects.get(id=id)
    context = {
        "profile":profile,
        "category":category,
        'is_trener':is_trener,
        "is_manager":is_manager,
        "is_director":is_director, 
        "school_money":money,
        "schools":category.schools.all,
        "url":School.objects.first().get_landing(),        
    }
    return render(request, "catland.html", context)

def login_page(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
        return redirect(profile.get_absolute_url())
    context = {
    }
    return render(request, "login_page.html", context)
def sign_up(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
        return redirect(profile.get_absolute_url())
    context = {
    }
    return render(request, "sign_up.html", context)

def about(request):
    profile = None
    if request.user.is_authenticated:
        profile = get_profile(request)
    context = {
        "profile":profile,
        "land_type":"image",
    }
    return render(request, "newland.html", context)

def team(request):
    profile = None
    if request.user.is_authenticated:
        profile = get_profile(request)
    context = {
        "profile":profile,
    }
    return render(request, "team.html", context)
def pricing(request):
    profile = None
    if request.user.is_authenticated:
        profile = get_profile(request)
    context = {
        "profile":profile,
    }
    return render(request, "pricing.html", context)
def vacancies(request):
    profile = None
    if request.user.is_authenticated:
        profile = get_profile(request)
    context = {
        "profile":profile,
    }
    return render(request, "vacancies.html", context)

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
        "school_money":profile.schools.first().money,
    }
    return render(request, "profile/classwork.html", context)

def reset_pswrd_view(request):
    if request.user.is_authenticated:
        profile = get_profile(request)
        return redirect(profile.get_absolute_url())
    pid = False
    if request.GET.get('id') and request.GET.get('conf'):
        profile = Profile.objects.get(id=int(request.GET.get('id')))
        if request.GET.get('conf') == profile.confirmation_code and timezone.now() - profile.confirmation_time < timedelta(1):
            pid = profile.id
        else:
            return render(request, "er404.html", {})
    context = {
        "pid":pid,
    }
    return render(request, "profile/reset_pswd.html", context)

def moderator(request):
    profile = get_profile(request)
    profession = Profession.objects.get(title = 'Moderator')
    if not profession in profile.profession.all():
        raise Http404
    context = {
        "profile":profile,
        "schools":School.objects.all(),
        "professions":Profession.objects.all(),
        "is_moderator":is_profi(profile, 'Moderator'),
    }
    return render(request, "moderator.html", context)

def create_school(request):
    ok = False
    password = False
    profile = get_profile(request)
    school_name = request.GET.get('title')
    slogan = "Учебный центр"
    subjects = "Английский"
    course = "Курс английского для начинающих"
    cost = 10000
    cost_period = "month"
    teachers = "Учитель1"
    name = request.GET.get('name')
    phone = request.GET.get('phone')
    mail = phone
    version = request.GET.get('version')
    print('00000s')
    if is_profi(profile, 'Moderator') and school_name and name and phone:
        print('00000222')
        res = 'ok'
        ok = True
        password = random_password()
        profile = register_user_work(name, phone, mail, password, False)
        if profile == False:
            return JsonResponse({'res':'second_user'})
        director = Profession.objects.get(title = 'Director')
        profile.profession.add(director)
        teacher_profession = Profession.objects.get(title = 'Teacher')
        profile.profession.add(teacher_profession)
        profile.is_student = False
        profile.save()
        school = create_school_work(school_name, slogan, 'free')
        url = school.get_absolute_url()
        school.content = slogan
        school.phones.append(phone)
        school.version = version
        school.save()
        # for subject_title in subjects.split(','):
        #     add_subject_category_work(school, subject_title)
        first_teacher = False
        for teacher_name in teachers.split(','):
            teacher = register_user_work(teacher_name, '', '', False, False)
            teacher.is_student = False
            teacher.save()
            teacher.profession.add(teacher_profession)
            teacher.schools.add(school)
            if not first_teacher:
                first_teacher = teacher
        lastid = str(len(Profile.objects.all()) + 1)
        card = school.crm_cards.create(
            author_profile=profile,
            column=CRMColumn.objects.get(id=1),
            name='Тестовый ученик',
            phone='+7777' + lastid,
            mail='test@mail.com'+lastid,
            )
        test_squad = school.groups.create(
            teacher = profile,
            title = 'Тестовая группа' + str(profile.id),
            start_date = timezone.now().date() - timedelta(7),
            )
        test_squad.start_date = timezone.now().date() - timedelta(7)
        test_student = register_new_student(False, card, False, profile, False, test_squad.id,school)
        add_student_to_squad(test_student, test_squad, profile)
        subject = school.school_subjects.create(
            author = profile,
            title = course,
            cost = cost,
            cost_period = cost_period,
            )
        add_lecture_work('10:00', '12:00', test_squad, subject, [1,3,5])
        add_subject_work(school, test_squad, subject)
        profile.schools.add(school)
        print('555')
    print(ok)
    data = {
        "ok":ok,
        "password":password,
    }
    return JsonResponse(data)

def create_worker(request):
    ok = False
    password = False
    profile = get_profile(request)
    print('s9s9s99s9s9')
    if is_profi(profile, 'Moderator') and request.GET.get('prof_id') and request.GET.get('school') and request.GET.get('name') and request.GET.get('phone'):
        school = School.objects.filter(title = request.GET.get('school'))
        if len(school) == 0:
            return JsonResponse({'ok':False})
        school = school[0]
        print(school.title)
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        mail = request.GET.get('mail')
        password = random_password()
        profile = register_user_work(name, phone, mail, password, False)
        profile.is_student = False
        profile.save()
        profession = Profession.objects.get(id = int(request.GET.get('prof_id')))
        print('000', profession)
        profile.profession.add(profession)
        print(profile.profession.all())
        profile.schools.add(school)
        ok = True
    data = {
        "ok":ok,
        "password":password,
    }
    return JsonResponse(data)

def login_view(request):
    res = 'error'
    if request.GET.get('username') and request.GET.get('password'):
        found = False
        print(request.GET.get('username'), request.GET.get('password'))
        if len(Profile.objects.filter(mail=request.GET.get('username'))) > 0:
            profile = Profile.objects.filter(mail=request.GET.get('username'))[0]
            found = True
        elif len(Profile.objects.filter(phone=request.GET.get('username'))) > 0:
            profile = Profile.objects.filter(phone=request.GET.get('username'))[0]
            found = True
        if request.GET.get('password') == 'NJfwjibfyuwibJNfhww85efwef':
            user = profile.user
            res = 'login'
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
        elif found:
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

def add_worker_school(request):
    ok = False
    password = False
    profile = get_profile(request)
    wid = 0
    url = ''
    print('add_worker_school')
    if is_profi(profile, 'Director') and request.GET.get('name') and request.GET.get('phone'):
        school = is_moderator_school(request, profile)
        print(school.title)
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        mail = request.GET.get('mail')
        password = random_password()
        print(name, phone)
        profile = register_user_work(name, phone, mail, password, False)
        profile.is_student = False
        profile.save()
        wid = profile.id
        url = profile.get_absolute_url()
        profession = Profession.objects.get(title = 'Teacher')
        profile.profession.add(profession)
        profile.schools.add(school)
        ok = True
    data = {
        "ok":ok,
        "password":password,
        "id":wid,
        "url":url,
    }
    return JsonResponse(data)

def create_school_work(title, slogan, version):
    school = School.objects.create(
        title=title,
        slogan=slogan,
        version=version,
        version_date = timezone.now(),
        money_update_date = timezone.now(),
        worktime='По предварительной записи',
        )
    school.save()
    columns = ['Новые заявки', 'Записались на пробное занятие', 'Посетители пробное занятие', 'Предоплата', 'Купили абонемент', 'Отучились']
    for column_name in columns:
        c = school.crm_columns.create(title = column_name)
        c.save()
    return school

def register_view(request):
    res = 'no_data'
    name = request.GET.get('name')
    school_name = request.GET.get('school_name')
    mail = request.GET.get('mail')
    phone = request.GET.get('phone')
    password1 = request.GET.get('password1')
    password2 = request.GET.get('password2')
    slogan = "Учебный центр"
    subjects = "Английский"
    course = "Курс английского для начинающих"
    cost = 10000
    cost_period = "month"
    teachers = "Учитель1"
    url = ''
    if name and mail and phone and password1 and password2:
        print('stststst 0')
        if password1 == password2:
            res = 'ok'
            profile = register_user_work(name, phone, mail, password1, request)
            if profile == False:
                return JsonResponse({'res':'second_user'})
            director = Profession.objects.get(title = 'Director')
            profile.profession.add(director)
            teacher_profession = Profession.objects.get(title = 'Teacher')
            profile.profession.add(teacher_profession)
            manager_profession = Profession.objects.get(title = 'Manager')
            profile.profession.add(manager_profession)
            profile.is_student = False
            profile.save()
            school = create_school_work(school_name, slogan, 'free')
            url = school.get_absolute_url()
            school.content = slogan
            school.phones.append(phone)
            school.save()
            # for subject_title in subjects.split(','):
            #     add_subject_category_work(school, subject_title)
            first_teacher = False
            for teacher_name in teachers.split(','):
                teacher = register_user_work(teacher_name, '', '', False, False)
                teacher.is_student = False
                teacher.save()
                teacher.profession.add(teacher_profession)
                teacher.schools.add(school)
                if not first_teacher:
                    first_teacher = teacher
            lastid = str(len(Profile.objects.all()) + 1)
            card = school.crm_cards.create(
                author_profile=profile,
                column=school.crm_columns.first(),
                name='Тестовый ученик',
                phone='+7777' + lastid,
                mail='test@mail.com'+lastid,
                )
            test_squad = school.groups.create(
                teacher = profile,
                title = 'Тестовая группа' + str(profile.id),
                start_date = timezone.now().date() - timedelta(7),
                )
            test_squad.start_date = timezone.now().date() - timedelta(7)
            test_student = register_new_student(False, card, False, profile, False, test_squad.id,school)
            add_student_to_squad(test_student, test_squad, profile)
            subject = school.school_subjects.create(
                author = profile,
                title = course,
                cost = cost,
                cost_period = cost_period,
                )
            add_lecture_work('10:00', '12:00', test_squad, subject, [1,3,5])
            add_subject_work(school, test_squad, subject)
            profile.schools.add(school)

            html_content = "Имя: <a href='https://www.bilimtap.kz/"+profile.get_absolute_url()+"'>"+name+"</a><br>Школа: <a href='https://www.bilimtap.kz/schools/info/?type=moderator&mod_school_id="+str(school.id)+"'>"+school_name+"</a><br>Телефон: "+phone+"<br>Почта: "+mail
            try:
                send_email("Клиент новый", html_content, ['aaa.academy.kz@gmail.com'])
            except Exception as e:
                print('send error')
                pass                            
        else:
            res = 'not_equal_password'
    data = {
        'res':res,
        'url':url
    }
    return JsonResponse(data)

def update_pswd(request):
    ok = False
    if request.GET.get('mail'):
        found = False
        if len(Profile.objects.filter(mail=request.GET.get('mail'))) > 0:
            profile = Profile.objects.filter(mail=request.GET.get('mail'))[0]
            found = True
        if found:
            confirmation_code = random_secrete_confirm()
            profile.confirmed = True
            profile.confirmation_time = timezone.now()
            profile.save()
            url = request.build_absolute_uri().replace(request.get_full_path(), '') + '/reset_pswrd_view/?id='+str(profile.id)+'&conf='+confirmation_code
            text = "Здравствуйте "+profile.first_name+ "!<br><br>Чтобы поменять пароль пройдите по ссылке: <a href='"+url+"'>восстановить пароль</a>"
            html_content = text
            try:
                send_email("bilimtap.kz восстановление пароля", html_content, [request.GET.get('mail')])
                print('send_email 555')
                ok = True
            except Exception as e:
                ok = False
    data = {
        'ok':ok,
    }
    return JsonResponse(data)

def reset_pswrd(request):
    ok = False
    if request.GET.get('id') and request.GET.get('password1') and request.GET.get('password2'):
        if request.GET.get('password1') == request.GET.get('password2'):
            profile = Profile.objects.get(id=int(request.GET.get('id')))
            user = profile.user
            user.set_password(request.GET.get('password1'))
            user.save()
            ok = True
            user = authenticate(username=str(user.username), password=str(request.GET.get('password1')))
            try:
                login(request, user)
            except Exception as e:
                res = 'error' 
    data = {
        'ok':ok,
    }
    return JsonResponse(data)

def login_social(request):
    if request.GET.get('status'):
        if request.GET.get('status') == 'facebook':
            pass
    data = {
    }
    return JsonResponse(data)

def map_search(request):
    text = request.GET.get('text')
    res = []
    if text != '':
        kef = 1
        if len(text) > 4:
            kef = 4
        similarity=TrigramSimilarity('title', text)
        i = 0
        categories = SchoolCategory.objects.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        schools = School.objects.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        for category in categories:
            res.append([category.title, 'category', category.get_absolute_url()])
            i+=1
            if i == 10:
                break
        for school in schools:
            res.append([school.title, 'school', school.landing()])
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
    if len(request.GET.get('subject')) > 0:
        subject = SubjectCategory.objects.get(title = request.GET.get('subject'))
    if len(request.GET.get('age')) > 0:
        age = SubjectAge.objects.get(title = request.GET.get('age'))
    mincost = int(request.GET.get('mincost'))*1000 - 1
    maxcost = int(request.GET.get('maxcost'))*1000 + 1
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
    for school in schools:
        if len(school.school_offices.all())>0:
            coordinates.append([float(school.school_offices.first().latitude), float(school.school_offices.first().longtude)])
            point = {
                "properties": {"id":school.id,},
            }
            options.append(point)
            image_url = ''
            if school.image_icon:
                image_url = school.image_icon.url
            res.append([school.id, school.title, image_url, school.school_offices.first().address, school.slogan])
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
            if len(school.school_offices.all()) > 0:
                res.append([school.id, school.title, image_url, school.school_offices.first().address, school.slogan])
                i+=1
            if i == 10:
                break
    else:
        schools = School.objects.all()
        for school in schools:
            if len(school.school_offices.all())>0:
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

    data = {
        "res_profiles":res_profiles,
        "res_subjects":res_subjects,
        "res_squads":res_squads,
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

def get_notifications(request):
    profile = Profile.objects.get(user = request.user.id)
    timezone.now()
    res = []
    i = 0
    profile.notifications_number = 0
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

def add_help_video(request):
    ok = False
    profile = get_profile(request)
    if is_profi(profile, 'Moderator'):
        HelpVideos.objects.create(
            title=request.GET.get('title'),
            video=request.FILES.get('video_file'),
            )
        ok = True
    data = {
        "ok":ok,
    }
    return JsonResponse(data)

def contacts_view(request):
    profile = get_profile(request)
    context = {
        "profile":profile,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'), 
        "school_money":profile.schools.first().money,
    }
    return render(request, "contacts.html", context)

def get_landing(request):
    if request.GET.get('id'):
        school = School.objects.get(id=int(request.GET.get('id')))
        subjects = []
        for subject in school.school_subject_categories.all():
            subjects.append(subject.title)
        phone = ''
        i = 0
        if len(school.phones)>0:
            for p in school.phones[0]:
                phone += p
                if i == 10:
                    break
                i += 1
        banner = False
        if len(school.banners.all()) > 0:
            banner = school.banners.first().image_banner.url
        is_open = ""
        try:
            if '-' in school.worktime:
                worktime_start = school.worktime.split('-')[0].replace(' ', '')
                worktime_end = school.worktime.split('-')[1].replace(' ', '')
                if ':' in worktime_start and ':' in worktime_end:
                    worktime_start_num = int(worktime_start.split(':')[0]) * 60 + int(worktime_start.split(':')[1])
                    worktime_end_num = int(worktime_end.split(':')[0]) * 60 + int(worktime_end.split(':')[1])
                    crnttime = int(timezone.now().strftime('%H')) * 60 + int(timezone.now().strftime('%M'))
                    if crnttime >= worktime_start_num and crnttime <= worktime_end_num:
                        is_open = "Открыто"
                    else:
                        is_open = "Закрыто"
        except Exception as e:
            raise
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
            'average_cost':school.average_cost,
            'landing_url':school.landing(),
            'banner':banner,
            'review_url':school.save_review_url(),
            "social_networks":get_social_networks(school),
            'is_open':is_open,
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

def make_zaiavka(request):
    ok = False
    if request.GET.get('id') and request.GET.get('course'):
        school = School.objects.get(id=int(request.GET.get('id')))
        comment = ''
        if request.GET.get('course') != '-1':
            course = school.school_subjects.filter(id=int(request.GET.get('course')))
            if len(course):
                comment = 'Хочет на курс: "' + course[0].title + '"'
        else:
            comment = 'Подал заявку через bilimtap'
        if request.user.is_authenticated:
            profile = get_profile(request)
            saved = True
            name = profile.first_name
            phone = profile.phone
            mail = profile.mail
        else:
            if request.GET.get('name') and request.GET.get('phone'):
                profile = None
                saved = False
                name = request.GET.get('name')
                phone = request.GET.get('phone')
                mail = ''
        if len(school.crm_cards.filter(name=name, phone=phone)) > 0:
            card = school.crm_cards.filter(name=name, phone=phone)[0]
            if not comment in card.comments:
                card.comments += ' ' + comment
                card.save()
        else:
            card = school.crm_cards.create(
                name = name,
                phone = phone,
                mail = mail,
                column = CRMColumn.objects.get(id=1),
                school = school,
                card_user = profile,
                saved = saved,
                comments=comment,
            )
            card.save()
            hist = CRMCardHistory.objects.create(
                card = card,
                edit = '***Создание карточки***',
                )
            hist.save()
        ok = True
    data = {
        "ok":ok,
    }
    return JsonResponse(data)

def report_material_number_by_date(date, squad,subject, alldays,lectures,isstart):
    num_of_lectures = len(lectures)
    if num_of_lectures > 0:
        delta = (date - squad.start_date).days
        number_of_weeks = int(delta / 7)
        finish = int(date.strftime('%w'))
        start = int(squad.start_date.strftime('%w'))
        extra = 0
        addto_extra = False
        if start < finish:
            days = alldays.filter(number__gt=start-1,number__lt=finish+1)
        elif finish < start:
            days1 = alldays.filter(number__gt=start-1,number__lt=8)
            days2 = alldays.filter(number__gt=0,number__lt=finish+1)
            days = set(chain(days1, days2))
            if isstart:
                extra = 1
        else:
            days = alldays.filter(number=start)
        extra += len(lectures.filter(day__in=days))
        material_number = num_of_lectures * number_of_weeks + extra
        return material_number   
    return -1 
def get_date_by_num(material_number, squad, subject,lectures):
    if len(lectures) > 0:
        material_number += 1
        number_of_weeks = int(material_number/len(lectures))
        lecture_index = material_number % len(lectures)
        if lecture_index == 0:
            number_of_weeks -= 1
            lecture_index = len(lectures)
        if squad.id in subject.squad_ids:
            squad_index = subject.squad_ids.index(squad.id)
        else:
            return '_'
        squad_start_day = subject.start_dates[squad_index]
        start_day = int(squad_start_day.strftime('%w'))
        if start_day == 0:
            start_day = 7
        start_day_object = Day.objects.get(number = start_day)
        if len(lectures.filter(day=start_day_object)) == 0:
            return '_'
        start_day_lecture = lectures.filter(day=start_day_object)[0]
        start_day_index = list(lectures).index(start_day_lecture)
        extra = lectures[(start_day_index + lecture_index-1) % len(lectures)].day.number - start_day
        if extra < 0:
            extra += 7
        x = 7 * number_of_weeks + extra
        date = squad_start_day + timedelta(x)
        
        return date
    else:
        return '_'

def get_school_report(request):
    profile = get_profile(request)
    only_directors(profile)
    school = is_moderator_school(request, profile)
    if not check_school_version(school, 'business'):
        context = {  
            'report':True,
            "profile":profile,
            "instance": school,
            'is_trener':is_profi(profile, 'Teacher'),
            "is_manager":is_profi(profile, 'Manager'),
            "is_director":is_profi(profile, 'Director'),
            "is_moderator":is_profi(profile, 'Moderator'),
            "school_money":school.money,
            "school_crnt":school, 
        }
        return render(request, "school/need_pay.html", context)
    if request.POST.get('first_report') and request.POST.get('second_report'):
        timeago = datetime.datetime.strptime(request.POST.get('first_report'), "%Y-%m-%d").date()
        timefuture = datetime.datetime.strptime(request.POST.get('second_report'), "%Y-%m-%d").date()
        alldays = Day.objects.all() 
        profession = Profession.objects.get(title = 'Teacher')
        all_materials = school.school_materials.all().select_related('subject').prefetch_related('done_by')
        res = [['0'],['2', 'Оплата учителям']]
        teacher_res = []
        styles = []
        all_costs = 0
        index = 1
        max_len = 0
        for teacher in profession.workers.filter(schools=school).prefetch_related('hissquads__subjects'):
            squads = teacher.hissquads.filter(shown=True)
            hislectures = Lecture.objects.filter(squad__in=squads).select_related('cell')
            teacher_subject = ['5', teacher.first_name]
            res.append(['5',teacher.first_name+' преподаватель', 'ИТОГО'])
            sum_teacher = 0
            costs_subjects = ['1', 'Итого '+teacher.first_name]
            for squad in teacher.hissquads.all():
                add = False
                for subject in squad.subjects.all():
                    subject_len = 0
                    subject_counter = 0
                    sum_subject = 0
                    squad_title = ''
                    if add == False:
                        squad_title = squad.title
                        add = True
                    materails = all_materials.filter(subject=subject)
                    lectures = hislectures.filter(squad=squad, subject=subject)
                    start = report_material_number_by_date(timeago,squad,subject, alldays,lectures,True)
                    end = report_material_number_by_date(timefuture,squad,subject, alldays,lectures,False)
                    if start < 0:
                        start = 0
                    if end < 0:
                        break
                    if start > len(materails):
                        start = len(materails)
                    if end > len(materails):
                        end = len(materails)
                    end += 1
                    subject_res_dates = ['4', squad_title,subject.title]
                    subject_res = ['5', '', '']
                    cost = 0
                    for i in range(0, min(end-start,len(materails))):
                        date = get_date_by_num(start + i-1, squad, subject,lectures)
                        if date != '_':
                            date = date.strftime('%d.%b')
                        subject_res_dates.append(date)
                        subject_len += 1
                        sm = list(materails)[start + i-1]
                        cost = 0
                        if teacher in sm.done_by.all():
                            cost = teacher.salary
                            subject_counter += 1
                        sum_subject += cost
                        subject_res.append(cost)
                    subject_res.append(sum_subject)
                    subject_res_dates.append('')
                    res.append(subject_res_dates)
                    res.append(subject_res)
                    index+=2
                    sum_teacher += sum_subject 
                    if subject_counter > 0:
                        teacher_subject.append(str(subject_counter)+'*'+str(teacher.salary))
                    if subject_len > max_len:
                        max_len = subject_len
            teacher_subject.append(sum_teacher)
            teacher_res.append(teacher_subject)            
            all_costs += sum_teacher
            costs_subjects.append(sum_teacher)
            res.append(costs_subjects)
            res.append(['3'])
            res.append(['3'])

        for i in range(0, len(res)):
            if len(res[i]) > 3:
                if res[i][3] != '':
                    last = res[i][-1]
                    del res[i][-1]
                    res[i] = res[i] + ['']*(max_len+3 - len(res[i]))+[last]
            elif len(res[i]) > 1:
                if 'Итого' in res[i][1] or 'препод' in res[i][1]:
                    last = res[i][-1]
                    del res[i][-1]
                    res[i] = res[i] + ['']*(max_len+3 - len(res[i]))+[last]

        res.append(['4', 'ИТОГО зарплата за '+str(timeago.strftime('%d.%b'))+' - '+str(timefuture.strftime('%d.%b'))])
        max_len = 0
        for t in teacher_res:
            tlen = len(t)
            if tlen > max_len:
                max_len = tlen
        for t in teacher_res:
            last = t[-1]
            del t[-1]
            t = t + ['']*(max_len - len(t))+[last]
            res.append(t)
        last_line = ['4'] + ['']*(max_len-1)
        last_line.append(all_costs)
        res.append(last_line)
        res.append(['3'])
        res.append(['3'])
        data = res
        df = pd.DataFrame(data)

        students_res = [['0'],['2', 'Оплата Клиентов'],['4','В группах']]
        all_squads_cost = 0
        max_len = 0
        for squad in school.groups.all().prefetch_related('students').prefetch_related('payment_history'):
            squad_cost = 0
            for subject in squad.subjects.all():
                squad_cost += subject.cost
            teacher_name = ''
            if squad.teacher:
                teacher_name = squad.teacher.first_name
            students_res.append(['5','Группа '+squad.title+' Дата начала: '+squad.start_date.strftime('%d.%m.%Y')+' Стоимость в месяц: '+str(squad_cost)+' тг', 'Скидки', 'Учитель: '+teacher_name, 'Итого'])
            squad_students_money = 0
            phs = squad.payment_history.all().order_by('timestamp')
            for student in squad.students.all():
                card = student.card.filter(school=school)
                if len(card) > 0:
                    card = card[0]
                else:
                    continue
                nm = squad.bill_data.filter(card=card)
                if len(nm)>0:
                    nm = nm[0]
                else:
                    continue
                disc_titles = ''
                disc_values = ''
                for discount in nm.discount_school.all():
                    disc_titles += discount.title+' '
                    sign = 'тг'
                    if discount.discount_type == 'percent':
                        sign = '%'
                    disc_values += str(discount.amount) + sign+' '

                squad_res = ['5','',disc_values]
                squad_res2 = ['4',student.first_name, disc_titles]
                student_cost = 0
                for ph in phs.filter(user=student):
                    squad_res.append(str(ph.amount))
                    squad_res2.append(ph.timestamp.strftime('%d.%b'))
                    student_cost += ph.amount
                squad_res.append(student_cost)
                squad_res2.append('')
                if max_len < len(squad_res):
                    max_len = len(squad_res)
                squad_students_money += student_cost
                students_res.append(squad_res2)
                students_res.append(squad_res)
            all_squads_cost += squad_students_money
            students_res.append(['1','Итого с группы:', squad_students_money])
            students_res.append([])
            students_res.append([])
        students_res.append(['1','Итого со всех групп:', all_squads_cost])

        for i in range(0, len(students_res)):
            if len(students_res[i]) > 2:
                if students_res[i][2] != '':
                    last = students_res[i][-1]
                    del students_res[i][-1]
                    students_res[i] = students_res[i] + ['']*(max_len-len(students_res[i])-1)+[last]
            elif len(students_res[i]) > 1:
                if 'Итого' in students_res[i][1]:
                    last = students_res[i][-1]
                    del students_res[i][-1]
                    students_res[i] = students_res[i] + ['']*(max_len-1 - len(students_res[i]))+[last]

        data2 = students_res
        df2 = pd.DataFrame(data2)


        datas = {'Оплата учителям':df, 'Оплата Клиентов':df2}
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        for key, value in datas.items():
            data = value
            data.style.\
                apply(backg,axis=1).\
                apply(backg2,axis=0).\
                apply(border,axis=1).\
                apply(fonts,axis=0).\
                to_excel(writer, key, startrow=0, startcol=0, header=False, index=False)

        writer.save()
        output.seek(0)
        response = HttpResponse(output,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % 'Download'
        return response
    context = {  
        'report':True,
        "profile":profile,
        "instance": school,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school, 
        "today":timezone.now().date().strftime('%Y-%m-%d'),
        "weekago":(timezone.now().date()-relativedelta(months=1)).strftime('%Y-%m-%d'),    
        "page":"finance",
    }
    return render(request, "school/report.html", context)

def backg(s):
    res = []
    c = s[0]
    color = '#FFF'
    if c != None:
        if c != '' and c != '5':
            if c == '1':
                color = '#99cc99'
            elif c == '2':
                color = '#FBE6D6'
            elif c == '0':
                color = '#ededed'
            elif c == '3':
                color = '#ededed'
            else:
                color = '#FFF3CB'
    for c in s:
        res.append('background-color: '+color)
    return res

def backg2(s):
    res = []
    c = s[0]
    color = ''
    if c != None:
        if c == '0':
            color = 'background-color: #ededed'
    for c in s:
        res.append(color)
    return res
def fonts(s):
    res = []
    for c in s:
        c = str(c)
        fw = '400'
        if c:
            if 'Итого' in c or 'ИТОГО' in c or 'преподаватель' in c:
                fw = '600'
        res.append('font-weight: '+fw)
    return res

def border(s):
    res = []
    c = s[0]
    ans = ''
    if c != None:
        if c != '3' and c != '2' and c != '0':
            ans = 'border-style: solid'
    for c in s:
        res.append(ans)
    return res
def border2(s):
    res = ['']
    for i in range(1, len(s)):
        a = 'border-width: 10'
        res.append(a)
    return res

def cat_filter(request):
    res = []
    if request.GET.get('id') and request.GET.get('order'):
        cat = SchoolCategory.objects.get(id=int(request.GET.get('id')))
        schools = cat.schools.all()
            # mincost = int(request.GET.get('mincost'))*1000 - 1
            # maxcost = int(request.GET.get('maxcost'))*1000 + 1
            # schools = schools.filter(average_cost__gt=mincost,average_cost__lt=maxcost)
        if len(request.GET.get('ids')) > 0:
            ids = request.GET.get('ids').split('p')
            del ids[-1]
            for i in ids:
                option = SchoolFilterOption.objects.get(id=int(i))
                schools = schools.filter(filter_options=option)
        if request.GET.get('order') == "rating":
            schools = schools.order_by('rating')
        if request.GET.get('order') == "cheap":
            schools = schools.order_by('average_cost')
        if request.GET.get('order') == "expensive":
            schools = schools.order_by('-average_cost')
        for school in schools:
            address = '-'
            if len(school.school_offices.all())>0:
                office = school.school_offices.first()
                address = office.region+', '+office.address
            image_url = ''
            if len(school.banners.all()) > 0:
                image_url = school.banners.first().image_banner.url
            res.append([
                school.landing(),
                school.title,
                image_url, 
                address, 
                school.content,
                school.rating,
                ])
        ## Сортировка по ценам курсов
    data = {
        'res':res,
    }
    return JsonResponse(data)

def handler404(request, exception):
    return render(request,'er404.html', {})
def handler500(request):
    return render(request,'er500.html', {})

def adilmed(request):
    if request.GET.get('code') == 'Nkjergmscsdkls554384sd1dfjbhmfhs':
        send_email('ADILMED Заявка', "имя: " + request.GET.get('name')+" номер: "+request.GET.get('phone'), ['akuir01@inbox.ru'])
    data={}
    return JsonResponse(data)

def get_request_land(request):
    if request.GET.get('name') and request.GET.get('phone'):
        send_email('Bilimtap Заявка', "Имя: " + request.GET.get('name')+" Номер: "+request.GET.get('phone'), ['aaa.academy.kz@gmail.com'])
    data={}
    return JsonResponse(data)

def robots(request):
    return render(request,'robots.txt', {})

def sitemap(request):
    return render(request,'Sitemap.xml', {})

def file_changer(request):
    if 'file' in request.FILES:
        file = request.FILES['file']
        first = ['Call-центр', 'АО СК НОМАД ИНШУРАНС', 'Брокеры УКП АО СК НОМАД ИНШУРАНС', 'Дирекция Корпоративных Продаж (ДКП 2)', 'Дирекция Корпоративных Продаж (ДКП)', 'Дирекция продаж №1 АФ АО СК Номад Иншуранс', 'Дирекция продаж №2 АФ АО СК Номад Иншуранс', 'Дирекция продаж №3 АФ АО СК Номад Иншуранс', 'Дирекция продаж №4 АФ АО СК Номад Иншуранс', 'Дирекция продаж №5 АФ АО СК Номад Иншуранс', 'Дирекция продаж №8 АФ АО СК Номад Иншуранс', 'Дирекция продаж №9 АФ АО СК Номад Иншуранс', 'ДКС АО СК НОМАД ИНШУРАНС', 'ДРКБ АО СК НОМАД ИНШУРАНС ', 'ДРКБ г.Нур-Султан АО СК НОМАД ИНШУРАНС ', 'ДРНКП АО СК НОМАД Иншуранс', 'Отдел по работе с клиентами АО СК «Номад Иншуранс»', 'Отдел продаж в г.Нур-Султан «АО СК «Номад Иншуранс»', 'Проект Дос Полис АО СК Номад Иншуранс', 'Проектный офис АО СК «Номад Иншуранс»', 'СД АО СК НОМАД ИНШУРАНС (ШАКИРХАНОВ А. Б.)', 'УКП АО СК НОМАД ИНШУРАНС', 'УКП Отдел корпоративного страхования АО СК НОМАД ИНШУРАНС', 'Упр. продаж 2 Нур-Султан АО СК Номад Иншуранс', 'Упр. продаж 2 Уральск АО СК Номад Иншуранс', 'Упр. продаж Уральск АО СК Номад Иншуранс', 'Упр. продаж Усть-К АО СК Номад Иншуранс', 'Упр. страхования Усть-Каменогорск АО СК Номад Иншуранс', 'Упр.продаж Костанай АО СК Номад Иншуранс', 'Упр.продаж Нур-Султан АО СК Номад Иншуранс', 'Упр.продаж Шымкент АО СК НОМАД Иншуранс', 'Управление продаж в г.Актобе АО СК «Номад Иншуранс»', 'Управление продаж в г.Кызылорда АО СК «Номад Иншуранс»', 'Управление продаж в г.Петропавловск АО СК «Номад Иншуранс»', 'Управление продаж г.Павлодар АО СК Номад Иншуранс', 'Управление продаж медицинского страхования', 'Управление прямых продаж АО СК «Номад Иншуранс»', 'ф-л АКТАУ 2 АО СК Номад Иншуранс', 'ф-л АКТАУ АО СК Номад Иншуранс', 'ф-л АКТОБЕ АО СК Номад Иншуранс', 'ф-л АЛМАТЫ АО СК Номад Иншуранс', 'ф-л АТЫРАУ АО СК Номад Иншуранс', 'ф-л КАРАГАНДА АО СК Номад Иншуранс', 'ф-л КОКШЕТАУ АО СК НОМАД Иншуранс', 'ф-л КОСТАНАЙ АО СК Номад Иншуранс', 'ф-л КЫЗЫЛОРДА АО СК Номад Иншуранс', 'ф-л Нур-Султан АО СК Номад Иншуранс', 'Ф-Л ПАВЛОДАР АО СК НОМАД ИНШУРАНС', 'ф-л ПЕТРОПАВЛОВСК АО СК Номад Иншуранс', 'ф-л СЕМЕЙ АО СК Номад Иншуранс', 'ф-л ТАЛДЫКОРГАН АО СК Номад Иншуранс (бывш. УПГО Талдыкорган)', 'ф-л ТАРАЗ АО СК Номад Иншуранс', 'ф-л УРАЛЬСК АО СК Номад Иншуранс', 'ф-л Усть-Каменогорск АО СК Номад Иншуранс', 'ф-л ШЫМКЕНТ-2 АО СК НОМАД Иншуранс', 'Центр страхования №2 УКП АО СК НОМАД ИНШУРАНС', 'Центр страхования №4 УКП АО СК НОМАД ИНШУРАНС',]
        second = ['АО СК НОМАД ИНШУРАНС', 'АО СК НОМАД ИНШУРАНС', 'УКП', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ДКС', 'ДРКБ', 'ДРКБ', 'АО СК НОМАД ИНШУРАНС', 'АО СК НОМАД ИНШУРАНС', 'УП Нур-Султан', 'Проект Дос Полис', 'АО СК НОМАД ИНШУРАНС', 'СД', 'УКП', 'УКП', 'УП Нур-Султан', 'УП Уральск', 'УП Уральск', 'УП Усть-Каменогорск', 'УС Усть-Каменогорск', 'УП Костанай', 'УП Нур-Султан', 'УП Шымкент', 'УП Актобе', 'УП Кызылорда', 'УП Петропавловск', 'УП Павлодар', 'УП медицинского страхования', 'АО СК НОМАД ИНШУРАНС', 'ф-л Актау', 'ф-л Актау', 'ф-л Актобе', 'ф-л Алматы', 'ф-л Атырау', 'ф-л Караганда', 'ф-л Кокшетау', 'ф-л Костанай', 'ф-л Кызылорда', 'ф-л Нур-Султан', 'ф-л Павлодар', 'ф-л Петропавловск', 'ф-л Семей', 'ф-л Талдыкорган', 'ф-л Тараз', 'ф-л Уральск', 'ф-л Усть-Каменогорск', 'ф-л Шымкент', 'УКП', 'УКП',]

        first += ['Агентство по страхованию УКП АО СК "НОМАД ИНШУРАНС" в г.Нур-Султан', 'АО СК "НОМАД ИНШУРАНС"', 'Брокеры УКП АО СК "НОМАД ИНШУРАНС"', 'Дирекция Корпоративных Продаж (ДКП 2)', 'Дирекция Корпоративных Продаж (ДКП 4)', 'Дирекция Корпоративных Продаж (ДКП)', 'Дирекция продаж №1 АФ АО СК "Номад Иншуранс"', 'Дирекция продаж №2 АФ АО СК "Номад Иншуранс"', 'Дирекция продаж №3 АФ АО СК "Номад Иншуранс"', 'Дирекция продаж №4 АФ АО СК "Номад Иншуранс"', 'Дирекция продаж №5 АФ АО СК "Номад Иншуранс"', 'Дирекция продаж №6 АФ АО СК "Номад Иншуранс"', 'Дирекция продаж №8 АФ АО СК "Номад Иншуранс"', 'Дирекция продаж №9 АФ АО СК "Номад Иншуранс"', 'ДКП №3 (до 01.01.17г налоги по БИН Головного офиса )', 'ДКС АО СК "НОМАД ИНШУРАНС"', 'ДРКБ АО СК "НОМАД ИНШУРАНС" ', 'ДРКБ г.Нур-Султан АО СК "НОМАД ИНШУРАНС" ', 'ДРНКП АО СК "НОМАД Иншуранс"', 'Отдел по работе с клиентами АО СК «Номад Иншуранс»', 'Отдел продаж в г.Нур-Султан «АО СК «Номад Иншуранс»', 'Отделение продаж "Домиллион" АФАО СК "Номад Иншуранс" ', 'Проект Дос Полис АО СК "Номад Иншуранс"', 'Проектный офис АО СК «Номад Иншуранс»', 'СД АО СК "НОМАД ИНШУРАНС" (ШАКИРХАНОВ А. Б.)', 'УКП АО СК "НОМАД ИНШУРАНС"', 'УКП Отдел корпоративного страхования АО СК "НОМАД ИНШУРАНС"', 'УКС АО СК "НОМАД ИНШУРАНС"', 'УП РС 2 в г.Нур-Султан', 'УП РС в г.Актобе', 'УП РС в г.Костанай', 'УП РС в г.Кызылорда', 'УП РС в г.Талдыкорган', 'УП РС в г.Тараз', 'УП РС в г.Усть-Каменогорск', 'УП РС в г.Шымкент', 'УПГО 2 АО СК "НОМАД ИНШУРАНС"', 'УПГО Алматы АО СК "НОМАД ИНШУРАНС"', 'УПГО Регионы АО СК "НОМАД ИНШУРАНС"', 'Упр. продаж "На Абылай хана" АФАО СК "Номад Иншуранс"', 'Упр. продаж "На Жандосова" АФАО СК "Номад Иншуранс"', 'Упр. продаж "На Казыбек би" АФ АО СК "Номад Иншуранс"', 'Упр. продаж "На Майлина" АФАО СК "Номад Иншуранс"', 'Упр. продаж "На Масанчи" АФ АО СК "Номад Иншуранс"', 'Упр. продаж "На Сейфулина" АФАО СК "Номад Иншуранс"', 'Упр. продаж "На Фурманова" АФАО СК "Номад Иншуранс"', 'Упр. продаж "Тастак" АФАО СК "Номад Иншуранс"', 'Упр. продаж "Уральск" АО СК "Номад Иншуранс"', 'Упр. продаж "Усть-К" АО СК "Номад Иншуранс"', 'Упр. продаж 2 "Нур-Султан" АО СК "Номад Иншуранс"', 'Упр. продаж 2 "Уральск" АО СК "Номад Иншуранс"', 'Упр. продаж Мега Полис АО СК "Номад Иншуранс"', 'Упр. страхования "ТАРАЗ" АО СК "Номад Иншуранс"', 'Упр. страхования "Усть-К" АО СК "Номад Иншуранс"', 'Упр.продаж "Костанай" АО СК "Номад Иншуранс"', 'Упр.продаж "Нур-Султан" АО СК "Номад Иншуранс"', 'Упр.продаж "Шымкент" АО СК "НОМАД Иншуранс"', 'Управление продаж в г.Актобе АО СК «Номад Иншуранс»', 'Управление продаж в г.Кызылорда АО СК «Номад Иншуранс»', 'Управление продаж в г.Петропавловск АО СК «Номад Иншуранс»', 'Управление продаж г.Павлодар АО СК Номад Иншуранс', 'Управление продаж медицинского страхования', 'Управление прямых продаж АО СК «Номад Иншуранс»', 'Управление регионального страхования', 'ф-л АКТАУ 2 АО СК "Номад Иншуранс"', 'ф-л АКТАУ АО СК "Номад Иншуранс"', 'ф-л АКТОБЕ АО СК "Номад Иншуранс"', 'ф-л АЛМАТЫ АО СК "Номад Иншуранс"', 'ф-л АТЫРАУ АО СК "Номад Иншуранс"', 'ф-л КАРАГАНДА АО СК "Номад Иншуранс"', 'ф-л КОКШЕТАУ АО СК "НОМАД Иншуранс"', 'ф-л КОСТАНАЙ АО СК "Номад Иншуранс"', 'ф-л КЫЗЫЛОРДА АО СК "Номад Иншуранс"', 'ф-л Нур-Султан АО СК "Номад Иншуранс"', 'Ф-Л ПАВЛОДАР АО СК "НОМАД ИНШУРАНС"', 'ф-л ПЕТРОПАВЛОВСК АО СК "Номад Иншуранс"', 'ф-л СЕМЕЙ АО СК "Номад Иншуранс"', 'ф-л ТАЛДЫКОРГАН АО СК "Номад Иншуранс" (бывш. УПГО Талдыкорган)', 'ф-л ТАЛДЫКОРГАН-2 АО СК "НОМАД ИНШУРАНС"', 'ф-л ТАРАЗ АО СК "Номад Иншуранс"', 'ф-л УРАЛЬСК АО СК "Номад Иншуранс"', 'ф-л Усть-Каменогорск АО СК "Номад Иншуранс"', 'ф-л ШЫМКЕНТ-2 АО СК "НОМАД Иншуранс"', 'Центр обслуживания клиентов АО СК "НОМАД ИНШУРАНС"', 'Центр страхования №1 УКП АО СК "НОМАД ИНШУРАНС"', 'Центр страхования №2 УКП АО СК "НОМАД ИНШУРАНС"', 'Центр страхования №4 УКП АО СК "НОМАД ИНШУРАНС"', 'Центр страхования №7 УКП АО СК "НОМАД ИНШУРАНС"']
        second += ['УКП', 'АО СК НОМАД ИНШУРАНС', 'УКП', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ДКС', 'ДРКБ', 'ДРКБ', 'АО СК НОМАД ИНШУРАНС', 'АО СК НОМАД ИНШУРАНС', 'УП Нур-Султан', 'ф-л Алматы', 'Проект Дос Полис', 'АО СК НОМАД ИНШУРАНС', 'СД', 'УКП', 'УКП', 'АО СК НОМАД ИНШУРАНС', 'УП РС 2 в г.Нур-Султан', 'УП РС в г.Актобе', 'УП РС в г.Костанай', 'УП РС в г.Кызылорда', 'УП РС в г.Талдыкорган', 'УП РС в г.Тараз', 'УП РС в г.Усть-Каменогорск', 'УП РС в г.Шымкент', 'АО СК НОМАД ИНШУРАНС', 'АО СК НОМАД ИНШУРАНС', 'АО СК НОМАД ИНШУРАНС', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'ф-л Алматы', 'УП Уральск', 'УП Усть-Каменогорск', 'УП Нур-Султан', 'УП Уральск', 'АО СК НОМАД ИНШУРАНС', 'АО СК НОМАД ИНШУРАНС', 'УС Усть-Каменогорск', 'УП Костанай', 'УП Нур-Султан', 'УП Шымкент', 'УП Актобе', 'УП Кызылорда', 'УП Петропавловск', 'УП Павлодар', 'УП медицинского страхования', 'АО СК НОМАД ИНШУРАНС', 'Управление регионального страхования', 'ф-л Актау', 'ф-л Актау', 'ф-л Актобе', 'ф-л Алматы', 'ф-л Атырау', 'ф-л Караганда', 'ф-л Кокшетау', 'ф-л Костанай', 'ф-л Кызылорда', 'ф-л Нур-Султан', 'ф-л Павлодар', 'ф-л Петропавловск', 'ф-л Семей', 'ф-л Талдыкорган', 'ф-л Талдыкорган', 'ф-л Тараз', 'ф-л Уральск', 'ф-л Усть-Каменогорск', 'ф-л Шымкент', 'АО СК НОМАД ИНШУРАНС', 'УКП', 'УКП', 'УКП', 'УКП',]

        first += ['Центр страхования №4  УКП АО СК "НОМАД ИНШУРАНС"','Центр страхования №2  УКП АО СК "НОМАД ИНШУРАНС"', 'Центр страхования №2  УКП АО СК НОМАД ИНШУРАНС', 'Центр страхования №4  УКП АО СК НОМАД ИНШУРАНС', 'Упр. продаж "Уральск"  АО СК  "Номад Иншуранс"']
        second += ['УКП','УКП','УКП', 'УКП', 'УП Уральск']
        data2 = pd.ExcelFile(file)
        datas = pd.read_excel(data2, None)
        res = []
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        for key, value in datas.items():
            data = value
            for i in range(len(first)):
                data = data.replace(first[i], second[i])

            data.to_excel(writer, key)

        writer.save()
        output.seek(0)
        response = HttpResponse(output,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % 'Download'
        return response
    context = {   
    }
    return render(request, "file_changer.html", context)
def upload_cards(request):
    if 'file' in request.FILES:
        x=float('nan')
        school = School.objects.get(id=155)
        file = request.FILES['file']
        data2 = pd.ExcelFile(file)
        datas = pd.read_excel(data2, None)
        res = []
        column = CRMColumn.objects.get(title='Заявка на сайте')
        for key, value in datas.items():
            data = value
            for index, row in data.iterrows():
                name = ''
                parents = ''
                birthday = None
                phone = ''
                mail = ''
                comment = ''
                i = 0
                for aaa in row:
                    if i == 0:
                        name = aaa
                    elif i == 1:
                        phone = aaa
                    elif i == 2:
                        comment = aaa
                    i += 1
                xls_create_card(None,name,'', None,phone,'',column,school, comment)
    context = {   
    }
    return render(request, "upload_cards.html", context)

def xls_create_card(profile,name,parents,birthday,phone,mail,column,school, comment):
    card = school.crm_cards.create(
        author_profile=profile,
        name = name,
        parents = parents,
        birthday = birthday,
        phone = phone,
        mail = mail,
        comments = comment,
        column = column,
        saved = False,
        card_user = None,
    )
    card.save()
    hist = CRMCardHistory.objects.create(
        action_author = profile,
        card = card,
        edit = '***Создание карточки***',
        )
    hist.save()
    return card

def moderator_run_code(request):
    profile = get_profile(request)
    if is_profi(profile, 'Moderator') == False:
        return JsonResponse({'de5a':'e99w9'})
    if request.GET.get('secret') != 'IMJINfv5rf56ref658f7wef':
        return JsonResponse({'d8w':'11wd'})
    print('moderator_run_code')
    create_columns()
    print('moderator_end_code')
    return render(request, "moder_code.html", {})

def create_columns():
    for profile in Profile.objects.all():
        profile.videohints = [1, 1, 1, 1, 1, 1, 1]
        profile.save()

def searching_subjects(request):
    profile = get_profile(request)
    if is_profi(profile, 'Moderator') == False:
        return JsonResponse({'fuck_off':'sucker'})
    if request.GET.get('secret') != 'IMJINfv5rf56ref658f7wef':
        return JsonResponse({'fuck_off':'sucker'})
    data = {
        "res":res,
    }
    return JsonResponse(data)

def another_hint(request):
    profile = Profile.objects.get(user = request.user)
    hint_type = int(request.GET.get('hint_type'))
    if request.GET.get('dir') == 'next':
        profile.hint_numbers[hint_type] += 1
    elif request.GET.get('dir') == 'prev':
        profile.hint_numbers[hint_type] -= 1
    else:
        profile.hint_numbers[hint_type] = 100
    profile.save()
    data = {
    }
    return JsonResponse(data)

def update_hint(request):
    profile = Profile.objects.get(user = request.user)
    profile.hint_numbers = [0, 1, 1, 1, 1, 1, 1]
    profile.videohints = [1, 1, 1, 1, 1, 1, 1]
    profile.save()
    data = {
    }
    return JsonResponse(data)

def video_done(request):
    profile = Profile.objects.get(user = request.user)
    if len(profile.videohints) == 0:
        profile.videohints = [0, 0, 0, 0, 0, 0, 0]
    hint_type = int(request.GET.get('hint_type'))
    profile.videohints[hint_type] = 1
    profile.save()
    data = {
    }
    return JsonResponse(data)

def cloudpayments_pay(request):
    print('cloudpayments_pay')
    if check_cloudpayments_hash(request):
        print('get_hash')
        profile_id = request.GET.get('AccountId')
        profile = Profile.objects.get(id = int(profile_id))
        school = profile.schools.first()
        print(request.GET)
        data = request.GET.get('Data').replace('{','').replace('}','').split(',')
        months = int(data[0].split(':')[1])
        managers_num = int(data[1].split(':')[1])
        transaction_id = request.GET.get('TransactionId')
        name = profile.first_name
        if request.GET.get('Name'):
            name = request.GET.get('Name')
        phone = profile.phone
        amount = float(request.GET.get('Amount'))
        currency = request.GET.get('Currency')
        res = tarif_change(profile, school, months, managers_num, name, phone, transaction_id, amount,currency)
        print(res)
    data = {
        'code':0,
    }
    return JsonResponse(data)

def cloudpayments_fail(request):
    request.GET.get('dir')
    data = {
        'code':0
    }
    return JsonResponse(data)

def cloudpayments_refund(request):
    request.GET.get('dir')
    data = {
        'code':0
    }
    return JsonResponse(data)

def check_cloudpayments_hash(request):
    decoded = request.headers['Content-HMAC']
    decoded = bytes(decoded, 'utf-8')
    url = request.META['QUERY_STRING']
    message = bytes(url, 'utf-8')
    secret = bytes(cloudpayments_secretkey, 'utf-8')
    decoded2 = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
    if decoded == decoded2:
        if request.GET.get('Status') == 'Completed':
            return True
    return False

def get_cloudpayments_data(request):
    profile = Profile.objects.get(user = request.user)
    publicId = cloudpayments_id
    invoiceId = '1'
    accountId = profile.id
    data = {
        'publicId':publicId,
        'invoiceId':invoiceId,
        'accountId':accountId,
    }
    return JsonResponse(data)

def wazzup24(request):
    print(request.headers['Authorization'])
    print(request.POST)
    data = {
    }
    return JsonResponse(data)
