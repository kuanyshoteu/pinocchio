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
from squads.models import Squad
from squads.views import remove_student_from_squad, add_student_to_squad
from papers.models import *
from library.models import Folder
from accounts.models import Profile, Corruption, Zaiavka
from accounts.forms import *
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
    school = profile.schools.first()
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
    }
    return render(request, "school/school_rating.html", context)

def school_payments(request):
    profile = get_profile(request)
    only_managers(profile)
    school = profile.schools.first()
    context = {
        "profile":profile,
        "instance": profile.schools.first(),
        "squads":school.groups.all(),
        "payments":True,
        "subject_categories":school.school_subject_categories.all(),
        "subject_ages":school.school_subject_ages.all(),
        "all_students":school.people.filter(),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
    }
    return render(request, "school/school_payments.html", context)

def school_info(request):
    profile = get_profile(request)
    only_directors(profile)
    school = profile.schools.first()
    context = {
        "profile":profile,
        "instance": profile.schools.first(),
        "squads":school.groups.all(),
        "main_school":True,
        "subjects":school.school_subjects.all(),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
    }
    return render(request, "school/info.html", context)

def school_salaries(request):
    profile = get_profile(request)
    only_directors(profile)
    school = profile.schools.first()
    context = {
        "profile":profile,
        "instance": school,
        "salaries":True,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
    }
    return render(request, "school/salaries.html", context)

def school_crm(request):
    profile = get_profile(request)
    only_managers(profile)
    school = profile.schools.first()
    time_periods = school.time_periods.all()
    context = {
        "profile":profile,
        "instance": profile.schools.first(),
        "columns":school.crm_columns.all(),
        "subject_categories":school.school_subject_categories.all(),
        "ages":school.school_subject_ages.all(),
        "offices":school.school_offices.all(),
        'days':Day.objects.all(),
        'time_periods':time_periods,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
    }
    return render(request, "school/crm.html", context)

def school_crm_reg(request):
    profile = get_profile(request)
    only_managers(profile)
    school = profile.schools.first()
    time_periods = school.time_periods.all()

    context = {
        "profile":profile,
        "instance": profile.schools.first(),
        "columns":school.crm_columns.all(),
        "subject_categories":school.school_subject_categories.all(),
        "ages":school.school_subject_ages.all(),
        "offices":school.school_offices.all(),
        'days':Day.objects.all(),
        'time_periods':time_periods,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "open_form":True,
    }
    return render(request, "school/crm.html", context)

def school_students(request):
    profile = get_profile(request)
    only_managers(profile)
    school = profile.schools.first()    
    context = {
        "profile":profile,
        "instance": profile.schools.first(),
        "all_students":school.people.filter(),
        "students":"students",
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
    }
    return render(request, "school/all_students.html", context)

def school_requests(request):
    profile = get_profile(request)
    only_managers(profile)
    school = profile.schools.first()
    context = {
        "profile":profile,
        "instance": profile.schools.first(),
        "all_students":school.zaiavkas.all(),
        "requests":"requests",
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
    }
    return render(request, "school/all_students.html", context)

def school_recalls(request):
    profile = get_profile(request)
    only_managers(profile)
    school = profile.schools.first()
    context = {
        "profile":profile,
        "instance": school,
        "all_students":school.people.filter(),
        "recalls":"recalls",
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
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
    }


    return render(request, "schools/school_list.html", context)

def school_update(request, slug=None):
    instance = get_object_or_404(School, slug=slug)
    form = SchoolForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if not instance.height_field:
            instance.height_field = 0
        if not instance.width_field:
            instance.width_field = 0

        instance.save()
        return HttpResponseRedirect(instance.get_update_url())
        
    profile = get_profile(request)

    context = {
        "instance": instance,
        "form":form,
        "profile":profile,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
    }
    return render(request, "schools/school_create.html", context)

def school_delete(request):
    if not request.user.is_authenticated:
        raise Http404
    try:
        instance = School.objects.get(slug=slug)
    except:
        raise Http404

    if not request.user.is_staff and not request.user.is_superuser:
        reponse.status_code = 403
        return HttpResponse("You do not have permission to do this.")
        
    if request.method == "POST":
        instance.delete()
        messages.success(request, "Successfully deleted")
        return redirect("schools:list")
    context = {
        "object": instance
    }
    return render(request, "confirm_delete.html", context)

def subject_create(request):
    manager_profile = Profile.objects.get(user = request.user.id)
    only_managers(manager_profile)
    create_url = ''
    delete_url = ''
    if request.GET.get('id') and request.GET.get('title'):
        school = manager_profile.schools.first()
        if school.school_subject_categories.filter(title = request.GET.get('title')):
            return JsonResponse({'taken_name':True})
        if request.GET.get('id') == '_new':
            subject = school.school_subject_categories.create(school = school, title=request.GET.get('title'))
            school.hashtags.create(title = request.GET.get('title').replace(' ', '_'))
        else:
            subject = school.school_subject_categories.get(id=int(request.GET.get('id')))
            hashtag = school.hashtags.filter(title = subject.title.replace(' ', '_'))
            if len(hashtag) > 0:
                hashtag.title = request.GET.get('title').replace(' ', '_')
                hashtag.save()
            else:
                school.hashtags.create(title=request.GET.get('title').replace(' ', '_'))
            subject.title = request.GET.get('title')
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
    school = profile.schools.first()
    only_managers(profile)
    subject = school.school_subject_categories.get(id=int(request.GET.get('id')))
    hashtag = school.hashtags.filter(title = subject.title.replace(' ', '_'))
    if len(hashtag) > 0:
        hashtag.delete()
    subject.delete()
    data = {
    }
    return JsonResponse(data)

def age_create(request):
    manager_profile = Profile.objects.get(user = request.user.id)
    only_managers(manager_profile)
    create_url = ''
    delete_url = ''
    if request.GET.get('id') and request.GET.get('title'):
        school = manager_profile.schools.first()
        if school.school_subject_ages.filter(title = request.GET.get('title')):
            return JsonResponse({'taken_name':True})
        if request.GET.get('id') == '_new':
            age = school.school_subject_ages.create(school = school, title=request.GET.get('title'))
            school.hashtags.create(title = request.GET.get('title').replace(' ', '_'))
        else:
            age = school.school_subject_ages.get(id=int(request.GET.get('id')))
            hashtag = school.hashtags.filter(title = age.title.replace(' ', '_'))
            if len(hashtag) > 0:
                hashtag.title = request.GET.get('title').replace(' ', '_')
                hashtag.save()
            else:
                school.hashtags.create(title=request.GET.get('title').replace(' ', '_'))
            age.title = request.GET.get('title')
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
    school = profile.schools.first()
    only_managers(profile)
    age = school.school_subject_ages.get(id=int(request.GET.get('id')))
    hashtag = school.hashtags.filter(title = age.title.replace(' ', '_'))
    if len(hashtag) > 0:
        hashtag.delete()
    age.delete()
    data = {
    }
    return JsonResponse(data)

def office_create(request):
    manager_profile = Profile.objects.get(user = request.user.id)
    only_managers(manager_profile)
    create_url = ''
    delete_url = ''
    if request.GET.get('id') and request.GET.get('title'):
        school = manager_profile.schools.first()
        if school.school_offices.filter(title = request.GET.get('title')):
            return JsonResponse({'taken_name':True})
        if request.GET.get('id') == '_new':
            office = school.school_offices.create(school = school, title=request.GET.get('title'))
            school.hashtags.create(title = request.GET.get('title').replace(' ', '_'))
        else:
            office = school.school_offices.get(id=int(request.GET.get('id')))
            hashtag = school.hashtags.filter(title = office.title.replace(' ', '_'))
            if len(hashtag) > 0:
                hashtag.title = request.GET.get('title').replace(' ', '_')
                hashtag.save()
            else:
                school.hashtags.create(title=request.GET.get('title').replace(' ', '_'))
            office.title = request.GET.get('title')
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
    school = profile.schools.first()
    only_managers(profile)
    office = school.school_offices.get(id=int(request.GET.get('id')))
    hashtag = school.hashtags.filter(title = office.title.replace(' ', '_'))
    if len(hashtag) > 0:
        hashtag.delete()
    office.delete()
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
    school = manager_profile.schools.first()
    password = ''
    add = True
    if request.GET.get('id') and request.GET.get('squad_id'):
        card = school.crm_cards.get(id = int(request.GET.get('id')))
        if card.saved == False:
            new_id = User.objects.order_by("id").last().id + 1
            password = random_password()
            user = User.objects.create(username='user' + str(new_id))
            user.set_password(password)
            user.save()
            card.saved = True
            profile = Profile.objects.get(user = user)
            profile.first_name = card.name
            profile.phone = card.phone
            profile.mail = card.mail
            profile.save()
            card.card_user = profile
            card.author_profile = manager_profile
            card.save()
            profile.schools.add(school)
            squad_id = int(request.GET.get('squad_id'))
            if squad_id > 0:
                squad = Squad.objects.get(id=squad_id)
                squad.students.add(profile)
                for subject in squad.subjects.all():
                    subject.students.add(profile)
                for lecture in squad.squad_lectures.all():
                    lecture.people.add(profile)
                for timep in school.time_periods.all():
                    timep.people.add(profile)

                hist = CRMCardHistory.objects.create(
                    action_author = manager_profile,
                    card = card,
                    edit = '*** Регистрация в ' + squad.title + ' ***',
                    )
        else:
            profile = card.card_user
            card.author_profile = manager_profile
            card.save()
            squad_id = int(request.GET.get('squad_id'))
            if squad_id > 0:
                squad = Squad.objects.get(id=squad_id)
                if profile in squad.students.all():
                    add = False
                    remove_student_from_squad(profile, squad)
                else:
                    add_student_to_squad(profile, squad)

                hist = CRMCardHistory.objects.create(
                    action_author = manager_profile,
                    card = card,
                    edit = '*** Регистрация в ' + squad.title + ' ***',
                    )
    data = {
        'password':password,
        'add':add,
    }
    return JsonResponse(data)

def crm_option(request):
    profile = Profile.objects.get(user = request.user.id)
    if request.GET.get('object_id') and request.GET.get('option'):
        if request.GET.get('option') == 'subject':
            if int(request.GET.get('object_id')) == -1:
                profile.crm_subject = None
            else:
                subject = SubjectCategory.objects.get(id = int(request.GET.get('object_id')))
                profile.crm_subject = subject
        if request.GET.get('option') == 'age':
            if int(request.GET.get('object_id')) == -1:
                profile.crm_age = None
            else:
                age = SubjectAge.objects.get(id = int(request.GET.get('object_id')))
                profile.crm_age = age
        if request.GET.get('option') == 'office':
            if int(request.GET.get('object_id')) == -1:
                profile.crm_office = None
            else:
                office = Office.objects.get(id = int(request.GET.get('object_id')))
                profile.crm_office = office
        if request.GET.get('option') == 'group':
            profile.rating_squad_choice.clear()
            if int(request.GET.get('object_id')) != -1:
                squad = Squad.objects.get(id = int(request.GET.get('object_id')))
                profile.rating_squad_choice.add(squad)
        profile.save()
    data = {
    }
    return JsonResponse(data)

def move_card(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    if request.GET.get('card_id') and request.GET.get('column_id'):
        school = profile.schools.first()
        column = school.crm_columns.get(id = int(request.GET.get('column_id')))
        card = school.crm_cards.get(id = int(request.GET.get('card_id')))
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
    if request.GET.get('id') and request.GET.get('name') and request.GET.get('phone') and request.GET.get('mail'):
        school = profile.schools.first()
        card = school.crm_cards.get(id = int(request.GET.get('id')))
        edit = '***Редактирование*** '
        if card.name != request.GET.get('name'):
            edit = edit + "Имя: " + card.name + " -> " + request.GET.get('name') + "; "
        if card.phone != request.GET.get('phone'):
            edit = edit + "Номер: " + card.phone + " -> " + request.GET.get('phone') + "; "
        if card.mail != request.GET.get('mail'):
            edit = edit + "Почта: " + card.mail + " -> " + request.GET.get('mail') + "; "
        if card.comments != request.GET.get('comment'):
            edit = edit + "Коммент: " + card.comments + " -> " + request.GET.get('comment') + "; "
        card.name = request.GET.get('name')
        card.phone = request.GET.get('phone')
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
    print(request.GET.get('id'), profile.schools.first().title)
    if request.GET.get('id'):
        school = profile.schools.first()
        card = school.crm_cards.get(id = int(request.GET.get('id')))
        for history in card.history.all():
            res.append([history.action_author.first_name, history.action_author.get_absolute_url(), history.timestamp.strftime('%d.%m.%Y %H:%M') ,history.oldcolumn,history.newcolumn, history.edit])
    data = {
        'res':res,
    }
    return JsonResponse(data)

def add_card(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    if request.GET.get('id') and request.GET.get('name') and request.GET.get('phone') and request.GET.get('mail'):
        school = profile.schools.first()
        column = school.crm_columns.get(id = int(request.GET.get('id')))
        card = school.crm_cards.create(
            author_profile=profile,
            name = request.GET.get('name'),
            phone = request.GET.get('phone'),
            mail = request.GET.get('mail'),
            comments = request.GET.get('comment'),
            column = column,
            school = school,
        )
        card.save()
        hist = CRMCardHistory.objects.create(
            action_author = profile,
            card = card,
            edit = '***Создание карточки***',
            )
        hist.save()
    data = {
        "card_id":card.id,
        "card_name":card.name,
        "card_date":card.timestamp.date().strftime('%d.%m.%Y'),
        "card_phone":card.phone,
        "card_mail":card.mail,
        "card_comment":card.comments,
    }
    return JsonResponse(data)

def save_salary(request):
    profile = Profile.objects.get(user = request.user.id)
    only_directors(profile)
    if request.GET.get('id') and request.GET.get('salary'):
        worker = Profile.objects.get(id=int(request.GET.get('id')))
        worker.salary = int(request.GET.get('salary'))
        worker.save()
    data = {
    }
    return JsonResponse(data)

def save_job_salary(request):
    profile = Profile.objects.get(user = request.user.id)
    school = profile.schools.first()
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
    school = profile.schools.first()
    if request.GET.get('id'):
        card = school.crm_cards.get(id=int(request.GET.get('id')))
        if not card.saved:
            card.delete()
    data = {
    }
    return JsonResponse(data)

def show_free_cards(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    school = profile.schools.first()
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
    profile = card.card_user
    res = []
    if profile:
        for squad in profile.squads.all():
            res.append(squad.id)
    data = {
        'res':res,
    }
    return JsonResponse(data)

def take_card(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)    
    card = CRMCard.objects.get(id=int(request.GET.get('id')))
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
    if len(card.days_of_weeks) < 7:
        card.days_of_weeks = [False,False,False,False,False,False,False]
    if card.days_of_weeks[int(request.GET.get('id'))]:
        card.days_of_weeks[int(request.GET.get('id'))] = False
    else:
        card.days_of_weeks[int(request.GET.get('id'))] = True
        status = 'yes'
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
    res = 'empty'
    if text != '':
        text = text[::-1]
        res = []
        school = profile.schools.first()
        kef = 1
        if len(text) > 4:
            kef = 4
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
