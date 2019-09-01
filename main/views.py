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
from schools.views import get_social_networks

def loaderio(request):
    context = {
    }
    return render(request, "loaderio.txt", context)

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
        "schools":School.objects.all(),
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
    }
    return render(request, "about.html", context)

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
        skill = profile.skill
        print(skill.confirmation_code, request.GET.get('conf'), skill.confirmation_time)
        if request.GET.get('conf') == skill.confirmation_code and timezone.now()-skill.confirmation_time < timedelta(1):
            pid = profile.id
        else:
            return render(request, "er404.html", {})
    context = {
        "pid":pid,
    }
    return render(request, "profile/reset_pswd.html", context)

def moderator(request):
    cts = SubjectCategory.objects.all()
    cta = SubjectAge.objects.all()
    ctl = SubjectLevel.objects.all()
    for subject in Subject.objects.all():
        school = subject.school
        school.school_subject_categories.remove(*cts)
        school.school_subject_ages.remove(*cta)
        school.school_subject_levels.remove(*ctl)
        for category in subject.category.all():
            school.school_subject_categories.add(category)
        for age in subject.age.all():
            school.school_subject_ages.add(age)
        for level in subject.level.all():
            school.school_subject_ages.add(age)
    profile = get_profile(request)
    profession = Profession.objects.get(title = 'Moderator')
    if not profession in profile.profession.all():
        raise Http404
    context = {
        "profile":profile,
    }
    return render(request, "moderator.html", context)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse

def create_school(request):
    ok = False
    password = False
    profile = get_profile(request)
    profession = Profession.objects.get(title = 'Moderator')
    if request.GET.get('title') and request.GET.get('slogan') and request.GET.get('name') and request.GET.get('phone'):
        school = School.objects.create(
            title=request.GET.get('title'),
            slogan=request.GET.get('slogan'),
            version=request.GET.get('version'),
            worktime='По предварительной записи',
            )
        school.save()
        for column in CRMColumn.objects.all():
            school.crm_columns.add(column)
        new_id = str(User.objects.order_by("id").last().id + 1)
        new_name = request.GET.get('name').replace(' ', '')+new_id
        password = random_password()
        user = User.objects.create(username=new_name, password=password)
        user.set_password(password)
        user.save()
        user2 = authenticate(username = str(user.username), password=password)
        profile = Profile.objects.get(user = user)
        profile.first_name = request.GET.get('name')
        profile.phone = request.GET.get('phone')
        director = Profession.objects.get(title = 'Director')
        profile.profession.add(director)
        profile.is_student = False
        skill = Skill.objects.create(
            confirmed=True,
            confirmation_time=timezone.now(),
            )
        skill.save()
        profile.skill = skill
        profile.save()
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
        if len(Profile.objects.filter(mail=request.GET.get('username'))) > 0:
            profile = Profile.objects.filter(mail=request.GET.get('username'))[0]
            found = True
        elif len(Profile.objects.filter(phone=request.GET.get('username'))) > 0:
            profile = Profile.objects.filter(phone=request.GET.get('username'))[0]
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
    if request.GET.get('name') and request.GET.get('phone') and request.GET.get('password1') and request.GET.get('password2'):
        if request.GET.get('password1') == request.GET.get('password2'):
            if len(Profile.objects.filter(mail=request.GET.get('phone'))) == 0 and len(Profile.objects.filter(phone=request.GET.get('phone'))) == 0:
                new_id = str(User.objects.order_by("id").last().id + 1)
                new_name = request.GET.get('name').replace(' ', '')+new_id
                user = User.objects.create(username=new_name, password=request.GET.get('password1'))
                user.set_password(request.GET.get('password1'))
                user.save()
                user2 = authenticate(username = str(user.username), password=str(request.GET.get('password1')))
                try:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                except Exception as e:
                    res = 'er'
                    data = {
                        'res':res,
                    }
                    return JsonResponse(data)
                profile = Profile.objects.get(user = user)
                profile.first_name = request.GET.get('name')
                profile.phone = request.GET.get('phone')
                profile.mail = request.GET.get('mail')
                profile.save()
            else:
                res = 'second_user'
        else:
            res = 'not_equal_password'

    data = {
        'res':res,
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
            skill = profile.skill
            skill.confirmation_code = confirmation_code
            skill.confirmation_time = timezone.now()
            skill.save()
            url = request.build_absolute_uri().replace(request.get_full_path(), '') + '/reset_pswrd_view/?id='+str(profile.id)+'&conf='+confirmation_code
            text = "Здравствуйте "+profile.first_name+ "!<br><br>Чтобы поменять пароль пройдите по ссылке: <a href='"+url+"'>восстановить пароль</a>"
            html_content = text
            try:
                send_email("bilimtap.kz восстановление пароля", html_content, [request.GET.get('mail')])
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
            print(profile.first_name)
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
    i = 0
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
            if len(school.school_offices.all()) > 0:
                res.append([school.id, school.title, image_url, school.school_offices.first().address, school.slogan])
                i+=1
            if i == 10:
                break
    else:
        schools = School.objects.filter(version='full')
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

def get_notifications(request):
    profile = Profile.objects.get(user = request.user.id)
    timezone.now()
    res = []
    i = 0
    skill = profile.skill
    skill.notifications_number = 0
    skill.save()
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
        "school_money":profile.schools.first().money,
    }
    return render(request, "contacts.html", context)

def map_view(request):
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
        "schools":School.objects.all(),
        "schools_all":School.objects.all(),
        "url":School.objects.first().get_landing(),
        'is_trener':is_trener,
        "is_manager":is_manager,
        "is_director":is_director, 
        "subjects":SubjectCategory.objects.all(),
        "ages":SubjectAge.objects.all(),
        "school_money":money,
        "map_view":True,
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

from django.shortcuts import render_to_response
from django.template import RequestContext
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
    if request.GET.get('code') == 'nfrejkNWcsdkls588w5sdkewdhs':
        send_email('Bilimtap Заявка', "Имя: " + request.GET.get('name')+" Номер: "+request.GET.get('phone'), ['aaa.academy.kz@gmail.com'])
    data={}
    return JsonResponse(data)

def robots(request):
    return render(request,'robots.txt', {})

def sitemap(request):
    return render(request,'Sitemap.xml', {})
