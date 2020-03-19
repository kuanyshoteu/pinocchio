from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import RedirectView
from itertools import chain

from .forms import SubjectForm,SubjectForm2
from .models import *
from papers.models import *
from library.models import Folder
from accounts.models import Profile
from schools.models import School, Cabinet
from accounts.forms import *
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.contrib.auth.models import User
from constants import *

def subject_detail(request, slug=None):
    instance = get_object_or_404(Subject, slug=slug)
    profile = get_profile(request)
    days = Day.objects.all()
    cells = Cell.objects.all()
    school = instance.school
    is_in_school(profile, school)
    time_periods = school.time_periods.all()
    if len(cells) < len(days) * len(time_periods):
        for day in days:
            for timep in time_periods:
                new_cell = Cell.objects.get_or_create(day = day, time_period = timep, school=school)
    if profile.is_student:
        profile.squads.filter(shown=True)
    context = {
        "instance": instance,
        "profile":profile,
        'time_periods':time_periods,
        'days':days,
        'materials':instance.materials.prefetch_related('lessons'),
        "lessons":school.lessons.all(),
        "folders":school.school_folders.all(),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
        "page":"subjects",
    }
    return render(request, "subjects/subject_detail.html", context)

def subject_list(request):
    profile = get_profile(request)
    only_staff(profile)
    school = is_moderator_school(request, profile)
    subjects = school.school_subjects.all()
    if profile.skill.crm_subject2:
        subjects = subjects.filter(category=profile.skill.crm_subject2)
        
    context = {
        "profile": profile,
        "subjects":subjects,
        "subject_categories":school.school_subject_categories.all(),
        "school":school,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
        "page":"subjects",        
    }
    return render(request, "subjects/subject_list.html", context)

def subject_create(request):
    profile = get_profile(request)
    only_managers(profile)
    form = SubjectForm(request.POST or None, request.FILES or None)
    school = is_moderator_school(request, profile)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.school = school
        instance.cost_period = request.POST.get('get_subject_period')
        if not instance.cost:
            instance.cost = 0
        instance.save()
        instance.subject_histories.create(action_author=profile,edit='Создал курс '+instance.title)        
        return HttpResponseRedirect(instance.get_update_url())
    context = {
        "form": form,
        "profile":profile,
        "all_teachers":all_teachers(school),
        "subject_categories":school.school_subject_categories.all(),        
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
        "page":"subjects",
    }
    return render(request, "subjects/subject_create.html", context)

def subject_update(request, slug=None):
    instance = get_object_or_404(Subject, slug=slug)
    profile = get_profile(request)
    only_staff(profile)
    school = instance.school
    is_in_school(profile, school)
    old_title = instance.title
    old_content = instance.content
    form = SubjectForm(request.POST or None, request.FILES or None, instance=instance)
    change_time = False
    change_title = False
    change_content = False
    old_cost = instance.cost
    old_cost_period = instance.cost_period
    if form.is_valid():
        instance = form.save(commit=False)
        if old_title != instance.title:
            change_title = True
        if old_content != instance.content:
            change_content = True
        instance.cost_period = request.POST.get('get_subject_period')
        instance.save()
        text = 'Внесены изменения в курс "'+instance.title+'"'
        if change_title:
            text += '<br> Название '+old_title+' -> ' + instance.title 
        if change_content:
            text += '<br> Описание '+old_content+' -> ' + instance.content
        instance.subject_histories.create(action_author=profile,edit=text)        

        squads = instance.squads.prefetch_related('students')
        cost = instance.cost
        cards = school.crm_cards.all()
        old_lesson_bill = 0

        if old_cost_period == 'lesson':
            old_lesson_bill = old_cost
            old_month_bill = 0
        elif old_cost_period == 'month':
            old_lesson_bill = 0
            old_month_bill = old_cost
        if instance.cost_period == 'lesson':
            new_lesson_bill = cost
            new_month_bill = 0
        elif instance.cost_period == 'month':
            new_lesson_bill = 0
            new_month_bill = cost
        for squad in squads:
            squad.lesson_bill = squad.lesson_bill - old_lesson_bill + new_lesson_bill
            squad.bill = squad.bill - old_month_bill + new_month_bill
            squad.save()

        cost = 0
        for subject in school.school_subjects.all():
            subject_cost = 0
            if subject.cost:
                subject_cost = subject.cost
            cost += subject_cost
        school.average_cost = int(cost / len(school.school_subjects.all()))
        school.save()
    if request.POST: 
        if len(request.FILES) > 0:
            if 'subject_banner' in request.FILES:
                file = request.FILES['subject_banner']
                instance.image_banner = file
            if 'subject_icon' in request.FILES:
                file = request.FILES['subject_icon']
                instance.image_icon = file
        for squad in instance.squads.all():
            update_squad_dates(instance, squad)
        instance.save()

        return HttpResponseRedirect(instance.get_update_url())

    time_periods = school.time_periods.all()
    days = Day.objects.all()
    cells = school.school_cells.all()
    if len(cells) < len(days) * len(time_periods):
        for day in days:
            for timep in time_periods:
                new_cell = Cell.objects.get_or_create(day = day, time_period = timep, school=school)
    context = {
        "instance": instance,
        "form":form,
        'page':'subject_update',
        "profile":profile,
        'squads':Squad.objects.filter(shown=True),
        "subject_categories":school.school_subject_categories.all(),        
        "subject_categories_this":instance.category.all(),        
        "subject_ages":SubjectAge.objects.all(),
        "subject_ages_this":instance.age.all(),        
        "subject_levels":school.school_subject_levels.all(),
        "subject_levels_this":instance.level.all(),        
        "subject_filter_options":instance.filter_options.all(),        
        'time_periods':time_periods,
        'days':days,
        "all_teachers":all_teachers(school),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":school.money,
        "school_crnt":school,
        "page":"subjects",
    }
    return render(request, "subjects/subject_create.html", context)

from datetime import timedelta
def update_squad_dates(subject, squad):
    if not squad.id in subject.squad_ids:
        subject.squad_ids.append(squad.id)
        subject.start_dates.append(timezone.now().date())
    squad_index = subject.squad_ids.index(squad.id)
    lectures = squad.squad_lectures.filter(subject = subject)
    found = False
    start = int(squad.start_date.strftime('%w'))
    if start == 0:
        start = 7
    for lecture in lectures:
        if lecture.day.number >= start:
            subject.start_dates[squad_index] = squad.start_date + timedelta(lecture.day.number - start)
            found = True
            break
    if found == False and len(lectures) > 0:
        subject.start_dates[squad_index] = squad.start_date + timedelta(7 + lectures[0].day.number - start)
    
def subject_delete(request, slug=None):
    instance = Subject.objects.get(slug=slug)
    profile = get_profile(request)
    only_managers(profile)
    only_main_managers(profile)
    school = instance.school
    is_in_school(profile, school)
    if request.method == "POST":
        text = 'Удален курс '+instance.title
        instance.subject_histories.create(action_author=profile,edit=text)
        instance.delete()
        return HttpResponseRedirect("/subjects/?type=moderator&mod_school_id="+str(school.id))
    context = {
        "object": instance,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_money":profile.schools.first().money,
        "page":"subjects",
    }
    return render(request, "confirm_delete.html", context)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse

def add_paper(request):
    profile = get_profile(request)
    only_teachers(profile)
    if request.GET.get('day_id') and request.GET.get('paper_id'):
        lesson = Lesson.objects.get(id = int(request.GET.get('paper_id')))
        school = lesson.school
        is_in_school(profile, school)
        subject_materials = SubjectMaterials.objects.get(id=int(request.GET.get('day_id')))
        subject_materials.lessons.add(lesson)
    data = {
        'href':lesson.get_absolute_url()
    }
    return JsonResponse(data)
    
def remove_lesson(request):
    profile = get_profile(request)
    only_teachers(profile)
    if request.GET.get('material_id') and request.GET.get('lesson_id'):
        material = SubjectMaterials.objects.get(id=int(request.GET.get('material_id')))
        lesson = Lesson.objects.get(id=int(request.GET.get('lesson_id')))
        school = lesson.school
        is_in_school(profile, school)
        material.lessons.remove(lesson)
    data = {
    }
    return JsonResponse(data)

def get_subject_students(squads):
    students = set()
    for sq in squads:
        sq_students = sq.students.all()
        students = chain(students, sq_students)
    return students

def change_category(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    ok = False
    is_in = False
    if request.GET.get('object_id'):
        subject = Subject.objects.prefetch_related('category').get(id = id)
        school = subject.school
        is_in_school(profile, school)
        category = school.school_subject_categories.get(id=int(request.GET.get('object_id')))
        students = get_subject_students(subject.squads.prefetch_related('students'))
        if subject in category.category_subjects.all():
            category.students.remove(*students)
            category.category_subjects.remove(subject)
            text = 'В курсе '+subject.title + ' убран предмет '+category.title
            subject.subject_histories.create(action_author=profile,edit=text)
            change_lecture_options(students, subject, 'subject', category, False)
            if category in hidden_filter_ids():
                options = SchoolFilterOption.objects.filter(title=category.title)
                if len(options) > 0:
                    for option in options:
                        subject.filter_options.remove(option)
                        if len(school.school_subjects.filter(filter_options=option)) == 0:
                            option.schools.remove(school)

        else:
            is_in = True
            category.category_subjects.add(subject)

            text = 'В курсе '+subject.title + ' добавлен предмет '+category.title
            subject.subject_histories.create(action_author=profile,edit=text)

            category.students.add(*students)
            change_lecture_options(students, subject, 'subject', category, True)
            if category in hidden_filter_ids():
                options = SchoolFilterOption.objects.filter(title=category.title)
                subject.filter_options.add(*options)
                school.filter_options.add(*options)
                school_cats = category.school_categories.all()
                school.categories.add(*school_cats)

        subject.save()
        ok = True
    data = {
        "ok":ok,
        "is_in":is_in,
    }
    return JsonResponse(data)

def change_filter_option(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    ok = False
    is_in = False
    if request.GET.get('object_id'):
        subject = Subject.objects.get(id = id)
        school = subject.school
        is_in_school(profile, school)
        option = SchoolFilterOption.objects.get(id=int(request.GET.get('object_id')))
        if option in subject.filter_options.all():
            subject.filter_options.remove(option)
            text = 'В курсе '+subject.title+' изменен фильтр '+option.title
            subject.subject_histories.create(action_author=profile,edit=text)        
            if len(school.school_subjects.filter(filter_options=option)) == 0:
                option.schools.remove(school)
        else:
            subject.filter_options.add(option)
            is_in = True
            option.schools.add(school)
        ok = True


    data = {
        "ok":ok,
        "is_in":is_in,
    }
    return JsonResponse(data)


def change_age(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    ok = False
    is_in = False
    if request.GET.get('object_id'):
        subject = Subject.objects.prefetch_related('age').get(id = id)
        school = subject.school
        is_in_school(profile, school)
        age = SubjectAge.objects.get(id=int(request.GET.get('object_id')))
        students = get_subject_students(subject.squads.prefetch_related('students'))
        if subject in age.age_subjects.all():
            age.students.remove(*students)
            age.age_subjects.remove(subject)
            change_lecture_options(students, subject, 'age', age, False)
        else:
            is_in = True
            age.age_subjects.add(subject)
            age.students.add(*students)
            change_lecture_options(students, subject, 'age', age, True)
        ok = True
        subject.save()
    data = {
        "ok":ok,
        "is_in":is_in,
    }
    return JsonResponse(data)
        
def change_level(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    ok = False
    is_in = False
    if request.GET.get('object_id'):
        subject = Subject.objects.prefetch_related('level').get(id = id)
        school = subject.school
        is_in_school(profile, school)
        level = school.school_subject_levels.get(id=int(request.GET.get('object_id')))
        students = get_subject_students(subject.squads.prefetch_related('students'))
        if subject in level.level_subjects.all():
            level.students.remove(*students)
            level.level_subjects.remove(subject)
            change_lecture_options(students, subject, 'level', level, False)
        else:
            is_in = True
            level.level_subjects.add(subject)
            level.students.add(*students)
            change_lecture_options(students, subject, 'level', level, True)
        ok = True
        subject.save()
    data = {
        "ok":ok,
        "is_in":is_in,
    }
    return JsonResponse(data)

def change_lecture_options(students, subject, option, objectt, is_add):
    hashtag = ''
    school = subject.school
    cards_qs = school.crm_cards.filter(card_user__in=students)
    if option == 'office':
        remove = False
        add = False
        lectures = subject.squad_lectures.all() # subject = squad only in this case 
        if is_add != None:
            hashtag = get_hashtag(school, is_add.title)
            if len(hashtag) > 0:
                hashtag = hashtag[0]
                remove = True
            for lecture in lectures:
                lecture.office = None
                lecture.save()
        if objectt != None:
            hashtag2 = get_hashtag(school, objectt.title)
            if len(hashtag2) > 0:
                hashtag2 = hashtag2[0]
                add = True
            objectt.office_lectures.add(*lectures)
        for card in cards_qs:
            print(card.name)
            if remove:
                card_remove_hashtag(card, hashtag)
            if add: 
                card_add_hashtag(card, hashtag2)
            card.save()
    else:
        if objectt:
            hashtag = get_hashtag(school, objectt.title)
        if len(hashtag) > 0:
            hashtag = hashtag[0]
            for card in cards_qs:
                if is_add:
                    card_add_hashtag(card, hashtag)
                else:
                    card_remove_hashtag(card, hashtag)
                card.save()                
        if option == 'subject':
            lectures = subject.subject_lectures.all()
            objectt.category_lectures.add(*lectures)
        elif option == 'age':
            lectures = subject.subject_lectures.all()
            objectt.age_lectures.add(*lectures)
        elif option == 'level':
            lectures = subject.subject_lectures.all()
            objectt.level_lectures.add(*lectures)

def get_hashtag(school, title):
    obj_title = title.replace(' ', '')
    hst = school.hashtags.filter(title=obj_title)
    if len(hst) == 0:
        hashtag = school.hashtags.get_or_create(title=obj_title)
    else:
        hashtag = hst
    return hashtag

def card_add_hashtag(card, hashtag):
    card.hashtags.add(hashtag)

def card_remove_hashtag(card, hashtag):
    card.hashtags.remove(hashtag)

def make_public(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('id') and request.GET.get('checked'):
        subject = Subject.objects.get(id=int(request.GET.get('id')) )
        school = subject.school
        is_in_school(profile, school)
        if request.GET.get('checked') == 'false':
            subject.public = False
        else:
            subject.public = True
        subject.save()

    data = {
    }
    return JsonResponse(data)
def make_public_cost(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('id') and request.GET.get('checked'):
        subject = Subject.objects.get(id=int(request.GET.get('id')) )
        school = subject.school
        is_in_school(profile, school)
        if request.GET.get('checked') == 'false':
            subject.public_cost = False
        else:
            subject.public_cost = True
        subject.save()

    data = {
    }
    return JsonResponse(data)

from django.contrib.postgres.search import TrigramSimilarity
def searching_subjects(request):
    profile = get_profile(request)
    school = profile.schools.first()
    only_managers(profile)

    text = request.GET.get('text')
    kef = 1
    res = []
    if len(text) > 4:
        kef = 4
    if text != '':
        similarity=TrigramSimilarity('title', text)        
        subjects = school.school_subjects.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        i = 0
        for subject in subjects:
            image_url = ''
            if subject.image_icon:
                image_url = subject.image_icon.url
            res.append([subject.title, subject.get_absolute_url(), image_url])
            i+=1
            if i == 4:
                break

    data = {
        "res":res,
    }
    return JsonResponse(data)
