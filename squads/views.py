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

from .forms import SquadForm, SquadForm2
from .table_change_form import TableChangeForm
from .models import *
from schools.models import School
from subjects.models import *
from subjects.views import update_squad_dates,change_lecture_options
from papers.models import *
from library.models import Folder
from accounts.models import Profile
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

def squad_detail(request, slug=None):
    instance = get_object_or_404(Squad, slug=slug)
    profile = get_profile(request)
    school = instance.school
    is_in_school(profile, school)
    time_periods = school.time_periods.all()
    days = Day.objects.all()
    context = {
        "instance": instance,
        "squad_url":instance.get_absolute_url(),
        "profile":profile,
        'time_periods':time_periods,
        'days':days,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "school_money":school.money,
    }
    return render(request, "squads/squad_detail.html", context)

def squad_list(request):
    profile = get_profile(request)
    only_staff(profile)
    if is_profi(profile, 'Teacher'):
        hissquads = profile.hissquads.all()
    else:
        hissquads = profile.squads.all()
    school = profile.schools.first()
    context = {
        "profile": profile,
        "squads":school.groups.all(),
        "hisschools":profile.schools.all(),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "school_money":school.money,
    }
    return render(request, "squads/squad_list.html", context)

def squad_create(request):
    profile = get_profile(request)
    only_managers(profile)
    form = SquadForm(request.POST or None, request.FILES or None)
    school = profile.schools.first()
    if form.is_valid():
        instance = form.save(commit=False)
        instance.start_date = timezone.now().date()
        instance.end_date = timezone.now().date()
        instance.school = school
        instance.save()
        return HttpResponseRedirect(instance.get_update_url())
    
    context = {
        "form": form,
        "profile":profile,
        "all_teachers":all_teachers(school),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "school_money":school.money,
    }
    return render(request, "squads/squad_create.html", context)

def squad_update(request, slug=None):
    profile = get_profile(request)
    only_managers(profile)
    instance = get_object_or_404(Squad, slug=slug)
    school = instance.school
    is_in_school(profile, school)
    form = SquadForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if not instance.height_field:
            instance.height_field = 0
        if not instance.width_field:
            instance.width_field = 0
        instance.start_date = datetime.datetime.strptime(request.POST.get('start'), "%Y-%m-%d").date()
        instance.end_date = datetime.datetime.strptime(request.POST.get('end'), "%Y-%m-%d").date()
        instance.save()
    if request.POST: 
        if len(request.FILES) > 0:
            if 'squad_banner' in request.FILES:
                file = request.FILES['squad_banner']
                instance.image_banner = file
            if 'squad_icon' in request.FILES:
                file = request.FILES['squad_icon']
                instance.image_icon = file
        instance.color_back = request.POST.get('color_back')
        instance.save()
        for subject in instance.subjects.all():
            update_squad_dates(subject, instance)
            subject.save()
        return HttpResponseRedirect(instance.get_update_url())

    context = {
        "instance": instance,
        "form":form,
        "profile":profile,
        "all_teachers":all_teachers(school),
        "squad_students":instance.students.all(),
        "all_students":school.people.filter(is_student=True).exclude(squads=instance),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "school_money":school.money,
        "offices":school.school_offices.all(),        
    }
    return render(request, "squads/squad_create.html", context)


def squad_delete(request, slug=None):
    profile = get_profile(request)
    only_managers(profile)
    instance = Squad.objects.get(slug=slug)
    school = instance.school
    is_in_school(profile, school)
        
    if request.method == "POST":
        instance.delete()
        messages.success(request, "Successfully deleted")
        return redirect("squads:list")
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
import datetime

def add_paper(request):
    if request.GET.get('group_id'):
        squad = Squad.objects.get(id = int(request.GET.get('group_id')) )
        school = squad.school
        is_in_school(profile, school)
        if request.GET.get('day_id'):
            if request.GET.get('paper_id'):
                try:
                    squad.lesson_ids.update({request.GET.get('day_id'): squad.lesson_ids[request.GET.get('day_id')] + '-' + request.GET.get('paper_id')})
                except Exception as e:
                    squad.lesson_ids.update({request.GET.get('day_id'): request.GET.get('paper_id')})
                squad.save() 
                
                lesson = Lesson.objects.get(id = int(request.GET.get('paper_id')))
                if not squad in lesson.squad_list.all(): 
                    lesson.squad_list.add(squad)
    data = {
        'href':lesson.get_absolute_url()
    }
    return JsonResponse(data)

def calendar_change(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('id'):
        squad = Squad.objects.get(id = int(request.GET.get('id')) )
        school = squad.school
        is_in_school(profile, school)
        if request.GET.get('day_of_week'):
            day_of_week = request.GET.get('day_of_week')
            if day_of_week in squad.days:
                index = squad.days.index(day_of_week)
                del squad.days[index]
            else:
                squad.days.append(day_of_week)
            squad.save()
    data = {
    }
    return JsonResponse(data)

def set_time(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('instance_id'):
        squad = Squad.objects.get(id = int(request.GET.get('instance_id')) )
        school = squad.school
        is_in_school(profile, school)
        if request.GET.get('day') and request.GET.get('time') and request.GET.get('checked'):
            index = squad.days.index("day_of_week" + request.GET.get('day'))
            x = []
            for i in range(len(squad.times_of_days), len(squad.days)):
                squad.times_of_days.append('')
            if request.GET.get('checked') == 'false':
                squad.times_of_days[index] += request.GET.get('time') + ' '
            else:
                squad.times_of_days[index] = squad.times_of_days[index].replace(request.GET.get('time'), '')
            squad.save()
    data = {
    }
    return JsonResponse(data)

def change_curator(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('teacher_id') and request.GET.get('squad_id'):
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')) )
        school = squad.school
        is_in_school(profile, school)
        oldteacher = squad.teacher
        teacher = Profile.objects.get(id = int(request.GET.get('teacher_id')) )
        squad.teacher = teacher
        squad.save()
        for subject in squad.subjects.all():
            subject.teachers.add(teacher)
            if oldteacher:
                subject.teachers.remove(oldteacher)
        for lecture in squad.squad_lectures.all():
            if oldteacher:
                remove_person_from_lecture(lecture, oldteacher)
            add_person_to_lecture(lecture, teacher)
            lecture.save()

    print(lecture.people.all())

    data = {
    }
    return JsonResponse(data)

def add_student(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('student_id') and request.GET.get('squad_id'):
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')) )
        school = squad.school
        is_in_school(profile, school)        
        student = Profile.objects.get(id = int(request.GET.get('student_id')) )
        add = True
        if student in squad.students.all():
            add = False
            remove_student_from_squad(student, squad)
        else:
            add_student_to_squad(student, squad,None,False)
    data = {
        'add':add,
    }
    return JsonResponse(data)

def remove_student_from_squad(student, squad):
    squad.students.remove(student)
    for subject in squad.subjects.all():
        subject.students.remove(student)
        student.salary -= subject.cost
    student.save()
    for lecture in squad.squad_lectures.all():
        remove_person_from_lecture(lecture, student)
        lecture.save()
    squad.squad_attendances.filter(student=student).delete()
def add_student_to_squad(student, squad, password, send_mail):
    squad.students.add(student)
    for subject in squad.subjects.all():
        subject.students.add(student)
        student.salary += subject.cost
    student.save()
    school = squad.school
    for timep in school.time_periods.all():
        timep.people.add(student)
    today = int(timezone.now().strftime('%w'))
    nowhour = int(timezone.now().strftime('%H')) 
    nowminute = int(timezone.now().strftime('%M')) 
    nowtime = int(nowhour*60 + nowminute)
    needed_day = 14
    lecture_time = ''
    is_send = True
    for lecture in squad.squad_lectures.all():
        lecture_day_number = lecture.day.number
        if lecture_day_number - today < 0:
            lecture_day_number += 7 
        if lecture_day_number - today < needed_day-today:
            lecture_start_h = int(lecture.cell.time_period.start.split(':')[0])
            lecture_start_m = int(lecture.cell.time_period.start.split(':')[1])
            lecture_start_t = lecture_start_h*60 + lecture_start_m
            if nowtime < lecture_start_t -120:
                is_send = True
            needed_day = lecture_day_number
            lecture_time = lecture.cell.time_period.start
            if '08:' in lecture.cell.time_period.start or '09:' in lecture.cell.time_period.start:
                needed_day -= 1
                time = '20:00'
            elif '10:' in lecture.cell.time_period.start:
                time = '09:00'
            else:
                timestr = str(int(lecture.cell.time_period.start.split(':')[0])-2)
                if int(lecture.cell.time_period.start.split(':')[0])-2 < 10:
                    timestr = '0' + str(int(lecture.cell.time_period.start.split(':')[0])-2)
                time = timestr+str(lecture.cell.time_period.start.split(':')[1])
        add_person_to_lecture(lecture, student)
        lecture.save()
    if len(squad.squad_lectures.all())>0:
        send_date = (timezone.now().date() + timedelta(needed_day - today)).strftime('%d%m%y')+time
        if lecture.office:
            address = lecture.office.address
        else:
            address = squad.school.school_offices.first().address
        print(send_date, lecture_time, address, is_send)
        if send_mail:
            send_hello_email(student,password, 'В '+lecture_time+' у Вас состоится пробный урок по адресу '+address)
        if is_send:
            #send_sms(student.phone, 'Ждем Вас на пробном уроке в '+lecture_time+' '+address, send_date)
            pass
def remove_person_from_lecture(lecture, person):
    if not person.id in lecture.person_id:
        lecture.person_id.append(person.id)
        lecture.person_number.append(1)
    index = lecture.person_id.index(person.id)
    number = lecture.person_number[index]
    if number == 1:
        lecture.people.remove(person)
    lecture.person_number[index] -= 1
    if lecture.person_number[index] < 0:
        lecture.person_number[index] = 0

def add_person_to_lecture(lecture, person):
    if not person.id in lecture.person_id:
        lecture.person_id.append(person.id)
        lecture.person_number.append(0)
    lecture.cell.time_period.people.add(person)
    index = lecture.person_id.index(person.id)
    number = lecture.person_number[index]
    lecture.people.add(person)
    lecture.person_number[index] += 1

def change_office(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('object_id'):
        squad = Squad.objects.select_related('office').get(id = id)
        school = squad.school
        is_in_school(profile, school)
        old_office = None
        if squad.office:
            old_office = squad.office
        if int(request.GET.get('object_id')) == -1:
            squad.office = None
            change_lecture_options(squad, 'office', None, old_office)
        else:
            office = Office.objects.get(id = int(request.GET.get('object_id')))
            squad.office = office
            change_lecture_options(squad, 'office', office, old_office)
        squad.save()
    data = {
    }
    return JsonResponse(data)
