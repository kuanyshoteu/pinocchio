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
from squads.models import Squad,PaymentHistory,SquadHistory,DiscountSchool
from subjects.templatetags.ttags import get_date, get_pay_date,constant_school_lectures
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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse
import json
import urllib
from django.contrib.postgres.search import TrigramSimilarity
from dateutil.relativedelta import relativedelta

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
            "page":"ratings",
        }
        return render(request, "school/school_rating.html", context)
    else:
        school = is_moderator_school(request, profile)
        context = {
            "profile":profile,
            "instance": profile.schools.first(),
            "squads":school.groups.filter(shown=True),
            "subject_categories":school.school_subject_categories.all(),
            "subject_ages":school.school_subject_ages.all(),
            "all_students":school.people.filter(),
            'is_trener':is_profi(profile, 'Teacher'),
            "is_manager":is_profi(profile, 'Manager'),
            "is_director":is_profi(profile, 'Director'),
            "is_moderator":is_profi(profile, 'Moderator'),
            "school_money":school.money,
            "school_crnt":school,
            "page":"ratings",
        }
        return render(request, "school/school_rating.html", context)

def school_payments(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    context = {
        "profile":profile,
        "instance": school,
        "squads":school.groups.filter(shown=True),
        "payments":True,
        "subject_categories":school.school_subject_categories.all(),
        "subject_ages":school.school_subject_ages.all(),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
        "page":"payments",
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
        "crm_cabinets":school.cabinets.all(),
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
        "page":"schedule",
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
                additional = '?type=moderator&mod_school_id='+str(school.id)
                return redirect(school.get_absolute_url()+additional)
    manager_prof = Profession.objects.get(title='Manager')
    managers = school.people.filter(profession=manager_prof)
    teacher_prof = Profession.objects.get(title='Teacher')
    teachers = school.people.filter(profession=teacher_prof)
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
        "squads":school.groups.filter(shown=True),
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
        "teachers":teachers,
        "voronka_array":voronka,
        "voronka2":voronka2,
        "worktime1":worktime1,
        "worktime2":worktime2,
        "social_networks":get_social_networks(school),
        "page":"info",        
    }
    return render(request, "school/info.html", context)
def get_social_networks(school):
    social_networks = []
    for i in range(0, min(len(school.social_network_links) , len(school.social_networks) )):
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
        "page":"finance",        
    }
    return render(request, "school/salaries.html", context)

def social_networks_settings(request):
    profile = get_profile(request)
    only_directors(profile)
    school = is_moderator_school(request, profile)
    context = {
        "profile":profile,
        "instance": school,
        "social_networks_settings":True,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
        "page":"info",
        "socialmedias":SocialMedia.objects.all(),
    }
    return render(request, "school/social_networks_settings.html", context)

def instagram_connecting(request):
    profile = get_profile(request)
    only_directors(profile)
    school = is_moderator_school(request, profile)
    print('yo1', instagram_id)
    sm = SocialMedia.objects.get(title='Instagram')
    insta = school.socialmedias.filter(socialmedia=sm)
    had_insta = False
    if len(insta) > 0:
        had_insta = True
        insta = insta[0]
    if request.GET.get('code'):
        code = request.GET.get('code')
        print('yo2', code, '<-code')
        url = 'https://api.instagram.com/oauth/access_token'
        data = {
            'client_id':instagram_id, 
            'client_secret':secret_instagram, 
            'grant_type':'authorization_code',
            'redirect_uri':insta_server, 
            'code':code,
        }
        r = requests.post(url,data=data,allow_redirects=True)
        a = json.loads(r.content)
        if not had_insta:
            insta = school.socialmedias.create(socialmedia=sm)
        user_id = str(a['user_id'])

        url2 = 'https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret='+secret_instagram+'&access_token='+str(a['access_token'])
        r2 = urllib.request.urlopen(url2).read()
        a2 = json.loads(r2)
        access_token = str(a2['access_token'])
        print('longtoken',a2['expires_in'], a2['token_type'])

        url3 = 'https://graph.instagram.com/'+user_id+'?fields=username&access_token='+access_token
        r3 = urllib.request.urlopen(url3).read()
        a3 = json.loads(r3)
        insta.user_id = user_id
        insta.access_token = access_token
        insta.username = a3['username']
        insta.save()
    return redirect('/schools/social_networks_settings')

def connect_sm(request):
    ok = False
    profile = Profile.objects.get(user = request.user.id)
    only_directors(profile)
    print('yo6')
    if request.GET.get('status') == 'Instagram':
        url = 'https://api.instagram.com/oauth/authorize/?client_id='+instagram_id+'&redirect_uri='+insta_server+'&scope=user_profile,user_media&response_type=code'
    elif request.GET.get('status') == 'Вконтакте':
        url = 'https://oauth.vk.com/authorize?client_id='+vk_id+'&display=page&redirect_uri='+vk_server+'&scope=groups&response_type=code&v=5.103'
    data = {
        'url':url,
    }
    return JsonResponse(data)

def vk_connecting(request):
    profile = get_profile(request)
    only_directors(profile)
    school = is_moderator_school(request, profile)
    print('yo1 vk')
    sm = SocialMedia.objects.get(title='Вконтакте')
    vk = school.socialmedias.filter(socialmedia=sm)
    if len(vk) > 0:
        vk = vk[0]
    else:
        vk = school.socialmedias.create(socialmedia=sm)
    group_list = []
    print('vk_connecting 1')
    if request.GET.get('code'):
        print('vk_connecting code')
        if vk.first_connect:
            print('getting user')
            code = request.GET.get('code')
            group_list = vk_get_user_access(code, vk)
            vk.first_connect = False
            vk.save()
        else:
            print('getting group')
            code = request.GET.get('code')
            vk.group_access_token = vk_get_group_access(code, vk)
            vk_set_callback(vk)
            vk.first_connect = True
            vk.save()
            return redirect('/schools/social_networks_settings')
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
        "vk_account":vk,
        "group_list":group_list,
        "page":"info",        
    }
    return render(request, "socialmedias/vk_connecting.html", context)
def save_vk_group(request):
    profile = Profile.objects.get(user = request.user.id)
    only_directors(profile)
    school = is_moderator_school(request, profile)
    if request.GET.get('id'):
        sm = SocialMedia.objects.get(title='Вконтакте')
        vk = school.socialmedias.filter(socialmedia=sm)[0]
        vk.groupid = request.GET.get('id')
        vk.groupname = request.GET.get('name')
        vk.save()
        url = 'https://oauth.vk.com/authorize?client_id='+vk_id+'&display=page&redirect_uri='+vk_server+'&group_ids='+vk.groupid+'&scope=messages,manage&response_type=code&v=5.103'
        print('save_vk_group')
    data = {
        "url":url,
    }
    return JsonResponse(data)

def long_poll():
    vk_longpoll_url = 'https://api.vk.com/method/groups.getLongPollServer'
    data = {
        'group_id':group_id,  # Надо достать его из бд 
        'access_token':access_token, 
        'v':'5.103', 
    }
    r = requests.post(vk_longpoll_url,data=data,allow_redirects=True)
    a = json.loads(r.content)
    key = a['key']
    server = a['server']
    ts = a['ts']
    vk.key = key
    vk.server = server
    vk.save()
    #Это получение данных
    # connect_longpoll_url = server
    # data = {
    #     'act':'a_check', 
    #     'key':key, 
    #     'ts':ts, 
    #     'wait':25,
    # }
    # r = requests.post(url,data=data,allow_redirects=True)
    # a = json.loads(r.content)

def vk_get_callback(request):
#    Подключение Callback API - уведомления сами приходят на сервер
    if request.method == 'POST':
        a = json.loads(request.body)
        print('yoyoyo', a['type'],a)
        confirmation_code = '0'
        if a['type'] == 'confirmation':
            group_id = str(a['group_id'])
            vks = SocialMediaAccount.objects.filter(groupid=group_id)
            if len(vks) > 0:
                vk = vks[0]
                confirmation_code = vk.confirmation_code
                print('return confirmation', confirmation_code)
            return HttpResponse(confirmation_code, content_type='text/plain')
        elif a['type'] == 'message_new':
            print("0 0 0 MESSAGE 0 0 0 0")
            return HttpResponse('1', content_type='text/plain')

def vk_set_callback(vk):
    groupid = vk.groupid
    group_access_token = vk.group_access_token
    print('vk_set_callback')
    allservers = vk_get_servers(groupid, group_access_token)
    count = 0
    server_id = -1
    servers = []
    for server in allservers:
        if server['title'] == 'Bilimtap':
            count += 1
            servers.append(server)
    if count > 1:
        for i in range(1, len(servers)):
            print('deleting servers', i)
            server = servers[i]
            vk_delete_server(groupid, server, group_access_token)
    secretkey = random_secrete_confirm()
    if count > 0:
        print('editing server vk')
        server_id = servers[0]['id']
        vk_edit_server(groupid, server_id, secretkey, group_access_token)
    else:
        print('adding server to vk')
        server_id = vk_add_server(groupid, secretkey, group_access_token)

    api_version = vk_get_callback_api_version(groupid,server_id,group_access_token)
    vk_set_callback_settings(groupid, server_id, api_version,group_access_token)

    confirmation_code = vk_get_confirmation_code(groupid, group_access_token)

    vk.serverid = str(server_id)
    vk.secretkey = secretkey
    vk.confirmation_code = confirmation_code
    print('confirmation_code', confirmation_code)
    vk.save()


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
    if is_director:
        manager_prof = Profession.objects.get(title='Manager')
        managers = school.people.filter(profession=manager_prof)
        director_prof = Profession.objects.get(title='Director')
        dirs = school.people.filter(profession=director_prof)
        managers = set(chain(managers, dirs))
    context = {
        "theprofile":theprofile,
        "profile":profile,
        "instance": school,
        "columns":school.crm_columns.all(),
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
        "squads":school.groups.all(),
        'crmdays':Day.objects.all(),
        "subject_categories":school.school_subject_categories.all(),
        'height':28*15*int(60/school.schedule_interval)+25,
        "page":"crm",        
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
        print(managers)
        director_prof = Profession.objects.get(title='Director')
        dirs = school.people.filter(profession=director_prof)
        managers = set(chain(managers, dirs))
        print('c',managers, dirs)
    context = {
        "profile":profile,
        "instance": school,
        "columns":school.crm_columns.all(),
        "squads":school.groups.all(),
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
        "page":"crm",
        'crmdays':Day.objects.all(),
        "crm_all":True,        
    }
    return render(request, "school/crm.html", context)

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
                subject = qs[0]
                school.school_subject_categories.add(subject)
                school_cats = subject.school_categories.all()
                school.categories.add(*school_cats)
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
    school_cats = subject.school_categories.all()
    school.categories.remove(*school_cats)
    hashtag = school.hashtags.filter(title = subject.title.replace(' ', '_'))
    if len(hashtag) > 0:
        hashtag.delete()
    school.school_subject_categories.remove(subject)
    data = {
    }
    return JsonResponse(data)

def discount_create(request):
    manager_profile = Profile.objects.get(user = request.user.id)
    only_managers(manager_profile)
    create_url = ''
    delete_url = ''
    idd = -1
    if request.GET.get('id') and request.GET.get('title') and request.GET.get('amount') and request.GET.get('discount_type'):
        title = request.GET.get('title')
        amount = int(request.GET.get('amount'))
        discount_type = request.GET.get('discount_type')
        school = is_moderator_school(request, manager_profile)
        if request.GET.get('id') == '_new':
            if school.discounts.filter(title = title):
                discount = school.discounts.filter(title = title)[0]
                return JsonResponse({'taken_name':True})
            qs = DiscountSchool.objects.filter(title=title)
            if len(qs) > 0:
                school.discounts.add(qs[0])
                discount = qs[0]
            else:
                discount = school.discounts.create(title=title,amount=amount,discount_type=discount_type)
        else:
            discount = school.discounts.get(id=int(request.GET.get('id')))
            discount.title = title
            discount.amount = request.GET.get('amount')
            discount.discount_type = request.GET.get('discount_type')
        discount.save()
        idd = discount.id
        create_url = discount.create_url()
        delete_url = discount.delete_url()
    data = {
        'taken_name':False,
        'create_url':create_url,
        'delete_url':delete_url,
        'idd':idd,
    }
    return JsonResponse(data)

def discount_delete(request):
    profile = Profile.objects.get(user = request.user.id)
    school = is_moderator_school(request, profile)
    only_managers(profile)
    discount = school.discounts.get(id=int(request.GET.get('id')))
    discount.delete()
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
        capacity = 100
        if request.GET.get('capacity'):
            capacity = int(request.GET.get('capacity'))
        office.cabinets.create(
            school=school,
            title=request.GET.get('title'),
            capacity=capacity,
            )
    data = {
    }
    return JsonResponse(data)
def delete_cabinet(request):
    profile = Profile.objects.get(user = request.user.id)
    school = is_moderator_school(request, profile)
    only_managers(profile)
    if request.GET.get('id'):
        cainet = school.cabinets.get(id=int(request.GET.get('id')))
        cainet.delete()
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

def save_card_as_user(request):
    manager_profile = Profile.objects.get(user = request.user.id)
    only_managers(manager_profile)
    school = is_moderator_school(request, manager_profile)
    password = ''
    add = True
    problems = 'ok'
    ok_mail = False
    res = []
    if request.GET.get('id') and request.GET.get('squad_id'):
        card = school.crm_cards.get(id = int(request.GET.get('id')))
        squad_id = int(request.GET.get('squad_id'))
        if squad_id > 0:
            squad = Squad.objects.get(id=squad_id)
            if card.saved == False:
                password = random_password()
                found = False
                student = False
                if card.mail != '' and len(Profile.objects.filter(mail=card.mail)) > 0:
                    student = Profile.objects.filter(mail=card.mail)[0]
                    found = True
                elif len(Profile.objects.filter(phone=card.phone)) > 0:
                    student = Profile.objects.filter(phone=card.phone)[0]
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
                profile = register_new_student(found,card,password,manager_profile,student,squad_id,school)
                add_student_to_squad(profile, squad,manager_profile)
            else:
                profile = card.card_user
                card.author_profile = manager_profile
                if profile in squad.students.all():
                    add = False
                    remove_student_from_squad(profile, squad, manager_profile)
                    ok_mail = True
                else:
                    problems = add_student_to_squad(profile, squad, manager_profile)
                    ok_mail = prepare_mail(profile.first_name, card.phone, card.mail, squad, None, True)
                profile.schools.add(school)
                card.last_groups = squad_id
                card.timestamp = timezone.now()
                card.save()
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
        if request.GET.get('option') == 'crm_cabinet':
            if int(request.GET.get('object_id')) == -1:
                skill.crm_cabinet = None
            else:
                crm_cabinet = Cabinet.objects.get(id = int(request.GET.get('object_id')))
                skill.crm_cabinet = crm_cabinet
        if request.GET.get('option') == 'office':
            if int(request.GET.get('object_id')) == -1:
                skill.crm_office2 = None
            else:
                office = Office.objects.get(id = int(request.GET.get('object_id')))
                skill.crm_office2 = office
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
    only_directors(profile)
    added = False
    school = is_moderator_school(request, profile)
    if request.GET.get('id') and request.GET.get('office'):
        manager = school.people.get(id=int(request.GET.get('id')))
        skill = manager.skill
        office = Office.objects.get(id = int(request.GET.get('office')))
        hisoffice = skill.crm_office2 
        if office == hisoffice:
            skill.crm_office2 = None            
        else:
            added = True
            skill.crm_office2 = office
        skill.save()
    data = {
        "added":added,
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

def card_send_mail(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    ok = False
    if request.GET.get('id') and request.GET.get('mail') and request.GET.get('text'):
        school = is_moderator_school(request, profile)
        card = school.crm_cards.get(id = int(request.GET.get('id')))
        head = school.title
        text = request.GET.get('text')
        send_email(head, text,[request.GET.get('mail')])
        ok = True
        time = timezone.now()
        print(card.mail)
        mail = card.mails.create(
            text = request.GET.get('text'),
            method = card.mail,
            action_author=profile,
            timestamp=time,
            )
        mail.save()
    data = {
        'ok':ok,
        'time':time.strftime('%d %B %H:%M'),
        'author':profile.first_name,
        'message_id':mail.id,
    }
    return JsonResponse(data)

def edit_card_mail(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    if request.GET.get('id') and request.GET.get('mail'):
        school = is_moderator_school(request, profile)
        card = school.crm_cards.get(id = int(request.GET.get('id')))
        student = card.card_user
        student.mail = request.GET.get('mail')
        student.save()
        card.mail = request.GET.get('mail')
        card.save()
        edit = ''
        if card.mail != request.GET.get('mail'):
            edit = "Почта: " + card.mail + " -> " + request.GET.get('mail')
        CRMCardHistory.objects.create(
            action_author = profile,
            card = card,
            edit = edit,
            )
    data = {
    }
    return JsonResponse(data)

def edit_card(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    if request.GET.get('id') and request.GET.get('name') and request.GET.get('phone'):
        school = is_moderator_school(request, profile)
        card = school.crm_cards.get(id = int(request.GET.get('id')))
        student = card.card_user
        edit_card_detailed(card, student, school,request,profile)
    data = {
    }
    return JsonResponse(data)

def send_login_url(request):
    manager_profile = Profile.objects.get(user = request.user.id)
    only_managers(manager_profile)
    school = is_moderator_school(request, manager_profile)
    ok = False
    if request.GET.get('mail') and request.GET.get('id'):
        card = school.crm_cards.filter(id=int(request.GET.get('id')))
        if len(card) > 0:
            card = card[0]
            found = False
            student = False
            if card.mail != '' and len(Profile.objects.filter(mail=card.mail)) > 0:
                student = Profile.objects.filter(mail=card.mail)[0]
                found = True
            elif len(Profile.objects.filter(phone=card.phone)) > 0:
                student = Profile.objects.filter(phone=card.phone)[0]
                found = True
            # Set password
            password = random_password()
            register_new_student(found,card,password,manager_profile,student,-1,school)
            student = card.card_user
            edit_card_detailed(card, student, school,request,manager_profile)
            if found:
                user = student.user
                user.set_password(password)
                user.save()
            # Send login and password to client email
            mail = request.GET.get('mail')
            head = 'Bilimtap Логин и Пароль'
            text = "Здравствуйте " + student.first_name + "! "
            text += "Вы зарегестрированы на сайте <a href='bilimtap.kz'>bilimtap.kz</a><br><br>"
            login_text = "<br>Ваш логин: "+student.phone+" или "+student.mail
            password_text = "<br>Ваш пароль (не говорите никому): "+password
            text += login_text + password_text
            send_email(head, text,[mail])
            ok = True
    data = {
        "ok":ok,
    }
    return JsonResponse(data)

def edit_card_detailed(card, student, school,request,profile):
    edit = '***Редактирование*** '
    if card.name != request.GET.get('name') and card.name:
        edit = edit + "Имя: " + card.name + " -> " + request.GET.get('name') + "; "
        if student:
            student.first_name = request.GET.get('name')
    if card.phone != request.GET.get('phone'):
        edit = edit + "Номер: " + card.phone + " -> " + request.GET.get('phone') + "; "
        if student:
            student.phone = request.GET.get('phone')
    if card.extra_phone != request.GET.get('extra_phone'):
        edit = edit + "Дополнительный номер: " + card.extra_phone + " -> " + request.GET.get('extra_phone') + "; "
    if card.parents != request.GET.get('parents'):
        edit = edit + "Родители: " + card.parents + " -> " + request.GET.get('parents') + "; "
    if card.comments != request.GET.get('comment'):
        edit = edit + "Коммент: " + card.comments + " -> " + request.GET.get('comment') + "; "
    if student:
        student.save()
    card.name = request.GET.get('name')
    card.phone = request.GET.get('phone')
    card.extra_phone = request.GET.get('extra_phone')
    card.parents = request.GET.get('parents')
    card.comments = request.GET.get('comment')
    crnt_tag = ''
    wright = False
    hashtags = school.hashtags.all()
    alltags = card.hashtags.all()
    card.hashtags.remove(*alltags)
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
    CRMCardHistory.objects.create(
        action_author = profile,
        card = card,
        edit = edit,
        )

def open_card(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    res = []
    if request.GET.get('id'):
        school = is_moderator_school(request, profile)
        card = school.crm_cards.get(id = int(request.GET.get('id')))
        for history in card.history.all():
            if history.action_author:
                author_name = history.action_author.first_name
                author_url = history.action_author.get_absolute_url()
            else:
                author_name = 'Свободная'
                author_url = ''
            res.append([
                author_name,            #0
                author_url,             #1
                history.timestamp.strftime('%d.%m.%Y %H:%M'), #2
                history.oldcolumn,      #3
                history.newcolumn,      #4  
                history.edit,           #5
                ])  
    data = {
        'res':res,
    }
    return JsonResponse(data)

def register_new_student(found,card,password,manager_profile,profile,squad_id,school):
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
    if profile:
        card.card_user = profile
    card.author_profile = manager_profile
    card.timestamp = timezone.now()
    if squad_id > 0:
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
    return profile

def card_called(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    if request.GET.get('id'):
        school = is_moderator_school(request, profile)
        card = school.crm_cards.get(id = int(request.GET.get('id')))
        skill = profile.skill
        if request.GET.get('action') == 'done':
            if not card.was_called:
                skill.need_actions -= 1
            card.was_called = True
        else:
            card.action = request.GET.get('action')
            if card.was_called:
                card.was_called = False
                skill.need_actions += 1
        skill.save()
        card.timestamp = timezone.now()
        card.save()
    data = {
        'is_called':card.was_called,
        'time':timezone.now().strftime('%d.%m.%Y %H:%M')
    }
    return JsonResponse(data)

def add_card(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    res = []
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
        res += get_card_data_by_column(card, column.id)        
    data = {
        "res":res,
    }
    return JsonResponse(data)

def move_worker(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    ok = False
    if request.GET.get('worker_id') and request.GET.get('job_id') and request.GET.get('oldjob_id'):
        school = is_moderator_school(request, profile)
        oldjob = False
        job = False
        jobprof = False
        worker = school.people.get(id = int(request.GET.get('worker_id')))
        professions = worker.profession.all()
        if int(request.GET.get('oldjob_id')) > 0:
            oldjob = school.job_categories.get(id = int(request.GET.get('oldjob_id')))  
        if int(request.GET.get('job_id')) > 0:
            job = school.job_categories.get(id = int(request.GET.get('job_id')))
            if not job.profession in professions:
                return JsonResponse({'ok':ok})

        ok = True
        if oldjob:
            worker.job_categories.remove(oldjob)
        if job:
            worker.job_categories.add(job)
    data = {
        'ok':ok
    }
    return JsonResponse(data)
def add_job(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    if request.GET.get('id') and request.GET.get('title'):
        school = is_moderator_school(request, profile)
        prof = Profession.objects.get(id = int(request.GET.get('id')))
        job = prof.job_categories.get_or_create(title=request.GET.get('title'))[0]
        job.save()
        job.schools.add(school)
    data = {
    }
    return JsonResponse(data)
def delete_job(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    ok =  False
    if request.GET.get('id'):
        school = is_moderator_school(request, profile)
        job = school.job_categories.get(id = int(request.GET.get('id')))
        prof = job.profession
        if len(prof.job_categories.all()) > 1:
            ok = True
            workers = job.job_workers.all()
            job.job_workers.remove(*workers)
            school.job_categories.remove(job)
    data = {
        'ok':ok
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
    author_url = ''
    author_name = 'Свободная'
    if request.GET.get('manager') and request.GET.get('card'):
        school = is_moderator_school(request, profile)
        card = school.crm_cards.get(id = int(request.GET.get('card')))
        if request.GET.get('manager') == '-1':
            card.author_profile = None
        else:
            manager = Profile.objects.get(id=int(request.GET.get('manager')))
            card.author_profile = manager
            author_name = manager.first_name
            author_url = manager.get_absolute_url()
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
        'author_url':author_url,
        'author_name':author_name,
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
    if profile:
        for squad in profile.squads.filter(shown=True):
            res.append(squad.id)
    data = {
        'res':res,
    }
    return JsonResponse(data)

def get_card_info(request):
    bills = []
    if request.GET.get('id'):
        profile = Profile.objects.get(user = request.user.id)
        card = CRMCard.objects.get(id=int(request.GET.get('id')))
        only_managers(profile)
        school = card.school
        is_in_school(profile, school)
        profile = card.card_user
        nms = card.need_money.select_related('squad')
        if profile:
            for squad in profile.squads.filter(shown=True):
                crnt = nms.filter(squad=squad)
                if len(crnt) > 0:
                    crnt = crnt[0]
                    bills.append([squad.title, 
                        crnt.money, 
                        squad.lesson_bill, 
                        squad.bill,
                        squad.id])
        colid = card.column.id
        res = get_card_data_by_column(card, colid)
        form_res = get_card_form_by_column(card, colid)
        dialog = get_card_dialog(card)
    data = {
        'bills':bills,
        'res':res,
        'form_res':form_res,
        'dialog':dialog,
        'colid':colid,
    }
    return JsonResponse(data)

def get_card_info_dialog(request):
    if request.GET.get('id'):
        profile = Profile.objects.get(user = request.user.id)
        card = CRMCard.objects.get(id=int(request.GET.get('id')))
        only_managers(profile)
        school = card.school
        is_in_school(profile, school)
        profile = card.card_user
        dialog = get_card_dialog(card)
    data = {
        'dialog':dialog,
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

def call_helper(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    text = request.GET.get('text')
    res = ''
    if text != '':
        if not request.GET.get('reverse'):
            text = text[::-1]
        school = is_moderator_school(request, profile)
        res = []
        kef = 1
        if len(text) > 2:
            kef = 4
        similarity=TrigramSimilarity('name', text)
        cards = school.crm_cards.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        i = 0
        for card in cards:
            res.append(card.name)
            i+=1
            if i == 5:
                break
        if i < 5:
            similarity=TrigramSimilarity('phone', text)
            cards = school.crm_cards.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
            for card in cards:
                res.append(card.phone)
                i+=1
                if i == 5:
                    break
        if i < 5:
            similarity=TrigramSimilarity('parents', text)
            cards = school.crm_cards.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
            for card in cards:
                res.append(card.parents)
                i+=1
                if i == 5:
                    break
        if i < 5:
            similarity=TrigramSimilarity('title', text)
            hashtags = school.hashtags.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
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
        print('0', request.GET.get('type'))
        school = is_moderator_school(request, profile)
        print('1', school.title)
        banner = school.banners.filter(id=int(request.GET.get('id')))
        if len(banner) > 0:
            print('2')
            banner[0].delete()
    data = {
    }
    return JsonResponse(data)

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
    ok = False
    profession = Profession.objects.get(title = 'Director')
    if profession in profile.profession.all():
        ok = True
    res = []
    if request.GET.get('id'):
        manager = Profile.objects.get(id=int(request.GET.get('id')))
        if manager == profile:
            ok = True
        if ok:
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
                    if h.amount < 0:
                        edit += 'Отмена оплаты у '
                    else:
                        edit+='Принята оплата у '
                    edit += h.user.first_name+', сумма '+str(h.amount)+'тг '
                    if h.squad:
                        edit+='за группу '+h.squad.title
                elif classname == 'CRMCardHistory':
                    edit += h.card.name
                    if h.oldcolumn != '' or h.newcolumn != '':
                        edit += ' <br>"' + h.oldcolumn+ '" -> "' + h.newcolumn+'"'
                    elif h.edit != '':
                        edit += h.edit
                    else:
                        edit += ' изменения данных'
                else:
                    edit += h.edit

                res.append([manager.first_name, h.timestamp.strftime('%d.%m.%Y %H:%M'), edit])
    data = {
        "res":res,
    }
    return JsonResponse(data)

def get_student_actions(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    res = []
    if request.GET.get('id'):
        school = is_moderator_school(request, profile)
        student = Profile.objects.get(id=int(request.GET.get('id')))
        card = school.crm_cards.get(card_user=student)
        history = sorted(
            chain(
                school.payment_history.filter(user=student), 
                card.history.all(),
                student.hisgrades.filter(school=school, present='present')),
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
                elif h.edit != '':
                    edit += h.edit
                else:
                    edit += ' изменения данных'
            elif classname == 'Attendance':
                edit = 'Посетил урок курса '+ h.subject.title+'<br>Дата: '+get_date(h.subject_materials, h.squad)[0].strftime('%d.%m.%Y')

            res.append([student.first_name, h.timestamp.strftime('%d.%m.%Y %H:%M'), edit])
    data = {
        "res":res,
        'student':True,
    }
    return JsonResponse(data)

def get_teacher_actions(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    res = []
    if request.GET.get('id'):
        school = is_moderator_school(request, profile)
        teacher = Profile.objects.get(id=int(request.GET.get('id')))
        materials = teacher.done_subject_materials.filter(school=school).select_related('subject')
        squads = teacher.hissquads.all().prefetch_related('subjects')
        for mat in materials:
            subject = mat.subject
            sq = squads.filter(subjects=subject)[0]
            date = get_date(mat, sq)[0].strftime('%d.%m.%Y')
            edit = 'Провел урок курса '+ subject.title
            edit+='<br>Дата: '+date
            edit+='<br>Заработок: '+str(teacher.salary)+'тг'
            res.append([teacher.first_name, date,edit])
    data = {
        "res":res,
        'teacher':True,
    }
    return JsonResponse(data)

def get_schedule(request):
    profile = Profile.objects.get(user = request.user.id)
    school = is_moderator_school(request, profile)
    data = {
        "res":constant_school_lectures(profile, school),
    }
    return JsonResponse(data)    

def get_all_cards_first(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    page = 1
    all_res = []
    for column in school.crm_columns.all():
        res = []
        if profile.skill and request.GET.get('all') == 'no':
            if profile.skill.crm_show_free_cards:
                res = column.cards.filter(author_profile=None, school=school)
        if res == []:
            if request.GET.get('all') == 'yes':
                res = column.cards.filter(school=school)
            else:
                res = column.cards.filter(author_profile=profile, school=school)
        if len(res) <= 0:
            continue
        p = Paginator(res, 4)
        page1 = p.page(page)
        res = []
        colid = column.id
        for card in page1.object_list:
            res += get_card_data_by_column(card, colid)
        all_res.append([colid,res])
    managers_res = [] 
    if is_profi(profile, 'Director'):
        manager_prof = Profession.objects.get(title='Manager')
        managers = school.people.filter(profession=manager_prof)
        for manager in managers:
            managers_res.append([manager.id,manager.first_name])
    data = {
        "all_res":all_res,
        "page":page,
        "is_director":is_profi(profile, 'Director'),
        "managers_res":managers_res,
        "Ended":False,
    }
    return JsonResponse(data)

def get_all_cards_second(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    all_res = []
    for column in school.crm_columns.all():
        query = []
        if profile.skill and request.GET.get('all') == 'no':
            if profile.skill.crm_show_free_cards:
                query = column.cards.filter(author_profile=None, school=school)
        if query == []:
            if request.GET.get('all') == 'yes':
                query = column.cards.filter(school=school)
            else:
                query = column.cards.filter(author_profile=profile, school=school)
        res = []
        colid = column.id
        i = 0
        for card in query:
            i += 1
            if i <= 4:
                continue
            if i > 10:
                break
            res += get_card_data_by_column(card, colid)
        all_res.append([colid,res])            
    managers_res = [] 
    if is_profi(profile, 'Director'):
        manager_prof = Profession.objects.get(title='Manager')
        managers = school.people.filter(profession=manager_prof)
        for manager in managers:
            managers_res.append([manager.id,manager.first_name])
    data = {
        "all_res":all_res,
        "page":2,
        "is_director":is_profi(profile, 'Director'),
        "managers_res":managers_res,
        "Ended":False,
    }
    return JsonResponse(data)

def search_crm_cards(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    text = request.GET.get('text')
    res = []
    if text != '':
        school = is_moderator_school(request, profile)
        kef = 16
        similarity=TrigramSimilarity('name', text)
        cards = school.crm_cards.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        if len(cards) < 5:
            similarity=TrigramSimilarity('phone', text)
            extra = school.crm_cards.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
            cards = set(chain(cards, extra))
        if len(cards) < 5:
            similarity=TrigramSimilarity('parents', text)
            extra = school.crm_cards.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
            cards = set(chain(cards, extra))
        if len(cards) < 5:
            similarity=TrigramSimilarity('title', text)
            hashtags = school.hashtags.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
            extra = school.crm_cards.filter(hashtags__in=hashtags)
            cards = set(chain(cards, extra))
        i = 0
        for card in cards:
            colid = card.column.id
            res.append([colid, get_card_data_by_column(card, colid)])
            i+=1
            if i == 5:
                break
    res.reverse()
    data = {
        'res':res,
    }
    return JsonResponse(data)

def filter_crm_cards_work(cards, request,all_squads,all_students,all_offices):
    if len(request.GET.get('offices')) > 0:
        sids = request.GET.get('offices').split('d')
        del sids[-1]
        offices = all_offices.filter(id__in=sids)
        squads = all_squads.filter(office__in=offices)
        students = all_students.filter(squads__in=squads)
        cards = cards.filter(card_user__in=students)
    if len(request.GET.get('squads')) > 0:
        sids = request.GET.get('squads').split('d')
        del sids[-1]
        squads = all_squads.filter(id__in=sids)
        students = all_students.filter(squads__in=squads)
        cards = cards.filter(card_user__in=students)
    if len(request.GET.get('days')) > 0:
        sids = request.GET.get('days').split('d')
        del sids[-1]
        slen = len(sids)
        for i in range(0,slen):
            sids[i] = 'day'+str(get_day_text(sids[i]))
        tags = Hashtag.objects.filter(title__in=sids)
        cards = cards.filter(hashtags__in=tags)
    return cards

def filter_crm_cards(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    if request.GET.get('is_all') == 'yes':
        all_cards = school.crm_cards.all().select_related('card_user')
    else:
        if profile.skill.crm_show_free_cards:
            all_cards = school.crm_cards.filter(author_profile=None).select_related('card_user')
        else:
            all_cards = school.crm_cards.filter(author_profile=profile).select_related('card_user')
    all_squads = school.groups.all()
    all_students = school.people.filter(is_student=True).prefetch_related('squads')
    all_offices = school.school_offices.all()
    all_res = []
    for column in school.crm_columns.all():
        cards = all_cards.filter(column=column)
        cards = filter_crm_cards_work(cards, request,all_squads,all_students,all_offices)
        i = 0
        res = []
        colid = column.id
        for card in cards:
            i+=1
            if i == 10:
                break
            res += get_card_data_by_column(card, colid)
        all_res.append([colid,res])            
    data = {
        'all_res':all_res,
    }
    return JsonResponse(data)

def get_extra_cards(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    res = []
    school = is_moderator_school(request, profile)
    if request.GET.get('column') and request.GET.get('page'):
        page = int(request.GET.get('page'))+1
        column = CRMColumn.objects.get(id=int(request.GET.get('column')))
        if profile.skill and request.GET.get('all') == 'no':
            if profile.skill.crm_show_free_cards:
                res = column.cards.filter(author_profile=None, school=school)
        if res == []:
            if request.GET.get('all') == 'yes':
                res = column.cards.filter(school=school)
            else:
                res = column.cards.filter(author_profile=profile, school=school)
        all_squads = school.groups.all()
        all_students = school.people.filter(is_student=True).prefetch_related('squads')
        all_offices = school.school_offices.all()
        res = filter_crm_cards_work(res, request,all_squads,all_students,all_offices)        
        if len(res) <= (page-1)*10:
            return JsonResponse({"Ended":True})
        p = Paginator(res, 10)
        page1 = p.page(page)
        res = []
        colid = column.id
        for card in page1.object_list:
            res += get_card_data_by_column(card, colid)
        managers_res = [] 
        if is_profi(profile, 'Director'):
            manager_prof = Profession.objects.get(title='Manager')
            managers = school.people.filter(profession=manager_prof)
            for manager in managers:
                managers_res.append([manager.id,manager.first_name])
    data = {
        "res":res,
        "page":page,
        "is_director":is_profi(profile, 'Director'),
        "managers_res":managers_res,
        "Ended":False,
    }
    return JsonResponse(data)

def payment_history(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    res = []
    student_name = False
    if request.GET.get('id'):
        student = school.people.filter(id=int(request.GET.get('id')))
        if len(student) > 0:
            student = student[0]
            student_name = student.first_name
            for payment in student.payment_history.all():
                squad_title = ''
                if payment.squad:
                    squad_title = payment.squad.title
                cancel_access = False
                if payment.timestamp > timezone.now() - timedelta(3):
                    cancel_access = True
                res.append([
                    payment.timestamp.strftime('%d.%m.%Y %H:%M'), #0
                    payment.amount,                               #1
                    squad_title,                                  #2
                    payment.action_author.get_absolute_url(),     #3
                    payment.action_author.first_name,             #4
                    cancel_access,                                #5
                    payment.id,                                   #6
                    ])
    data = {
        "res":res,
        "student_name":student_name,
    }
    return JsonResponse(data)

def group_finance(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    res = []
    res_squad = []
    if request.GET.get('id'):
        squad = school.groups.get(id=int(request.GET.get('id')))
        teacher = squad.teacher
        if teacher:
            teacher_name = teacher.first_name
            teacher_url = teacher.get_absolute_url()
        else:
            teacher_name = ''
            teacher_url = ''
        sq_cost = ''
        if squad.lesson_bill > 0:
            sq_cost = str(squad.lesson_bill)+' за урок | '
        if squad.bill > 0:
            sq_cost += str(squad.bill)+' в месяц | '
        if squad.course_bill > 0:
            sq_cost += str(squad.course_bill)+' за курс'
        res_squad = [squad.title,
            teacher_name,
            teacher_url,
            sq_cost]
        res_subjects = []
        for subject in squad.subjects.all():
            cost = str(subject.cost)
            if subject.cost_period == 'month':
                cost += " в месяц"
            elif subject.cost_period == 'lesson':
                cost += " за урок"
            elif subject.cost_period == 'course':
                cost += " за курс"
            color_back = subject.color_back
            if color_back == '':
                color_back = 'rgb(49, 58, 87)'
            res_subjects.append([subject.title, cost, color_back])
        for nm in squad.need_money.all():
            name = nm.card.name
            url = nm.card.card_user.get_absolute_url()
            fcs = nm.finance_closed.all()
            closed_months = 0
            first_present = '<i>Еще не было посещения</i>'
            if len(fcs) > 0:
                fc = fcs[0]
                closed_months = fc.closed_months
                first_present = 'Первое занятие: '
                first_present += fc.first_present.strftime('%d.%m.%Y')
            res.append([name,url,first_present,closed_months])

    data = {
        "res":res,
        "res_subjects":res_subjects,
        "res_squad":res_squad,
    }
    return JsonResponse(data)

def payday_change(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    pay_date = False
    if request.GET.get('student') and request.GET.get('squad') and request.GET.get('paydate'):
        ok = True
        student = school.people.get(id=int(request.GET.get('student')))
        squad = school.groups.get(id = int(request.GET.get('squad')))
        card = student.card.get(school=school)
        nm = card.need_money.get(squad=squad)
        nm.pay_day = int(request.GET.get('paydate').split('-')[-1])
        nm.save()
        pay_date = get_pay_date(nm).strftime('%d %B')
    data = {
        "pay_date":pay_date
    }
    return JsonResponse(data)

def show_finance_update(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    school = is_moderator_school(request, profile)    
    data = {
        "author":school.money_update_person,
        "date":school.money_update_date.strftime('%d %B'),
    }
    return JsonResponse(data)

def update_finance(request):
    ok = False
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    school = is_moderator_school(request, profile)    
    school.money_update_person = profile.first_name
    school.money_update_date = timezone.now()
    school.money = 0
    school.save()
    data = {
        "ok":True,
        "author":profile.first_name,
        "date":timezone.now().strftime('%d %B'),
    }
    return JsonResponse(data)