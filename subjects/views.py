from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import RedirectView

from .forms import SubjectForm,SubjectForm2
from .models import *
from papers.models import *
from library.models import Folder
from accounts.models import Profile
from schools.models import Cabinet
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
        profile.squads
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
        "school_money":school.money,
    }
    return render(request, "subjects/subject_detail.html", context)

def subject_list(request):
    profile = get_profile(request)
    only_staff(profile)
    school = profile.schools.first()
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
        "school_money":school.money,
    }
    return render(request, "subjects/subject_list.html", context)

def subject_create(request):
    profile = get_profile(request)
    only_managers(profile)
    form = SubjectForm(request.POST or None, request.FILES or None)
    school = profile.schools.first()    
    if form.is_valid():
        instance = form.save(commit=False)
        instance.school = school
        instance.save()
        return HttpResponseRedirect(instance.get_update_url())

    context = {
        "form": form,
        "profile":profile,
        "all_teachers":all_teachers(school),
        "subject_categories":school.school_subject_categories.all(),        
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "school_money":school.money,
    }
    return render(request, "subjects/subject_create.html", context)

def subject_update(request, slug=None):
    instance = get_object_or_404(Subject, slug=slug)
    profile = get_profile(request)
    only_staff(profile)
    school = instance.school
    is_in_school(profile, school)
    form = SubjectForm(request.POST or None, request.FILES or None, instance=instance)
    if is_profi(profile, 'Manager'):
        if form.is_valid():
            instance = form.save(commit=False)
            if not instance.height_field:
                instance.height_field = 0
            if not instance.width_field:
                instance.width_field = 0
            instance.save()
        cost = 0
        for subject in school.school_subjects.all():
            if not subject.cost:
                subject.cost = 0
                subject.save()
            cost += subject.cost
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
        get_number_of_materials = int(request.POST.get('number_of_materials'))
        if instance.number_of_materials < get_number_of_materials:
            if get_number_of_materials < 100:
                for i in range(0, get_number_of_materials - instance.number_of_materials):
                    instance.materials.create(
                        school=instance.school
                    )
        instance.number_of_materials = int(request.POST.get('number_of_materials'))
        instance.color_back = request.POST.get('color_back')
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
        'squads':Squad.objects.all(),
        "subject_categories":school.school_subject_categories.all(),        
        "subject_ages":school.school_subject_ages.all(),        
        'time_periods':time_periods,
        'days':days,
        "all_teachers":all_teachers(school),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "school_money":school.money,
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
    school = instance.school
    is_in_school(profile, school)
    if request.method == "POST":
        instance.delete()
        messages.success(request, "Successfully deleted")
        return redirect("subjects:list")
    context = {
        "object": instance,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "school_money":profile.schools.first().money,
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
        print('ok')
    data = {
    }
    return JsonResponse(data)

def subject_schedule(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    subject = Subject.objects.get(id = id)
    school = subject.school
    is_in_school(profile, school)
    res = []
    for timep in school.time_periods.all():
        line = []
        for cell in timep.time_cell.all():
            lectures = []
            for lecture in cell.lectures.filter(subject = subject):
                if lecture.squad in subject.squads.all():
                    cabinet='каб.'
                    cabinet_id = '-1'
                    if lecture.cabinet:
                        cabinet = lecture.cabinet.title
                        cabinet_id = lecture.cabinet.id
                    office_cabs = [[cabinet_id, cabinet]]
                    if lecture.office:
                        for cab in lecture.office.cabinets.all():
                            if cab.id != cabinet_id:
                                office_cabs.append([cab.id, cab.title])
                    lectures.append([lecture.id, lecture.squad.title, lecture.squad.id, cabinet, cabinet_id, office_cabs])
            line.append([cell.id, lectures])
        res.append([timep.start + '-' + timep.end, line])

    data = {
        'calendar':res
    }
    return JsonResponse(data)

def squad_list(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    subject = Subject.objects.get(id = id)
    school = subject.school
    is_in_school(profile, school)
    res = []
    res2 = []
    for squad in school.groups.all():
        if not squad in subject.squads.all():
            res.append([squad.id, [squad.title]])
        else:
            res2.append([squad.id, [squad.title]])
    data = {
        'groups_in_subject':res2,
        'groups_not_in_subject':res,
    }
    return JsonResponse(data)

def change_schedule(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    subject = Subject.objects.get(id = id)
    school = subject.school
    is_in_school(profile, school)
    school.new_schedule = True
    school.save()

    if request.GET.get('squad_id') and request.GET.get('cell_id') and request.GET.get('old_cell'):
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')) )
        squad_students = squad.students.all()
        cell = Cell.objects.get(id = int(request.GET.get('cell_id')))
        if request.GET.get('old_cell') == 'none':
            if len(Lecture.objects.filter(subject=subject,squad=squad,cell=cell)) == 0:
                lecture = Lecture.objects.create(
                    subject=subject,
                    squad=squad,
                    cell=cell, 
                    school=school,
                    day=cell.day,
                    office=squad.office,
                    category=subject.category,
                    age=subject.age)
                lecture.people.add(*squad_students)
                if squad.teacher:
                    lecture.people.add(squad.teacher)
        else:
            old_cell = Cell.objects.get(id = int(request.GET.get('old_cell')))
            lecture = Lecture.objects.get(subject=subject,squad=squad,cell=old_cell)
            if len(Lecture.objects.filter(subject=subject,squad=squad,cell=cell)) == 0:
                lecture.cell = cell
                lecture.day = cell.day
                lecture.save()
            else:
                lecture.delete()
        subject.save()

    data = {
    }
    return JsonResponse(data)

def add_squad(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('squad_id') and request.GET.get('subject_id'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')) )
        school = subject.school
        is_in_school(profile, school)
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')) )
        subject.squads.add(squad)
        squad_students = squad.students.all()
        subject.students.add(*squad_students)
        if squad.teacher:
            subject.teachers.add(squad.teacher)
    data = {
    }
    return JsonResponse(data)

def delete_squad(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('squad_id') and request.GET.get('subject_id'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')) )
        school = subject.school
        is_in_school(profile, school)
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')) )
        subject.squads.remove(squad)
        squad_students = squad.students.all()
        subject.students.remove(*squad_students)
        subject.teachers.remove(squad.teacher)
    data = {
    }
    return JsonResponse(data)

def change_category(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('object_id'):
        subject = Subject.objects.select_related('category').get(id = id)
        school = subject.school
        is_in_school(profile, school)
        students = subject.students.all()
        if subject.category:
            subject.category.students.remove(*students)
        if int(request.GET.get('object_id')) == -1:
            subject.category = None
            change_lecture_options(subject, 'subject', None)
        else:
            category = SubjectCategory.objects.get(id = int(request.GET.get('object_id')))
            subject.category = category
            change_lecture_options(subject, 'subject', category)
            category.students.add(*students)
        subject.save()
    data = {
    }
    return JsonResponse(data)
        
def change_age(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('object_id'):
        subject = Subject.objects.select_related('age').get(id = id)
        school = subject.school
        is_in_school(profile, school)
        students = subject.students.all()
        if subject.age:
            subject.age.students.remove(*students)
        if int(request.GET.get('object_id')) == -1:
            subject.age = None
            change_lecture_options(subject, 'age', None)
        else:
            age = SubjectAge.objects.get(id = int(request.GET.get('object_id')))
            subject.age = age
            change_lecture_options(subject, 'age', age)
            age.students.add(*students)
        subject.save()
    data = {
    }
    return JsonResponse(data)

def change_lecture_options(subject, option, objectt):
    if option == 'subject':
        for lecture in subject.subject_lectures.all():
            lecture.category = objectt
            lecture.save()
    elif option == 'age':
        for lecture in subject.subject_lectures.all():
            lecture.age = objectt
            lecture.save()
    if option == 'office':
        for lecture in subject.squad_lectures.all():
            lecture.office = objectt
            lecture.save()
        
def delete_lesson(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('lecture_id'):
        subject = Subject.objects.get(id = id)
        school = subject.school
        is_in_school(profile, school)
        lecture = subject.subject_lectures.get(id=int(request.GET.get('lecture_id')))
        lecture.delete()
    data = {
    }
    return JsonResponse(data)
        
def change_lecture_cabinet(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('cabinet_id') and request.GET.get('lecture_id'):
        lecture = Lecture.objects.get(id=int(request.GET.get('lecture_id')))
        school = lecture.school
        is_in_school(profile, school)        
        cabinet = Cabinet.objects.get(id=int(request.GET.get('cabinet_id')))
        lecture.cabinet = cabinet
        lecture.save()
    data = {
    }
    return JsonResponse(data)
