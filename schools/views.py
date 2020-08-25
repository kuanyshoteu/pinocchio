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
from subjects.templatetags.ttags import get_date, get_pay_date,constant_school_lectures, material_number_by_date
from squads.views import remove_student_from_squad, add_student_to_squad, prepare_mail, update_payment_notices
from papers.models import *
from accounts.models import Profile,CRMCardHistory
from accounts.forms import *
from accounts.views import add_money
from .send_mails import *
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.contrib.auth.models import User
import os
from constants import *
from .social_media import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse
import json
import urllib
from django.contrib.postgres.search import TrigramSimilarity
from dateutil.relativedelta import relativedelta

def mails(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    check_school_version(school, 'business')
    default_templates = MailTemplate.objects.filter(default=True)
    school_templates = school.mail_templates.all()
    mail_templates = set(chain(default_templates, school_templates))
    context = {
        "profile":profile,
        "instance": school,
        "squads":school.groups.filter(shown=True),
        "subject_categories":school.school_subject_categories.all(),
        "subjects":school.school_subjects.all(),
        "mail_templates":mail_templates,
        "is_trener":is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
        "page":"mails",
    }
    return render(request, "mails/mails.html", context)

def connect_site(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    check_school_version(school, 'business')
    context = {
        "profile":profile,
        "instance": school,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
        "page":"info",
        "connect_site":True,
    }
    return render(request, "school/connect_site.html", context)

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
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
        "page":"payments",
        "hint":profile.hint_numbers[3],
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
    if school.version == 'business':
        for column in school.crm_columns.all().order_by('-id'):
            if column.id != 6:
                x = len(all_cards.filter(column=column))
                number += x
                if number_of_all > 0:
                    percent = round((number/number_of_all)*100,2)
                else:
                    percent = 0
                voronka.append([column.title, number, percent])
                voronka2.append([column.title, number, percent])
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
        "all_students_len":len(school.people.filter(is_student=True, squads__in=school.groups.filter(shown=True)).exclude(card=None).exclude(squads=None).distinct()),
        "managers":managers,
        "teachers":teachers,
        "voronka_array":voronka,
        "voronka2":voronka2,
        "worktime1":worktime1,
        "worktime2":worktime2,
        "number_of_all":number_of_all,
        "social_networks":get_social_networks(school),
        "page":"info",
        "info_data":"info_data",
        "hint":profile.hint_numbers[0],
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
    manager_prof = Profession.objects.get(title='Manager')
    managers = school.people.filter(profession=manager_prof)
    teacher_prof = Profession.objects.get(title='Teacher')
    teachers = school.people.filter(profession=teacher_prof)
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
        "teachers":teachers,
        "managers":managers,
        "page":"info",        
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
    sm = SocialMedia.objects.get(title='Instagram')
    insta = school.socialmedias.filter(socialmedia=sm)
    had_insta = False
    if len(insta) > 0:
        had_insta = True
        insta = insta[0]
    if request.GET.get('code'):
        code = request.GET.get('code')
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
        url = 'https://oauth.vk.com/authorize?client_id=' + vk_id + '&display=page&redirect_uri='+vk_server+'&group_ids='+vk.groupid+'&scope=messages,manage&response_type=code&v=5.103'
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
        sm = SocialMedia.objects.get(title='Вконтакте')
        if a['type'] == 'confirmation':
            group_id = str(a['group_id'])
            vks = SocialMediaAccount.objects.filter(groupid=group_id)
            if len(vks) > 0:
                vk = vks[0]
                confirmation_code = vk.confirmation_code
                print('return confirmation', confirmation_code)
            return HttpResponse(confirmation_code, content_type='text/plain')
        else:
            print("0 0 0 MESSAGE 0 0 0 0")
            if a['type'] == 'message_new':
                message = a['object']['message']
                fwd_messages = message['fwd_messages']
            elif a['type'] == 'wall_reply_new':
                message = a['object']
                fwd_messages = message['parents_stack']
            group_id = str(a['group_id'])
            vks = SocialMediaAccount.objects.filter(groupid=group_id)
            if len(vks) > 0:
                vk = vks[0]
                user_id = message['from_id']
                username = vk_get_user(user_id,vk.group_access_token)
                text = message['text']
                date = message['date']
                print(text, username,fwd_messages)
                school = vk.school
                search_card = school.crm_cards.filter(social_media_id='vk'+str(user_id))
                if len(search_card) == 0:
                    card = school.crm_cards.create(
                        column=school.crm_columns.first(),
                        name=username,
                        color='greencard',
                        social_media_id='vk'+str(user_id)
                        )
                    card.save()
                    search_card = [card]
                for card in search_card:
                    card.mails.create(
                        text=text,
                        method='vk',
                        is_client=True,
                        social_media=vk,
                        )
    return HttpResponse('ok', content_type='text/plain')

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
        for i in range(0, len(servers)):
            print('deleting servers', i)
            server = servers[i]
            vk_delete_server(groupid, server, group_access_token)
    secretkey = random_secrete_confirm()
    print('adding server to vk')
    server_id = vk_add_server(groupid, secretkey, group_access_token)

    # api_version = vk_get_callback_api_version(groupid,server_id,group_access_token)
    vk_set_callback_settings(groupid, server_id,'5.103',group_access_token)
    print('group_id', groupid, 'server_id',server_id)
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
        "hint":profile.hint_numbers[1],
        "page":"crm",
    }
    return render(request, "school/crm.html", context)

def add_subject_category_work(school, title):
    qs = SubjectCategory.objects.filter(title=title)
    if len(qs) > 0:
        subject = qs[0]
        school.school_subject_categories.add(subject)
        school_cats = subject.school_categories.all()
        school.categories.add(*school_cats)
    else:
        subject = school.school_subject_categories.create(title=title)
    school.hashtags.get_or_create(title = title.replace(' ', '_'))
    return subject

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
            subject = add_subject_category_work(school, title)
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
    data = {
    }
    return JsonResponse(data)
    
def create_cabinet(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    cid = -1
    if request.GET.get('title') != '':
        school = is_moderator_school(request, profile)
        capacity = 100
        if request.GET.get('capacity'):
            capacity = int(request.GET.get('capacity'))
        if request.GET.get('id') == '-1':
            cabinet = school.cabinets.create(
                title=request.GET.get('title'),
                capacity=capacity,
                )
        else:
            cabinet = school.cabinets.get(id=int(request.GET.get('id')))
            cabinet.title = request.GET.get('title')
            cabinet.capacity=capacity
        cabinet.save()
        cid = cabinet.id
    data = {
        "cid":cid,
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
        filter_data = profile.filter_data
        # if request.GET.get('option') == 'filter_subject_category':
        #     if int(request.GET.get('object_id')) == -1:
        #         filter_data.subject_category = None
        #     else:
        #         category = SubjectCategory.objects.get(id = int(request.GET.get('object_id')))
        #         filter_data.subject_category = category
        # if request.GET.get('option') == 'office':
        #     if int(request.GET.get('object_id')) == -1:
        #         filter_data.office = None
        #     else:
        #         office = Office.objects.get(id = int(request.GET.get('object_id')))
        #         filter_data.office = office
        if request.GET.get('option') == 'group':
            if int(request.GET.get('object_id')) != -1:
                squad = Squad.objects.get(id = int(request.GET.get('object_id')))
                filter_data.squad = squad
            else:
                filter_data.squad = None                
        if request.GET.get('option') == 'filter_subject':
            if int(request.GET.get('object_id')) != -1:
                subject = Subject.objects.get(id = int(request.GET.get('object_id')))
                filter_data.subject = subject
            else:
                filter_data.subject = None                
        if request.GET.get('option') == 'teacher':
            if int(request.GET.get('object_id')) != -1:
                teacher = profile.schools.first().people.get(id = int(request.GET.get('object_id')))
                filter_data.teacher = teacher
            else:
                filter_data.teacher = None                
        if request.GET.get('option') == 'payment':
            filter_data.payment = request.GET.get('object_id')
        if request.GET.get('option') == 'subject_type':
            filter_data.subject_type = request.GET.get('object_id')
        filter_data.save()
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
        filter_data = manager.filter_data
        office = Office.objects.get(id = int(request.GET.get('office')))
        hisoffice = filter_data.office 
        if office == hisoffice:
            filter_data.office = None            
        else:
            added = True
            filter_data.office = office
        filter_data.save()
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
    if request.GET.get('id') and request.GET.get('text'):
        school = is_moderator_school(request, profile)
        card = school.crm_cards.get(id = int(request.GET.get('id')))
        head = school.title
        text = request.GET.get('text')
        method = ''
        if '@' in request.GET.get('mail'):
            send_email(head, text,[request.GET.get('mail')])
            method = card.mail
        elif request.GET.get('social_media_id'):
            smid = request.GET.get('social_media_id')
            print('smid0', smid)
            if smid[0]+smid[1] == 'vk':
                smid = smid[2:]
                print('smid1', smid)
                sm = SocialMedia.objects.get(title='Вконтакте')
                vk = school.socialmedias.filter(socialmedia=sm)
                if len(vk) > 0:
                    vk = vk[0]
                    print('foundvk', vk)
                    vk_send_message(vk, text, int(smid))
                    print('sended', text)
                    method = 'vk'+smid
        ok = True
        time = timezone.now()
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
    if request.GET.get('id'):
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
    if card.comments != request.GET.get('birthday'):
        old_birthday = card.birthday
        if not old_birthday:
            old_birthday = 'Пусто'
        edit = edit + "День рождения: " + str(old_birthday) + " -> " + request.GET.get('birthday') + "; "
    if student:
        student.save()
    card.name = request.GET.get('name')
    card.phone = request.GET.get('phone')
    card.extra_phone = request.GET.get('extra_phone')
    card.parents = request.GET.get('parents')
    card.comments = request.GET.get('comment')
    if request.GET.get('birthday') == '':
        card.birthday = None
    else:
        card.birthday = request.GET.get('birthday')
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
        if password:
            user.set_password(password)
        user.save()
        profile = Profile.objects.create(user = user)
        profile.first_name = card.name
        profile.phone = card.phone
        profile.mail = card.mail
    card.author_profile = manager_profile
    card.timestamp = timezone.now()
    if squad_id > 0:
        card.last_groups = squad_id
    card.card_user = profile
    card.saved = True
    card.save()
    profile.schools.add(school)
    skill = Skill.objects.create()
    profile.hint_numbers = [0, 1, 1, 1, 1, 1, 1]
    profile.skill = skill
    profile.confirmation_time = timezone.now()
    profile.confirmed = False
    profile.save()
    return profile

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
        update_crm_notices(school)
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
        card.delete()
    data = {
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
    individual_subjects = []
    prefered_individual_subjects = []
    if profile:
        sqs = profile.squads.filter(shown=True)
        for squad in sqs:
            res.append(squad.id)
        for subject in school.school_subjects.filter(is_individual=True,squads__in=sqs):
            individual_subjects.append(subject.id)
        for subject in school.school_subjects.filter(is_individual=True,prefered_squads__in=sqs):
            print(subject.title)
            prefered_individual_subjects.append(subject.id)
    data = {
        'res':res,
        'individual_subjects':individual_subjects,
        'prefered_individual_subjects':prefered_individual_subjects,
    }
    return JsonResponse(data)

def get_card_info(request):
    bills = []
    if request.GET.get('id'):
        manager = Profile.objects.get(user = request.user.id)
        card = CRMCard.objects.get(id=int(request.GET.get('id')))
        only_managers(manager)
        school = card.school
        is_in_school(manager, school)
        profile = card.card_user
        nms = card.bill_data.select_related('squad')
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
        form_res = get_card_form_by_column(card, colid)
        dialog = get_card_dialog(card)
        if card.color == 'red':
            if card.author_profile == manager:
                card.color = 'white'
                card.save()
                number_of_free = len(school.crm_cards.filter(color='red', author_profile=None))
                fd = manager.filter_data
                number_of_manager = len(school.crm_cards.filter(color='red', author_profile = manager))
                fd.crm_notices = number_of_free + number_of_manager
                fd.save()
    data = {
        'bills':bills,
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
        if card.color == 'red':
            card.color = 'white'
            card.save()
            update_crm_notices(school)
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
            similarity=TrigramSimilarity('mail', text)
            cards = school.crm_cards.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
            for card in cards:
                res.append(card.mail)
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
            similarity=TrigramSimilarity('extra_phone', text)
            cards = school.crm_cards.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
            for card in cards:
                res.append(card.extra_phone)
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
        if request.GET.get('status') == 'cities':
            cities = request.GET.get('text').split(',')
            old_cities = school.cities.all()
            school.cities.remove(*old_cities)
            for city_title in cities:
                city = City.objects.filter(title=city_title)

                similarity=TrigramSimilarity('title', city_title)
                city = City.objects.annotate(similarity=similarity,).filter(similarity__gt=0.9).order_by('-similarity')
                if len(city) > 0:
                    city = city[0]
                else:
                    city = City.objects.create(title=city_title)
                school.cities.add(city)
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
                if number_of_all == 0:
                    percent = 0
                else:
                    percent = round((number/number_of_all)*100, 2)
                res.append([column.title, number, percent])
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
            check_school_version(school, 'business')
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
        check_school_version(school, 'business')
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
        res = column.cards.filter(school=school).select_related('card_user')
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
    column_cards_lens = []
    for column in school.crm_columns.all():
        query = column.cards.filter(school=school).select_related('card_user')
        column_cards_lens.append(len(query))
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
    all_columns = school.crm_columns.all()
    all_cards = school.crm_cards.filter(column__in=all_columns)
    all_cards_len = len(all_cards)
    number_of_free = len(all_cards.filter(color='red', author_profile=None))
    number_of_manager = len(all_cards.filter(color='red', author_profile = profile))
    individual_subjects = get_individual_subjects(school)
    my_cards_len = len(school.crm_cards.filter(author_profile=profile,column__in=all_columns))
    free_cards_len = len(school.crm_cards.filter(author_profile=None,column__in=all_columns))
    data = {
        "all_res":all_res,
        "page":2,
        "is_director":is_profi(profile, 'Director'),
        "managers_res":managers_res,
        "Ended":False,
        "number_of_free":number_of_free,
        "number_of_manager":number_of_manager,
        "all_cards_len":all_cards_len,
        "my_cards_len":my_cards_len,
        "free_cards_len":free_cards_len,
        "individual_subjects":individual_subjects,
        "column_cards_lens":column_cards_lens,
    }
    return JsonResponse(data)

def get_individual_subjects(school):
    res = []
    for s in school.school_subjects.filter(is_individual=True):
        res.append([s.id, s.title])
    return res

def create_individual_group(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    ok = False
    if request.GET.get('student_id') and request.GET.get('subject_id'):
        card = school.crm_cards.get(id=int(request.GET.get('student_id')))
        subject = school.school_subjects.get(id=int(request.GET.get('subject_id')))
        title = card.name+' - '+subject.title
        title = title[:45]
        title = create_squad_title(title, 1)
        new_squad = school.groups.create(
            title=title,
            content='Записан на прохождение курса '+subject.title,
            start_date=timezone.now().date(),
        )
        # if len(school.school_offices.all()) > 0:
        #     new_squad.office = new_squad.school.school_offices.first()
        new_squad.save()
        student = card.card_user
        if not student:
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
                ok_mail = prepare_mail(card.name, card.phone, card.mail, new_squad, None, True)
            else:
                ok_mail = prepare_mail(card.name, card.phone, card.mail, new_squad, password, True)
            hist = CRMCardHistory.objects.create(
                action_author = profile,
                card = card,
                edit = '*** Регистрация в ' + new_squad.title + ' ***',
                )
            student = register_new_student(found,card,password,profile,student,new_squad.id,school)

        add_student_to_squad(student, new_squad, profile)
        new_squad.prefered_subjects.add(subject)
        new_squad.squad_histories.create(action_author=profile,edit='Создана группа '+new_squad.title)
        ok = True
    data = {
        "ok":ok,
    }
    return JsonResponse(data)

def create_squad_title(title, i):
    last = len(Squad.objects.filter(title=title))
    if last > 0:
        title += str(i)
        title = create_squad_title(title, i+1)
    return title

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
            similarity=TrigramSimilarity('mail', text)
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
            print(extra)
            cards = set(chain(cards, extra))
        i = 0
        for card in cards:
            colid = card.column.id
            res.append([colid, get_card_data_by_column(card, colid)])
            i += 1
            if i == 5:
                break
    res.reverse()
    data = {
        'res':res,
    }
    return JsonResponse(data)

def filter_crm_cards_work(cards, request,all_squads,all_students):
    if len(request.GET.get('offices')) > 0:
        sids = request.GET.get('offices').split('d')
        del sids[-1]
        squads = all_squads
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
    all_columns = school.crm_columns.all()
    all_cards = school.crm_cards.filter(column__in=all_columns).select_related('card_user')
    all_cards_len = len(all_cards)
    if request.GET.get('kind') == 'freecards':
        all_cards = school.crm_cards.filter(author_profile=None).select_related('card_user')
    elif request.GET.get('kind') == 'mycards':
        all_cards = school.crm_cards.filter(author_profile=profile).select_related('card_user')
    all_squads = school.groups.all()
    all_students = school.people.filter(is_student=True).prefetch_related('squads')
    # all_offices = school.school_offices.all()
    all_res = []
    column_cards_lens = []
    for column in school.crm_columns.all():
        cards = all_cards.filter(column=column)
        column_cards_lens.append(len(cards))
        cards = filter_crm_cards_work(cards, request,all_squads,all_students)
        i = 0
        res = []
        colid = column.id
        for card in cards:
            i+=1
            if i == 10:
                break
            res += get_card_data_by_column(card, colid)
        all_res.append([colid,res])
    my_cards_len = len(school.crm_cards.filter(author_profile=profile, column__in=all_columns))
    free_cards_len = len(school.crm_cards.filter(author_profile=None, column__in=all_columns))
    data = {
        'all_res':all_res,
        'column_cards_lens':column_cards_lens,
        'all_cards_len':all_cards_len,
        'my_cards_len':my_cards_len,
        'free_cards_len':free_cards_len,
    }
    return JsonResponse(data)

def get_extra_cards(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    res = []
    school = is_moderator_school(request, profile)
    Ended = False
    if request.GET.get('column') and request.GET.get('page'):
        page = int(request.GET.get('page'))
        column = CRMColumn.objects.get(id=int(request.GET.get('column')))
        if request.GET.get('kind') == 'allcards':
            res = column.cards.filter(school=school).select_related('card_user')
        elif request.GET.get('kind') == 'freecards':
            res = column.cards.filter(author_profile=None,school=school).select_related('card_user')
        else:
            res = column.cards.filter(author_profile=profile,school=school).select_related('card_user')
        all_squads = school.groups.all()
        all_students = school.people.filter(is_student=True).prefetch_related('squads')
        res = filter_crm_cards_work(res, request,all_squads,all_students)
        print(len(res), (page)*10)
        if len(res) <= (page)*10:
            Ended = True
            print('last')
            if len(res) <= (page-1)*10:
                print('ended')
                return JsonResponse({'Ended':True})
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
        "page":page+1,
        "is_director":is_profi(profile, 'Director'),
        "managers_res":managers_res,
        "Ended":Ended,
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
                squad_color = ''
                if payment.squad:
                    squad_title = payment.squad.title
                    squad_color = payment.squad.color_back
                cancel_access = False
                if payment.timestamp > timezone.now() - timedelta(3):
                    cancel_access = True
                res.append([
                    payment.timestamp.strftime('%d %B %Y  %H:%M'), #0
                    payment.amount,                               #1
                    squad_title,                                  #2
                    payment.action_author.get_absolute_url(),     #3
                    payment.action_author.first_name,             #4
                    cancel_access,                                #5
                    payment.id,                                   #6
                    squad_color,                                  #7
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
        for nm in squad.bill_data.all():
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
    month_pay_notice = False
    wasred = False
    ok = False
    if request.GET.get('student') and request.GET.get('squad') and request.GET.get('paydate'):
        ok = True
        student = school.people.get(id=int(request.GET.get('student')))
        squad = school.groups.get(id = int(request.GET.get('squad')))
        card = student.card.get(school=school)
        nm = card.bill_data.get(squad=squad)
        today = timezone.now().date()
        if nm.pay_date > today + timedelta(school.bill_day_diff):
            wasred = False
        else:
            wasred = True
        nm.pay_date = datetime.datetime.strptime(request.GET.get('paydate'), "%Y-%m-%d").date()
        nm.save()
        if nm.pay_date > today + timedelta(school.bill_day_diff):
            month_pay_notice = False
        else:
            month_pay_notice = True
        lesson_pay_notice = False     
        if len(squad.subjects.filter(cost_period='lesson')) > 0:
            if nm.money < 2 * squad.lesson_bill:
                lesson_pay_notice = True
        update_payment_notices(school, today)
        pay_date = nm.pay_date.strftime('%d %B %Y')
    data = {
        "pay_date":pay_date,
        "payment_notices":profile.filter_data.payment_notices,
        "month_pay_notice":month_pay_notice,
        "lesson_pay_notice":lesson_pay_notice,
        "wasred":wasred,
        "ok":ok,
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

def get_payment_list(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    res = []
    today = timezone.now().date()
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
        school = is_moderator_school(request, profile)
        cards = school.crm_cards.select_related('card_user')
        students, squads = payment_get_students_list(profile, school)
        all_students_len = len(school.people.filter(is_student=True, squads__in=squads).exclude(card=None).exclude(squads=None).distinct())
        crnt_students_len = len(students)
        if len(students) <= (page-1)*16:
            return JsonResponse({"ended":True})
        p = Paginator(students, 16)
        page1 = p.page(page)
        res = []
        bill_day_diff = school.bill_day_diff
        squad = profile.filter_data.squad
        for student in page1.object_list:
            card = cards.filter(card_user=student)[0]
            if squad == None:
                squads2 = squads.filter(students=student)
            else:
                squads2 = squads
            sq_res, notices = payment_student_collect(squads2, card, today, bill_day_diff)
            res.append([
                student.id,
                student.first_name,
                student.get_absolute_url(),
                sq_res,
                notices,
                ])
    data = {
        "res":res,
        "crnt_students_len":crnt_students_len,
        "all_students_len":all_students_len,
        "today":today,
    }
    return JsonResponse(data)

def payment_get_students_list(profile, school):
    squad = profile.filter_data.squad
    squads = school.groups.filter(shown=True).prefetch_related('students')
    if squad != None:
        squads = school.groups.filter(id = squad.id)
    # else:
    #     if profile.filter_data.office:
    #         squads = school.groups.filter(shown=True,office=profile.filter_data.office).prefetch_related('students')
    # if profile.filter_data.subject_category:
    #     subjects = school.school_subjects.filter(category=profile.filter_data.subject_category)
    #     squads = squads.filter(subjects__in=subjects).distinct()
    print(school.people.filter(is_student=True))
    students = school.people.filter(is_student=True, squads__in=squads).exclude(card=None).exclude(squads=None).distinct()
    print(students)
    if profile.filter_data.payment != 'all':
        firstofmonth = first_day_of_month(timezone.now().date())
        lastofmonth = last_day_of_month(firstofmonth)
        payments = school.payment_history.filter(squad__in=squads,timestamp__gte=firstofmonth, timestamp__lte=lastofmonth)
        if profile.filter_data.payment == 'paid':
            students = students.filter(payment_history__in=payments).distinct()
        if profile.filter_data.payment == 'not_paid':
            students = students.exclude(payment_history__in=payments).distinct()
    return students, squads

def payment_student_collect(squads2, card, today, bill_day_diff):
    notices = 0
    sq_res = []
    for sq in squads2:
        nm = sq.bill_data.filter(card=card)
        pay_date = '-'
        pay_date_input = '-'
        pd = ''
        lesson_pay_notice = False
        month_pay_notice = False
        discount_res = ''
        if len(nm) > 0:
            nm = nm.last()
            pay_date_input = nm.pay_date.strftime("%Y-%m-%d")
            pay_date = nm.pay_date.strftime("%d %B %Y")
            if nm.pay_date <= today + timedelta(bill_day_diff):
                month_pay_notice = True
                notices += 1
            if len(sq.subjects.filter(cost_period='lesson')) > 0:
                if nm.money < 2 * sq.lesson_bill:
                    lesson_pay_notice = True
            if len(nm.discount_school.all()) > 0:
                discount = nm.discount_school.first()
                discount_res = str(discount.amount)
                if discount.discount_type == 'percent':
                    discount_res += '%'
                else:
                    discount_res += 'тг'
        lectures = sq.squad_lectures.all()
        days = Day.objects.filter(lectures__in=lectures).distinct()
        days_res = ''
        for day in days:
            days_res += str(day.number) + ','
        sq_res.append([
            sq.id,              #0
            sq.title,           #1
            sq.color_back,      #2
            pay_date_input,     #3
            pay_date,           #4
            month_pay_notice,   #5
            lesson_pay_notice,  #6
            days_res,           #7
            discount_res,       #8
            sq.get_update_url(),
            ])
    return sq_res, notices

def get_payment_student(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    res = []
    ok = False
    if request.GET.get('id'):
        school = is_moderator_school(request, profile)
        student = school.people.filter(is_student=True, id=int(request.GET.get('id')))
        if len(student) == 0:
            return JsonResponse({'ok':ok})
        student = student[0]
        if len(student.squads.all()) == 0:
            return JsonResponse({'ok':True, 'nosquad':True})
        card = school.crm_cards.filter(card_user=student)
        if len(card) == 0:
            return JsonResponse({'ok':ok})
        card = card[0]
        squads2 = school.groups.filter(students=student,shown=True)
        today = timezone.now().date()
        sq_res, notices = payment_student_collect(squads2, card, today, school.bill_day_diff)
        res.append([
            student.id,
            student.first_name,
            student.get_absolute_url(),
            sq_res,
            notices,
            ])
        ok = True
        students = payment_get_students_list(profile, school)[0]
        number = len(students.filter(id__lt=student.id)) + 1
    data = {
        "ok":ok,
        "res":res,
        "number":number,
    }
    return JsonResponse(data)

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)
def first_day_of_month(day):
    crnt_mnth = day.strftime('%m')
    crnt_year = day.strftime('%Y')
    firstofmonth = datetime.datetime.strptime('01-'+crnt_mnth+'-'+crnt_year,'%d-%m-%Y').date()
    return firstofmonth

def search_city(request):
    profile = Profile.objects.get(user = request.user.id)
    only_directors(profile)
    res = []
    if request.GET.get('text'):
        similarity=TrigramSimilarity('title', request.GET.get('text'))
        kef = 1
        if len(request.GET.get('text')) > 4:
            kef = 4
        objects = City.objects.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
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

def connect_site_api(request, school_id=None):
    if school_id:
        if request.GET.get('name') and request.GET.get('phone'):
            school = School.objects.get(id=school_id)
            check_school_version(school, 'business')
            found = False
            student = None
            if len(Profile.objects.filter(phone=request.GET.get('phone'))) > 0:
                found = True
                student = Profile.objects.filter(phone=request.GET.get('phone'))[0]
                card = student.card.get(school=school)
            if len(school.crm_cards.filter(phone=request.GET.get('phone'))) > 0:
                found = True
                student = False
                card = school.crm_cards.filter(phone=request.GET.get('phone'))[0]
            if found:
                card.comments += '; Оставлена заявка через сайт'
                card.color = 'red'
                card.save()
                return JsonResponse({})
            column = school.crm_columns.get(id = 1)
            saved = False
            if found:
                saved = True
            card = school.crm_cards.create(
                name = request.GET.get('name'),
                phone = request.GET.get('phone'),
                column = column,
                saved = saved,
                comments = 'Оставлена заявка через сайт',
                card_user = student,
                color = 'red'
            )
            card.save()
            update_crm_notices(school)
            hist = CRMCardHistory.objects.create(
                card = card,
                edit = '***Создание карточки***',
                )
            hist.save()
    data = {
    }
    return JsonResponse(data)

def update_crm_notices(school):
    all_cards = school.crm_cards.all() 
    number_of_free = len(all_cards.filter(color='red', author_profile=None))
    manager_prof = Profession.objects.get(title='Manager')
    dir_prof = Profession.objects.get(title='Director')
    managers = school.people.filter(profession__in=[manager_prof,dir_prof])
    for manager in managers:
        fd = manager.filter_data
        number_of_manager = len(all_cards.filter(color='red', author_profile = manager))
        fd.crm_notices = number_of_free + number_of_manager
        fd.save()

def search_for_payment(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    res = []
    res_squads = []
    res_subject_categories = []
    if request.GET.get('text'):
        school = is_moderator_school(request, profile)
        similarity=TrigramSimilarity('first_name', request.GET.get('text'))
        kef = 1
        if len(request.GET.get('text')) > 4:
            kef = 4
        students = school.people.filter(is_student=True).annotate(similarity=similarity).filter(similarity__gt=0.05*kef).order_by('-similarity')
        i = 0
        for student in students:
            res.append([student.id, student.first_name])
            i+=1
            if i == 5:
                break
        if i < 5:
            similarity=TrigramSimilarity('phone', request.GET.get('text'))
            kef = 1
            if len(request.GET.get('text')) > 4:
                kef = 4
            students = school.people.filter(is_student=True).annotate(similarity=similarity).filter(similarity__gt=0.05*kef).order_by('-similarity')
            i = 0
            for student in students:
                res.append([student.id, student.first_name])
                i+=1
                if i == 5:
                    break
            if i < 5:
                similarity=TrigramSimilarity('mail', request.GET.get('text'))
                kef = 1
                if len(request.GET.get('text')) > 4:
                    kef = 4
                students = school.people.filter(is_student=True).annotate(similarity=similarity).filter(similarity__gt=0.05*kef).order_by('-similarity')
                i = 0
                for student in students:
                    res.append([student.id, student.first_name])
                    i+=1
                    if i == 5:
                        break
                if i < 5:
                    similarity=TrigramSimilarity('mail', request.GET.get('text'))
                    kef = 1
                    if len(request.GET.get('text')) > 4:
                        kef = 4
                    students = school.people.filter(is_student=True).annotate(similarity=similarity).filter(similarity__gt=0.05*kef).order_by('-similarity')
                    i = 0
                    for student in students:
                        res.append([student.id, student.first_name])
                        i+=1
                        if i == 5:
                            break

    data = {
        'res':res,
    }
    return JsonResponse(data)

def get_attendance_calendar(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    res = []
    ok = False
    if request.GET.get('squad') and request.GET.get('student') and request.GET.get('getday'):
        getday = datetime.datetime.strptime(request.GET.get('getday'), "%Yz%mz%d").date()
        school = is_moderator_school(request, profile)
        student = school.people.filter(is_student=True, id=int(request.GET.get('student')))
        if len(student) == 0:
            return JsonResponse({'ok':ok})
        student = student[0]
        squad = school.groups.filter(shown=True,id=int(request.GET.get('squad')))
        if len(squad) == 0:
            return JsonResponse({'ok':ok})
        squad = squad[0]
        alldays = Day.objects.all()
        for subject in squad.subjects.all():
            dates = get_crnt_month(squad,subject, getday)
            res_subject = []
            subject_materials = subject.materials.all()
            subject_materials_len = len(subject_materials)
            for date in dates:
                mrl_nmb = material_number_by_date(date, squad, subject, alldays, None)
                if mrl_nmb > subject_materials_len:
                    break
                sm = list(subject_materials)[mrl_nmb-1]
                att = sm.sm_atts.filter(student=student,squad=squad)
                if len(att) > 0:
                    att = att[0]
                    res_subject.append([date, att.present])
                else:
                    res_subject.append([date, ''])
            res.append([subject.title, res_subject])
        ok = True
    data = {
        "res":res,
        "ok":ok,
    }
    return JsonResponse(data)

def get_crnt_month(squad, subject, getday):
    lectures = subject.subject_lectures.filter(squad = squad)  
    days = Day.objects.filter(lectures__in=lectures).distinct()
    ds = []
    for day in days:
        ds.append(day.number)
    today = timezone.now().date()
    crnt_mnth = getday.strftime('%m')
    crnt_year = getday.strftime('%Y') 
    firstofmonth = first_day_of_month(getday)
    lastofmonth = last_day_of_month(firstofmonth)
    dates = []
    i0 = firstofmonth - timedelta(int(firstofmonth.strftime('%w')) - 1)
    week_count = 0
    while i0 < lastofmonth:
        for d in ds:
            i1 = i0 + timedelta(d - 1)
            if today < i1:
                break
            dates.append(i1)
        if today < i1:
            break
        i0 += timedelta(7)
    return dates

def get_workers_list(request):
    pass

def connect_full_version(request):
    profile = Profile.objects.get(user = request.user.id)
    only_directors(profile)
    school = is_moderator_school(request, profile)
    ok = 'error'
    if school.version == 'business':
        ok = 'already'
        data = {"ok":ok}
    else:
        if len(school.subscribe_payments.all()) == 0:
            school.version = 'business'
            last_date = timezone.now()
            day = last_date.strftime('%d')
            mnth = last_date.strftime('%m')
            year = last_date.strftime('%Y')
            newmnth = int(mnth) + 6
            if newmnth > 12:
                newmnth -= 12
                year = str(int(year) + 1)
            if newmnth < 10:
                newmnth = '0' + str(newmnth)
            else:
                newmnth = str(newmnth)
            school.version_date = datetime.datetime.strptime(year+
                '-'+newmnth+'-'+day+' '+last_date.strftime('%H')+':'+last_date.strftime('%M'), "%Y-%m-%d %H:%M")
            school.save()
            ok = 'ok'
            school.subscribe_payments.create(
                author = profile.first_name,
                phone = profile.phone,
                transactionId = -1,
                amount = 0,
                currency = '',
                timestamp = timezone.now(),
                )
            data = {"ok":ok}
        else:
            ok = 'need_pay'
            invoiceId = '1'
            data = {
                "ok":ok,
                'publicId':cloudpayments_id,
                'invoiceId':invoiceId,
                'accountId':profile.id,
            }
    return JsonResponse(data)

def rename_column(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    if request.GET.get('id') and request.GET.get('name'):
        column = school.crm_columns.get(id = int(request.GET.get('id')))
        column.title = request.GET.get('name')
        column.save()
    data = {
    }
    return JsonResponse(data)
