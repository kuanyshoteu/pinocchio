from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import RedirectView
from datetime import timedelta

from .forms import SchoolForm
from .models import *
from subjects.models import *
from squads.models import Squad,PaymentHistory,SquadHistory
from squads.views import remove_student_from_squad, add_student_to_squad, prepare_mail
from papers.models import *
from library.models import Folder
from accounts.models import Profile,CRMCardHistory
from accounts.forms import *
from accounts.views import add_money
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.contrib.auth.models import User
import os
from constants import *

def school_rating(request):
    profile = get_profile(request)
    if len(profile.schools.all()) == 0:
        context = {
            "profile":profile,
            "instance": None,
            "squads":[],
            "subject_categories":[],
            "subject_ages":[],
            "all_students":[],
            'is_trener':is_profi(profile, 'Teacher'),
            "is_manager":is_profi(profile, 'Manager'),
            "is_director":is_profi(profile, 'Director'),
            "is_moderator":is_profi(profile, 'Moderator'),
        }
        return render(request, "school/school_rating.html", context)
    else:
        school = is_moderator_school(request, profile)
        context = {
            "profile":profile,
            "instance": profile.schools.first(),
            "squads":school.groups.all(),
            "subject_categories":school.school_subject_categories.all(),
            "subject_ages":school.school_subject_ages.all(),
            "all_students":school.people.filter(),
            'is_trener':is_profi(profile, 'Teacher'),
            "is_manager":is_profi(profile, 'Manager'),
            "is_director":is_profi(profile, 'Director'),
            "is_moderator":is_profi(profile, 'Moderator'),
            "school_money":school.money,
            "school_crnt":school,
        }
        return render(request, "school/school_rating.html", context)

def school_payments(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)   
    context = {
        "profile":profile,
        "instance": school,
        "squads":school.groups.all(),
        "payments":True,
        "subject_categories":school.school_subject_categories.all(),
        "subject_ages":school.school_subject_ages.all(),
        "all_students":school.people.filter(is_student=True),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
    }
    return render(request, "school/school_payments.html", context)

def school_schedule(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    time_periods = school.time_periods.all()
    context = {
        "profile":profile,
        "instance": school,
        "subject_categories":school.school_subject_categories.all(),
        "ages":school.school_subject_ages.all(),
        "offices":school.school_offices.all(),
        "courses":school.school_subjects.all(),
        "teachers":all_teachers(school),        
        'days':Day.objects.all(),
        'time_periods':time_periods,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
        'constant_times':get_times(school.schedule_interval),
        'interval':school.schedule_interval,
        'days':get_days(),
        'height':28*15*int(60/school.schedule_interval)+25,
    }
    return render(request, "school/schedule.html", context)

def school_landing(request, school_id=None):
    school = School.objects.get(id=school_id)
    profile = None
    is_trener = False
    is_manager = False
    is_director = False
    school_money = 0
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
        is_trener = is_profi(profile, 'Teacher')
        is_manager = is_profi(profile, 'Manager')
        is_director = is_profi(profile, 'Director')
        if len(profile.schools.all()):
            school_money = profile.schools.first().money
    count = 0
    posts = []
    for post in school.school_posts.all():
        if post.image:
            posts.append(post)
            count += 1
        if count == 4:
            break
    context = {
        "profile":profile,
        "school": school,
        "all_teachers":all_teachers(school),
        'is_trener':is_trener,
        "is_manager":is_manager,
        "is_director":is_director,
        "school_money":school_money,
        "school_crnt":school,
        "posts":posts,
        "five":[1,2,3,4,5],
        "landing":True,
        "social_networks":get_social_networks(school),
    }
    return render(request, "school/landing.html", context)

def school_info(request):
    profile = get_profile(request)
    only_directors(profile)
    school = is_moderator_school(request, profile)
    if is_profi(profile, 'Director'):
        money = school.money
    if request.POST: 
        if len(request.FILES) > 0:
            if 'school_banner' in request.FILES:
                file = request.FILES['school_banner']
                banner = school.banners.create()
                banner.image_banner = file
                banner.save()
                return redirect("schools:info")
    manager_prof = Profession.objects.get(title='Manager')
    managers = school.people.filter(profession=manager_prof)
    weekago = timezone.now().date() - timedelta(7)    
    voronka = []
    voronka2 = []
    number = 0
    all_cards = school.crm_cards.filter(timestamp__gt=weekago)
    number_of_all = len(all_cards)
    if number_of_all > 0:
        for column in school.crm_columns.all().order_by('-id'):
            if column.id != 6:
                x = len(all_cards.filter(column=column))
                number += x
                voronka.append([column.title, number, round((number/number_of_all)*100,2)])
                voronka2.append([column.title, number, round((number/number_of_all)*100,2)])
    voronka = reversed(voronka)
    voronka2 = reversed(voronka2)
    worktime1 = ''
    worktime2 = ''
    if '-' in school.worktime:
        worktime1 = school.worktime.split('-')[0]
        worktime2 = school.worktime.split('-')[1]
    context = {
        "profile":profile,
        "instance": school,
        "squads":school.groups.all(),
        "main_school":True,
        "subjects":school.school_subjects.all(),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
        "today":timezone.now().date().strftime('%Y-%m-%d'),
        "weekago":(timezone.now().date() - timedelta(7)).strftime('%Y-%m-%d'),
        "managers":managers,
        "voronka_array":voronka,
        "voronka2":voronka2,
        "worktime1":worktime1,
        "worktime2":worktime2,
        "social_networks":get_social_networks(school),
    }
    return render(request, "school/info.html", context)
def get_social_networks(school):
    social_networks = []
    for i in range(0, min(len(school.social_network_links)), len(school.social_networks)):
        social_networks.append([school.social_networks[i], school.social_network_links[i]])
    return social_networks

def school_salaries(request):
    profile = get_profile(request)
    only_directors(profile)
    school = is_moderator_school(request, profile)
    context = {
        "profile":profile,
        "instance": school,
        "salaries":True,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
    }
    return render(request, "school/salaries.html", context)

def school_crm(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    time_periods = school.time_periods.all()
    managers = None
    is_director = is_profi(profile, 'Director')
    theprofile = profile
    if is_profi(profile, 'Moderator'):
        theprofile = school.people.first()
        print(theprofile.first_name)
    if is_director:
        manager_prof = Profession.objects.get(title='Manager')
        managers = school.people.filter(profession=manager_prof)
    context = {
        "theprofile":theprofile,
        "profile":profile,
        "instance": school,
        "columns":school.crm_columns.all(),
        "subject_categories":school.school_subject_categories.all(),
        "ages":SubjectAge.objects.all(),
        "offices":school.school_offices.all(),
        "courses":school.school_subjects.all(),
        "teachers":all_teachers(school),
        'time_periods':time_periods,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "is_director":is_director,
        'managers':managers,
        "school_money":school.money,
        "school_crnt":school,
        "all":False,
        'constant_times':get_times(school.schedule_interval),
        'interval':school.schedule_interval,
        'days':get_days(),
        'crmdays':Day.objects.all(),
    }
    return render(request, "school/crm.html", context)

def school_crm_all(request):
    profile = get_profile(request)
    only_directors(profile)
    school = is_moderator_school(request, profile)
    time_periods = school.time_periods.all()
    managers = None
    is_director = is_profi(profile, 'Director')
    if is_director:
        manager_prof = Profession.objects.get(title='Manager')
        managers = school.people.filter(profession=manager_prof)
    context = {
        "profile":profile,
        "instance": school,
        "columns":school.crm_columns.all(),
        "subject_categories":school.school_subject_categories.all(),
        "ages":school.school_subject_ages.all(),
        "offices":school.school_offices.all(),
        'days':Day.objects.all(),
        'time_periods':time_periods,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_director,
        "is_moderator":is_profi(profile, 'Moderator'),
        'managers':managers,
        "school_money":school.money,
        "school_crnt":school,
        "all":True,
        'constant_times':get_times(school.schedule_interval),
        'interval':school.schedule_interval,
        'days':get_days(),
    }
    return render(request, "school/crm.html", context)

def school_students(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)    
    context = {
        "profile":profile,
        "instance": profile.schools.first(),
        "all_students":school.people.filter(),
        "students":"students",
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
    }
    return render(request, "school/all_students.html", context)

def school_requests(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    context = {
        "profile":profile,
        "instance": profile.schools.first(),
        "all_students":school.zaiavkas.all(),
        "requests":"requests",
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
    }
    return render(request, "school/all_students.html", context)

def school_recalls(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    context = {
        "profile":profile,
        "instance": school,
        "all_students":school.people.filter(),
        "recalls":"recalls",
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
    }
    return render(request, "school/all_students.html", context)

def school_courses(request):
    profile = get_profile(request)
    only_managers(profile)
    context = {
        "profile":profile,
        "instance": profile.schools.first(),
        "courses":"courses",
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
    }
    return render(request, "school/all_courses.html", context)

def school_list(request):
    profile = get_profile(request)
    context = {
        "profile": profile,
        "schools":School.objects.all(),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_crnt":school,
    }
    return render(request, "schools/school_list.html", context)

def subject_create(request): ### Если нет предмета, то отправить письмо Адилю
    manager_profile = Profile.objects.get(user = request.user.id)
    only_managers(manager_profile)
    create_url = ''
    delete_url = ''
    if request.GET.get('id') and request.GET.get('title'):
        title = request.GET.get('title')
        school = is_moderator_school(request, manager_profile)
        if school.school_subject_categories.filter(title = title):
            return JsonResponse({'taken_name':True})
        if request.GET.get('id') == '_new':
            qs = SubjectCategory.objects.filter(title=title)
            if len(qs) > 0:
                school.school_subject_categories.add(qs[0])
                subject = qs[0]
            else:
                subject = school.school_subject_categories.create(title=title)
            school.hashtags.get_or_create(title = title.replace(' ', '_'))
        else:
            subject = school.school_subject_categories.get(id=int(request.GET.get('id')))
            hashtag = school.hashtags.filter(title = subject.title.replace(' ', '_'))
            if len(hashtag) > 0:
                hashtag = hashtag[0]
                hashtag.title = title.replace(' ', '_')
                hashtag.save()
            else:
                school.hashtags.create(title=title.replace(' ', '_'))
            subject.title = title
        subject.save()
        create_url = subject.create_url()
        delete_url = subject.delete_url()
    data = {
        'taken_name':False,
        'create_url':create_url,
        'delete_url':delete_url,
        'idd':subject.id,
    }
    return JsonResponse(data)

def subject_delete(request):
    profile = Profile.objects.get(user = request.user.id)
    school = is_moderator_school(request, profile)
    only_managers(profile)
    subject = school.school_subject_categories.get(id=int(request.GET.get('id')))
    hashtag = school.hashtags.filter(title = subject.title.replace(' ', '_'))
    if len(hashtag) > 0:
        hashtag.delete()
    school.school_subject_categories.remove(subject)
    data = {
    }
    return JsonResponse(data)

def age_create(request):
    manager_profile = Profile.objects.get(user = request.user.id)
    only_managers(manager_profile)
    create_url = ''
    delete_url = ''
    if request.GET.get('id') and request.GET.get('title'):
        title = request.GET.get('title')
        school = is_moderator_school(request, manager_profile)
        if school.school_subject_ages.filter(title = title):
            return JsonResponse({'taken_name':True})
        if request.GET.get('id') == '_new':
            qs = SubjectAge.objects.filter(title=title)
            if len(qs) > 0:
                school.school_subject_ages.add(qs[0])
                age = qs[0]
            else:
                age = school.school_subject_ages.create(title=title)
            school.hashtags.create(title = title.replace(' ', '_'))
        else:
            age = school.school_subject_ages.get(id=int(request.GET.get('id')))
            hashtag = school.hashtags.filter(title = age.title.replace(' ', '_'))
            if len(hashtag) > 0:
                hashtag.title = title.replace(' ', '_')
                hashtag.save()
            else:
                school.hashtags.create(title=title.replace(' ', '_'))
            age.title = title
        age.save()
        create_url = age.create_url()
        delete_url = age.delete_url()
    data = {
        'taken_name':False,
        'create_url':create_url,
        'delete_url':delete_url,
        'idd':age.id,
    }
    return JsonResponse(data)

def age_delete(request):
    profile = Profile.objects.get(user = request.user.id)
    school = is_moderator_school(request, profile)
    only_managers(profile)
    age = school.school_subject_ages.get(id=int(request.GET.get('id')))
    hashtag = school.hashtags.filter(title = age.title.replace(' ', '_'))
    if len(hashtag) > 0:
        hashtag.delete()
    age.delete()
    data = {
    }
    return JsonResponse(data)

def level_create(request):
    manager_profile = Profile.objects.get(user = request.user.id)
    only_managers(manager_profile)
    create_url = ''
    delete_url = ''
    if request.GET.get('id') and request.GET.get('title'):
        title = request.GET.get('title')
        school = is_moderator_school(request, manager_profile)
        if school.school_subject_levels.filter(title = title):
            return JsonResponse({'taken_name':True})
        if request.GET.get('id') == '_new':
            qs = SubjectLevel.objects.filter(title=title)
            if len(qs) > 0:
                school.school_subject_levels.add(qs[0])
                level = qs[0]
            else:
                level = school.school_subject_levels.create(title=title)
            school.hashtags.create(title = title.replace(' ', '_'))
        else:
            level = school.school_subject_levels.get(id=int(request.GET.get('id')))
            hashtag = school.hashtags.filter(title = level.title.replace(' ', '_'))
            if len(hashtag) > 0:
                hashtag.title = title.replace(' ', '_')
                hashtag.save()
            else:
                school.hashtags.create(title=title.replace(' ', '_'))
            level.title = title
        level.save()
        create_url = level.create_url()
        delete_url = level.delete_url()
    data = {
        'taken_name':False,
        'create_url':create_url,
        'delete_url':delete_url,
        'idd':level.id,
    }
    return JsonResponse(data)

def level_delete(request):
    profile = Profile.objects.get(user = request.user.id)
    school = is_moderator_school(request, profile)
    only_managers(profile)
    level = school.school_subject_levels.get(id=int(request.GET.get('id')))
    hashtag = school.hashtags.filter(title = level.title.replace(' ', '_'))
    if len(hashtag) > 0:
        hashtag.delete()
    school.school_subject_levels.remove(level)
    data = {
    }
    return JsonResponse(data)

def office_create(request):
    manager_profile = Profile.objects.get(user = request.user.id)
    only_managers(manager_profile)
    create_url = ''
    delete_url = ''
    if request.GET.get('id') and request.GET.get('title'):
        title = request.GET.get('title')
        school = is_moderator_school(request, manager_profile)
        if len(school.school_offices.filter(title = title)) > 0:
            return JsonResponse({'taken_name':True})
        if request.GET.get('id') == '_new':
            office = school.school_offices.create(title=title)
            school.offices += 1
            school.save()
            school.hashtags.create(title = title.replace(' ', '_'))
        else:
            office = school.school_offices.get(id=int(request.GET.get('id')))
            hashtag = school.hashtags.filter(title = office.title.replace(' ', '_'))
            if len(hashtag) > 0:
                hashtag = hashtag[0]
                hashtag.title = title.replace(' ', '_')
                hashtag.save()
            else:
                school.hashtags.create(title=title.replace(' ', '_'))
            office.title = title
        office.save()
        create_url = office.create_url()
        delete_url = office.delete_url()
    data = {
        'taken_name':False,
        'create_url':create_url,
        'delete_url':delete_url,
        'idd':office.id,
    }
    return JsonResponse(data)

def office_delete(request):
    profile = Profile.objects.get(user = request.user.id)
    school = is_moderator_school(request, profile)
    only_managers(profile)
    office = school.school_offices.get(id=int(request.GET.get('id')))
    hashtag = school.hashtags.filter(title = office.title.replace(' ', '_'))
    if len(hashtag) > 0:
        hashtag.delete()
    for cabinet in office.cabinets.all():
        cabinet.delete()
    office.delete()
    school.offices -= 1
    school.save()
    data = {
    }
    return JsonResponse(data)
    
def create_cabinet(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    if request.GET.get('title') != '':
        school = is_moderator_school(request, profile)
        office = school.school_offices.get(id=int(request.GET.get('id')))
        office.cabinets.create(
            school=school,
            title=request.GET.get('title'),
            capacity=int(request.GET.get('capacity')),
            )
    data = {
    }
    return JsonResponse(data)

def create_social(request):
    manager_profile = Profile.objects.get(user = request.user.id)
    only_managers(manager_profile)
    create_url = ''
    delete_url = ''
    if request.GET.get('id') and request.GET.get('link'):
        link = request.GET.get('link')
        school = is_moderator_school(request, manager_profile)
        social_name = ''
        if 'instagram' in link:
            social_name = 'instagram'
        elif 'facebook' in link:
            social_name = 'facebook'
        elif 'vk.com' in link:
            social_name = 'Вконтакте'
        else:
            social_name = 'Страница' + str(len(school.social_networks)+1)
        if [link, social_name] in school.social_networks:
            return JsonResponse({'taken_name':True})
        if request.GET.get('id') == '_new':
            school.social_networks.append(link)
            school.social_network_links.append(social_name)
        else:
            school.social_networks[int(request.GET.get('id'))-1] = link
            school.social_network_links[int(request.GET.get('id'))-1] = social_name
        school.save()
        create_url = school.create_social_url()
        delete_url = school.delete_social_url()
    data = {
        'create_url':create_url,
        'delete_url':delete_url,
        'social_name':social_name,
    }
    return JsonResponse(data)

def delete_social(request):
    profile = Profile.objects.get(user = request.user.id)
    school = is_moderator_school(request, profile)
    only_managers(profile)
    index = int(request.GET.get('id'))
    a = school.social_networks
    school.social_networks = a[:index-1] + a[index :]
    school.save()
    data = {
    }
    return JsonResponse(data)

def timep_create(request):
    manager_profile = Profile.objects.get(user = request.user.id)
    only_managers(manager_profile)
    create_url = ''
    delete_url = ''
    if request.GET.get('id') and request.GET.get('start') and request.GET.get('end'):
        start = request.GET.get('start')
        end = request.GET.get('end')
        school = is_moderator_school(request, manager_profile)
        if school.time_periods.filter(start = start, end=end):
            return JsonResponse({'taken_name':True})
        if request.GET.get('id') == '_new':
            timep = school.time_periods.create(start = start, end=end)
        else:
            timep = school.time_periods.get(id=int(request.GET.get('id')))
            timep.start = start
            timep.end = end
        if len(timep.time_cell.all()) == 0:
            for day in Day.objects.all():
                timep.time_cell.create(day=day, school=school)
        timep.save()
        create_url = timep.create_url()
        delete_url = timep.delete_url()
        school_people = school.people.all()
        timep.people.add(*school_people)
    data = {
        'taken_name':False,
        'create_url':create_url,
        'delete_url':delete_url,
        'idd':timep.id,
    }
    return JsonResponse(data)

def timep_delete(request):
    profile = Profile.objects.get(user = request.user.id)
    school = is_moderator_school(request, profile)
    only_managers(profile)
    timep = school.time_periods.get(id=int(request.GET.get('id')))
    timep.delete()
    data = {
    }
    return JsonResponse(data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse

def save_card_as_user(request):
    manager_profile = Profile.objects.get(user = request.user.id)
    only_managers(manager_profile)
    school = is_moderator_school(request, manager_profile)
    password = ''
    add = True
    problems = 'ok'
    ok_mail = False
    if request.GET.get('id') and request.GET.get('squad_id'):
        card = school.crm_cards.get(id = int(request.GET.get('id')))
        squad_id = int(request.GET.get('squad_id'))
        if squad_id > 0:
            squad = Squad.objects.get(id=squad_id)
            if card.saved == False:
                password = random_password()
                found = False
                if card.mail != '' and len(Profile.objects.filter(mail=card.mail)) > 0:
                    profile = Profile.objects.filter(mail=card.mail)[0]
                    found = True
                elif len(Profile.objects.filter(phone=card.phone)) > 0:
                    profile = Profile.objects.filter(phone=card.phone)[0]
                    found = True
                if found:
                    ok_mail = prepare_mail(card.name, card.phone, card.mail, squad, None, True)
                else:
                    ok_mail = prepare_mail(card.name, card.phone, card.mail, squad, password, True)
                hist = CRMCardHistory.objects.create(
                    action_author = manager_profile,
                    card = card,
                    edit = '*** Регистрация в ' + squad.title + ' ***',
                    )
                if found == False:
                    new_id = User.objects.order_by("id").last().id + 1
                    user = User.objects.create(username='user' + str(new_id))
                    user.set_password(password)
                    user.save()
                    profile = Profile.objects.get(user = user)
                    profile.first_name = card.name
                    profile.phone = card.phone
                    profile.mail = card.mail
                    profile.save()
                card.card_user = profile
                card.author_profile = manager_profile
                card.timestamp = timezone.now()
                card.last_groups = squad_id
                card.saved = True
                card.save()
                profile.schools.add(school)
                skill = Skill.objects.create()
                profile.skill = skill
                profile.save()
                skill.confirmation_time = timezone.now()
                skill.confirmed = True
                skill.save()
                add_student_to_squad(profile, squad)
            else:
                profile = card.card_user
                card.author_profile = manager_profile
                card.save()
                # if squad_id == card.last_groups and card.timestamp + timedelta(minutes = 1) > timezone.now():
                #     return JsonResponse({'stop':True, 'problems':'ok'})
                if profile in squad.students.all():
                    add = False
                    remove_student_from_squad(profile, squad)
                    ok_mail = True
                else:
                    problems = add_student_to_squad(profile, squad)
                    ok_mail = prepare_mail(profile.first_name, card.phone, card.mail, squad, None, True)
                profile.schools.add(school)
                card.last_groups = squad_id
                card.timestamp = timezone.now()
                card.save()
                hist = CRMCardHistory.objects.create(
                    action_author = manager_profile,
                    card = card,
                    edit = '*** Регистрация в ' + squad.title + ' ***',
                    )
            if request.GET.get('predoplata'):
                add_money(card.card_user, school, squad, card, int(request.GET.get('predoplata')), manager_profile)
    data = {
        'password':password,
        'add':add,
        'ok_mail':ok_mail,
        'problems':problems,
    }
    return JsonResponse(data)

def predoplata(request):
    manager_profile = Profile.objects.get(user = request.user.id)
    only_managers(manager_profile)
    school = is_moderator_school(request, manager_profile)
    if request.GET.get('id') and request.GET.get('predoplata'):
        card = school.crm_cards.get(id = int(request.GET.get('id')))
        profile = card.card_user
        if request.GET.get('predoplata'):
            card.premoney += int(request.GET.get('predoplata'))
            card.save()
            name = card.name
            change_school_money(school, int(request.GET.get('predoplata')), 'student_payment', name)
            school.save()
    data = {
    }
    return JsonResponse(data)

def crm_option(request):
    profile = Profile.objects.get(user = request.user.id)
    if request.GET.get('object_id') and request.GET.get('option'):
        skill = profile.skill
        if request.GET.get('option') == 'subject':
            if int(request.GET.get('object_id')) == -1:
                skill.crm_subject = None
            else:
                subject = SubjectCategory.objects.get(id = int(request.GET.get('object_id')))
                skill.crm_subject = subject
        if request.GET.get('option') == 'age':
            if int(request.GET.get('object_id')) == -1:
                skill.crm_age = None
            else:
                age = SubjectAge.objects.get(id = int(request.GET.get('object_id')))
                skill.crm_age = age
        if request.GET.get('option') == 'office':
            if int(request.GET.get('object_id')) == -1:
                skill.crm_office = None
            else:
                office = Office.objects.get(id = int(request.GET.get('object_id')))
                skill.crm_office = office
        if request.GET.get('option') == 'course':
            skill.filter_course_connect.clear()
            if int(request.GET.get('object_id')) != -1:
                course = Subject.objects.get(id = int(request.GET.get('object_id')))
                skill.filter_course_connect.add(course)
        if request.GET.get('option') == 'teacher':
            skill.filter_teacher.clear()
            if int(request.GET.get('object_id')) != -1:
                teacher = Profile.objects.get(id = int(request.GET.get('object_id')))
                skill.filter_teacher.add(teacher)
        if request.GET.get('option') == 'group':
            profile.rating_squad_choice.clear()
            if int(request.GET.get('object_id')) != -1:
                squad = Squad.objects.get(id = int(request.GET.get('object_id')))
                profile.rating_squad_choice.add(squad)
        skill.save()
    data = {
    }
    return JsonResponse(data)
def crm_option2(request):
    profile = Profile.objects.get(user = request.user.id)
    if request.GET.get('object_id') and request.GET.get('option'):
        skill = profile.skill
        if request.GET.get('option') == 'subject':
            if int(request.GET.get('object_id')) == -1:
                skill.crm_subject2 = None
            else:
                subject = SubjectCategory.objects.get(id = int(request.GET.get('object_id')))
                skill.crm_subject2 = subject
        if request.GET.get('option') == 'age':
            if int(request.GET.get('object_id')) == -1:
                skill.crm_age2 = None
            else:
                age = SubjectAge.objects.get(id = int(request.GET.get('object_id')))
                skill.crm_age2 = age
        if request.GET.get('option') == 'office':
            if int(request.GET.get('object_id')) == -1:
                skill.crm_office2 = None
            else:
                office = Office.objects.get(id = int(request.GET.get('object_id')))
                skill.crm_office2 = office
        if request.GET.get('option') == 'group':
            profile.rating_squad_choice.clear()
            if int(request.GET.get('object_id')) != -1:
                squad = Squad.objects.get(id = int(request.GET.get('object_id')))
                profile.rating_squad_choice.add(squad)
        skill.save()
    data = {
    }
    return JsonResponse(data)

def move_card(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    if request.GET.get('card_id') and request.GET.get('column_id'):
        school = is_moderator_school(request, profile)
        column = school.crm_columns.get(id = int(request.GET.get('column_id')))
        card = school.crm_cards.get(id = int(request.GET.get('card_id')))
        card.timestamp = timezone.now()
        CRMCardHistory.objects.create(
            action_author = profile,
            card = card,
            oldcolumn = card.column.title,
            newcolumn = column.title,
            )
        card.column = column
        card.save()
    data = {
    }
    return JsonResponse(data)

def edit_card(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    if request.GET.get('id') and request.GET.get('name') and request.GET.get('phone'):
        school = is_moderator_school(request, profile)
        card = school.crm_cards.get(id = int(request.GET.get('id')))
        edit = '***Редактирование*** '
        if card.name != request.GET.get('name'):
            edit = edit + "Имя: " + card.name + " -> " + request.GET.get('name') + "; "
        if card.phone != request.GET.get('phone'):
            edit = edit + "Номер: " + card.phone + " -> " + request.GET.get('phone') + "; "
        if card.extra_phone != request.GET.get('extra_phone'):
            edit = edit + "Дополнительный номер: " + card.extra_phone + " -> " + request.GET.get('extra_phone') + "; "
        if card.mail != request.GET.get('mail'):
            edit = edit + "Почта: " + card.mail + " -> " + request.GET.get('mail') + "; "
        if card.comments != request.GET.get('comment'):
            edit = edit + "Коммент: " + card.comments + " -> " + request.GET.get('comment') + "; "
        card.name = request.GET.get('name')
        card.phone = request.GET.get('phone')
        card.extra_phone = request.GET.get('extra_phone')
        card.mail = request.GET.get('mail')
        card.comments = request.GET.get('comment')
        crnt_tag = ''
        wright = False
        hashtags = school.hashtags.all()
        for l in request.GET.get('comment')+' ':
            if wright:
                crnt_tag += l
            if l == '!':
                wright = True
            elif l == ' ':
                if wright:
                    crnt_tag = crnt_tag.replace(' ','')
                    founttag = hashtags.filter(title=crnt_tag)
                    if len(founttag) > 0:
                        card.hashtags.add(founttag[0])
                    else:
                        founttag = school.hashtags.create(title=crnt_tag)
                        card.hashtags.add(founttag)                        
                wright = False
                crnt_tag = ''
        card.save()
        print(card)
        CRMCardHistory.objects.create(
            action_author = profile,
            card = card,
            edit = edit,
            )
    data = {
    }
    return JsonResponse(data)

def open_card(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    res = []
    if request.GET.get('id'):
        school = is_moderator_school(request, profile)
        card = school.crm_cards.get(id = int(request.GET.get('id')))
        for history in card.history.all():
            res.append([history.action_author.first_name, history.action_author.get_absolute_url(), history.timestamp.strftime('%d.%m.%Y %H:%M') ,history.oldcolumn,history.newcolumn, history.edit])
    data = {
        'res':res,
    }
    return JsonResponse(data)

def card_called(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    if request.GET.get('id'):
        school = is_moderator_school(request, profile)
        card = school.crm_cards.get(id = int(request.GET.get('id')))
        skill = profile.skill
        card.action = request.GET.get('action')
        if card.was_called:
            card.was_called = False
            skill.need_actions += 1
        else:
            card.was_called = True
            skill.need_actions -= 1
        skill.save()
        card.save()
    data = {
        'is_called':card.was_called
    }
    return JsonResponse(data)

def add_card(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    if request.GET.get('id') and request.GET.get('name') and request.GET.get('phone'):
        school = is_moderator_school(request, profile)
        found = False
        student = None
        if len(request.GET.get('mail')) > 0:
            if len(Profile.objects.filter(mail=request.GET.get('mail'))) > 0:
                found = True
                student = Profile.objects.filter(mail=request.GET.get('mail'))[0]
        elif len(Profile.objects.filter(phone=request.GET.get('phone'))) > 0:
            found = True
            student = Profile.objects.filter(phone=request.GET.get('phone'))[0]            
        if len(school.crm_cards.filter(phone=request.GET.get('phone'))) > 0:
            found = True
            student = False
        elif len(request.GET.get('mail')) > 0:
            if len(school.crm_cards.filter(mail=request.GET.get('mail'))) > 0:
                found = True
                student = False
        if found:
            if student:
                if school in student.schools.all():
                    return JsonResponse({"already_registered":True})
            else:
                return JsonResponse({"already_registered":True})
        column = school.crm_columns.get(id = int(request.GET.get('id')))
        saved = False
        if found:
            saved = True
        card = school.crm_cards.create(
            author_profile=profile,
            name = request.GET.get('name'),
            phone = request.GET.get('phone'),
            mail = request.GET.get('mail'),
            comments = request.GET.get('comment'),
            column = column,
            school = school,
            saved = saved,
            card_user = student,
        )
        card.save()
        hist = CRMCardHistory.objects.create(
            action_author = profile,
            card = card,
            edit = '***Создание карточки***',
            )
        hist.save()
        skill = profile.skill
        skill.need_actions += 1
        skill.save()
    data = {
        "card_id":card.id,
        "card_name":card.name,
        "card_date":card.timestamp.date().strftime('%d.%m.%Y'),
        "card_phone":card.phone,
        "card_mail":card.mail,
        "card_comment":card.comments,
        "is_saved":card.saved,
        "author_profile":profile.first_name,
        "author_url":profile.get_absolute_url(),
        "call_helper":card.call_helper(),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
    }
    return JsonResponse(data)

def make_zaiavka(request, school_id):
    profile = Profile.objects.get(user = request.user.id)
    school = School.objects.get(id=school_id)
    column = school.crm_columns.first()
    course = 'Заявка с рекламной страницы: ' + timezone.now().strftime('%d %m %Y %H:%M')
    if request.GET.get('course') != '':
        course = '. Хочет на курс ' + request.GET.get('course')
    card = school.crm_cards.create(
        name = profile.first_name,
        phone = profile.phone,
        mail = profile.mail,
        comments = course,
        column = column,
        school = school,
    )
    card.save()
    hist = CRMCardHistory.objects.create(
        card = card,
        edit = '***Создание карточки***',
        )
    hist.save()
    text = "Новая заявка в СРМ"
    manager_prof = Profession.objects.get(title='Manager')
    for manager in school.workers.filter(profession=manager_prof):
        Notification.objects.create(
            text = text,
            author_profile = manager,
            school = school,
            itstype = 'crm',
            url = '',
            image_url = 'crm'
        )
    data = {
    }
    return JsonResponse(data)

def change_manager(request):
    profile = Profile.objects.get(user = request.user.id)
    only_directors(profile)
    if request.GET.get('manager') and request.GET.get('card'):
        school = is_moderator_school(request, profile)
        card = school.crm_cards.get(id = int(request.GET.get('card')))
        if request.GET.get('manager') == '-1':
            card.author_profile = None
        else:
            manager = Profile.objects.get(id=int(request.GET.get('manager')))
            card.author_profile = manager
            text = 'У вас новый клиент в CRM'
            Notification.objects.create(
                text = text,
                author_profile = manager,
                school = is_moderator_school(request, profile),
                itstype = 'crm',
                url = '',
                image_url = 'crm'
            )
        card.save()
    data = {
    }
    return JsonResponse(data)

def save_salary(request):
    profile = Profile.objects.get(user = request.user.id)
    only_directors(profile)
    if request.GET.get('id') and request.GET.get('salary'):
        worker = Profile.objects.get(id=int(request.GET.get('id')))
        school = is_moderator_school(request, profile)
        is_in_school(worker, school)
        worker.salary = int(request.GET.get('salary'))
        worker.save()
    data = {
    }
    return JsonResponse(data)

def save_job_salary(request):
    profile = Profile.objects.get(user = request.user.id)
    school = is_moderator_school(request, profile)
    only_directors(profile)
    if request.GET.get('id') and request.GET.get('salary'):
        job = JobCategory.objects.get(id=int(request.GET.get('id')))
        job.salary = int(request.GET.get('salary'))
        job.save()
        for worker in job.job_workers.all():
            worker.salary = job.salary
            worker.save()
    data = {
    }
    return JsonResponse(data)

def delete_card(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    if request.GET.get('id'):
        card = school.crm_cards.get(id=int(request.GET.get('id')))
        if not card.was_called:
            if card.author_profile:
                skill = card.author_profile.skill
                skill.need_actions -= 1
                skill.save()
        card.delete()
    data = {
    }
    return JsonResponse(data)

def show_free_cards(request, school_id):
    school = School.objects.get(id=school_id)
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    if profile.skill == None:
        skill = Skill.objects.create()
        profile.skill = skill
        profile.save()
    if request.GET.get('check'):
        skill = profile.skill
        if request.GET.get('check') == 'true':
            skill.crm_show_free_cards = True
        else:
            skill.crm_show_free_cards = False  
        skill.save()          
    print(profile.first_name, skill.crm_show_free_cards)
    data = {
        'check':request.GET.get('check')
    }
    return JsonResponse(data)

def get_card_squads(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    card = CRMCard.objects.get(id=int(request.GET.get('id')))
    school = card.school
    is_in_school(profile, school)
    profile = card.card_user
    res = []

    bills = []
    if profile:
        nms = card.need_money.select_related('squad')
        for squad in profile.squads.all():
            res.append(squad.id)
            crnt = nms.filter(squad=squad)
            if len(crnt) > 0:
                crnt = crnt[0]
                bills.append([squad.title, crnt.money, crnt.lesson_bill, crnt.bill])
    data = {
        'res':res,
        'bills':bills,
    }
    return JsonResponse(data)

def take_card(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)    
    card = CRMCard.objects.get(id=int(request.GET.get('id')))
    school = card.school
    is_in_school(profile, school)
    ok = False
    if not card.author_profile:
        card.author_profile = profile
        ok = True
    else:
        card.author_profile = None
    card.save()
    data = {
        'ok':ok,
        "manager":profile.first_name,
        "manager_url":profile.get_absolute_url(),
    }
    return JsonResponse(data)

def change_day_of_week(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    status = 'no'
    card = CRMCard.objects.get(id=int(request.GET.get('card')))
    school = card.school
    is_in_school(profile, school)
    if len(card.days_of_weeks) < 7:
        card.days_of_weeks = [False,False,False,False,False,False,False]
    tag = Hashtag.objects.get_or_create(title='day'+str(int(request.GET.get('id'))+1))[0]
    school.hashtags.add(tag)
    if card.days_of_weeks[int(request.GET.get('id'))]:
        card.days_of_weeks[int(request.GET.get('id'))] = False
        card.hashtags.remove(tag)
    else:
        card.days_of_weeks[int(request.GET.get('id'))] = True
        status = 'yes'
        card.hashtags.add(tag)
    card.save()

    data = {
        'status':status,
    }
    return JsonResponse(data)

from django.contrib.postgres.search import TrigramSimilarity
def call_helper(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    text = request.GET.get('text')
    res = ''
    if text != '':
        if not request.GET.get('reverse'):
            text = text[::-1]
        res = []
        school = is_moderator_school(request, profile)
        kef = 1
        similarity=TrigramSimilarity('title', text)
        hashtags = school.hashtags.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        i = 0
        for hashtag in hashtags:
            res.append(hashtag.title)
            i+=1
            if i == 5:
                break
    
    data = {
        'res':res,
    }
    return JsonResponse(data)

def search_title(request):
    profile = Profile.objects.get(user = request.user.id)
    only_directors(profile)
    res = []
    if request.GET.get('status') and request.GET.get('text'):
        similarity=TrigramSimilarity('title', request.GET.get('text'))
        kef = 1
        if len(request.GET.get('text')) > 4:
            kef = 4
        if request.GET.get('status') == 'subject':
            objects = SubjectCategory.objects.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        elif request.GET.get('status') == 'level':
            objects = SubjectLevel.objects.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        else:
            objects = Office.objects.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')            
        i = 0
        for obj in objects:
            res.append(obj.title)
            i+=1
            if i == 5:
                break
    data = {
        'res':res,
    }
    return JsonResponse(data)

def change_title(request):
    profile = Profile.objects.get(user = request.user.id)
    only_directors(profile)
    if request.GET.get('id') and request.GET.get('text') and request.GET.get('status') and request.GET.get('text') != "":
        school = is_moderator_school(request, profile)
        if request.GET.get('status') == 'title':
            school.title = request.GET.get('text') 
        if request.GET.get('status') == 'slogan':
            school.slogan = request.GET.get('text') 
        if request.GET.get('status') == 'content':
            school.content = request.GET.get('text') 
        if request.GET.get('status') == 'site':
            school.site = request.GET.get('text') 
        if request.GET.get('status') == 'worktime':
            if request.GET.get('text') == '-':
                school.worktime = 'По предварительной записи'
            else:
                school.worktime = request.GET.get('text') 
        if request.GET.get('status') == 'phones':
            phones = request.GET.get('text').split(',')
            print(phones)
            if len(phones) > 0:
                school.phones = phones
        if request.GET.get('status') == 'social_networks':
            school.social_networks = request.GET.get('text') 
        school.save()
    data = {
    }
    return JsonResponse(data)

def save_review(request, school_id=None):
    if not request.user.is_authenticated:
        return JsonResponse({'nouser':True})
    profile = Profile.objects.get(user = request.user.id)
    if request.GET.get('number'):
        school = School.objects.get(id = school_id)
        if request.GET.get('number') != '':
            review = school.reviews.create(
                text=request.GET.get('text'),
                author_profile=profile,
                rating=int(request.GET.get('number')),
                )
            rating = 0
            for review in school.reviews.all():
                rating += review.rating
            rating = round(rating/len(school.reviews.all()),2)
            school.rating = rating 
            school.save()
    data = {
        "name":profile.first_name,
        "timestamp":review.timestamp.strftime('%d %m %Y %H:%M'),
    }
    return JsonResponse(data)

def delete_school_banner(request):
    profile = Profile.objects.get(user = request.user.id)
    if request.GET.get('id'):
        school = is_moderator_school(request, profile)
        banner = school.banners.filter(id=int(request.GET.get('id')))
        if len(banner) > 0:
            banner[0].delete()
    data = {
    }
    return JsonResponse(data)

from dateutil.relativedelta import relativedelta
def update_voronka(request):
    profile = Profile.objects.get(user = request.user.id)
    only_directors(profile)
    res = []
    is_ago = False
    if request.GET.get('status') and request.GET.get('first_vrnk') and request.GET.get('second_vrnk'):
        school = is_moderator_school(request, profile)
        timefuture = timezone.now().date()
        today = timefuture
        weekago = timezone.now().date() - timedelta(7)
        monthago = timezone.now().date() - relativedelta(months=1)
        yearago = timezone.now().date() - relativedelta(years=1)
        if request.GET.get('status') == 'get_here':
            if request.GET.get('value') == 'week':
                timeago = weekago
            if request.GET.get('value') == 'month':
                timeago = monthago
            if request.GET.get('value') == 'year':
                timeago = yearago
        if request.GET.get('status') == 'get_input':
            timeago = datetime.datetime.strptime(request.GET.get('first_vrnk'), "%Y-%m-%d").date()
            timefuture = datetime.datetime.strptime(request.GET.get('second_vrnk'), "%Y-%m-%d").date()
            if timefuture == today:
                if timeago == weekago:
                    is_ago = 'week_vrnk'
                elif timeago == monthago:
                    is_ago = 'month_vrnk'
                elif timeago == yearago:
                    is_ago = 'year_vrnk'
        number = 0
        manager = False
        timeago = timeago - timedelta(1)
        timefuture = timefuture + timedelta(1)
        if request.GET.get('manager_id') != '-1':
            manager = school.people.get(id=int(request.GET.get('manager_id')))
        all_cards = school.crm_cards.filter(timestamp__gt=timeago, timestamp__lt=timefuture)
        number_of_all = len(all_cards)
        if manager:
            all_cards = all_cards.filter(author_profile=manager)
        for column in school.crm_columns.all().order_by('-id'):
            if column.id != 6:
                x = len(all_cards.filter(column=column))
                number += x
                res.append([column.title, number, round((number/number_of_all)*100, 2)])            
    data = {
        "res":res,
        "timeago":timeago.strftime('%Y-%m-%d'),
        "is_ago":is_ago,
        "number":number,
    }
    return JsonResponse(data)

def new_money_object(request):
    profile = Profile.objects.get(user = request.user.id)
    only_directors(profile)
    if request.GET.get('title') and request.GET.get('amount'):
        school = is_moderator_school(request, profile)
        change_school_money(school, -1*int(request.GET.get('amount')), request.GET.get('title'), profile.first_name)        
    data = {
    }
    return JsonResponse(data)

def show_money_history(request):
    profile = Profile.objects.get(user = request.user.id)
    only_directors(profile)
    school = is_moderator_school(request, profile)
    res = []
    for money in school.money_object.all():
        res.append([money.title, money.amount, money.timestamp.strftime('%d.%m.%Y %H:%M')])
    data = {
        "res":res,
    }
    return JsonResponse(data)

def get_manager_actions(request):
    profile = Profile.objects.get(user = request.user.id)
    only_directors(profile)
    res = []
    if request.GET.get('id'):
        manager = Profile.objects.get(id=int(request.GET.get('id')))
        school = is_moderator_school(request, profile)
        history = sorted(
            chain(
                PaymentHistory.objects.filter(action_author=manager), 
                CRMCardHistory.objects.filter(action_author=manager), 
                SquadHistory.objects.filter(action_author=manager), 
                SubjectHistory.objects.filter(action_author=manager)),
            key=lambda item: item.timestamp, reverse=False)
        for h in history:
            edit = ''
            classname = h.__class__.__name__
            if classname == 'PaymentHistory':
                edit+='Принята оплата у '+h.user.first_name+', сумма '+str(h.amount)+'тг '
                if h.squad:
                    edit+='за группу '+h.squad.title
            elif classname == 'CRMCardHistory':
                edit += 'Карточка '+ h.card.name
                if h.oldcolumn != '' or h.newcolumn != '':
                    edit += ' <br>"' + h.oldcolumn+ '" -> "' + h.newcolumn+'"'
                else:
                    edit += ' изменения данных'
            else:
                edit += h.edit

            res.append([manager.first_name, h.timestamp.strftime('%d.%m.%Y %H:%M'), edit])
    data = {
        "res":res,
    }
    return JsonResponse(data)
