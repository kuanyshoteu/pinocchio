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
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_crnt":school,        
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
    school = is_moderator_school(request, profile)
    context = {
        "profile": profile,
        "squads":school.groups.all(),
        "hisschools":profile.schools.all(),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_crnt":school,        
        "school_money":school.money,
    }
    return render(request, "squads/squad_list.html", context)

def squad_create(request):
    profile = get_profile(request)
    only_managers(profile)
    form = SquadForm(request.POST or None, request.FILES or None)
    school = is_moderator_school(request, profile)
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
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_crnt":school,        
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

    time_periods = school.time_periods.all()
    days = Day.objects.all()
    cells = school.school_cells.all()
    if len(cells) < len(days) * len(time_periods):
        for day in days:
            for timep in time_periods:
                new_cell = Cell.objects.get_or_create(day = day, time_period = timep, school=school)

    free_students = []
    i = 0
    qs = school.people.filter(is_student=True).exclude(squads=instance)
    number_in_page = 27
    for student in qs:
        free_students.append(student)
        i += 1
        if i == number_in_page:
            break
    if len(qs) % number_in_page == 0:
        number_of_pages = int(len(qs)/number_in_page)
    else:
        number_of_pages = int(len(qs)/number_in_page) + 1
    context = {
        "instance": instance,
        "form":form,
        "profile":profile,
        "all_teachers":all_teachers(school),
        "squad_students":instance.students.all(),
        "all_students":free_students,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_crnt":school,        
        "school_money":school.money,
        "offices":school.school_offices.all(),        
        'time_periods':time_periods,
        'days':days,
        'number_of_pages':number_of_pages,
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
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_crnt":school,        
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
            add_student_to_squad(student, squad)
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

def prepare_mail(first_name, phone, mail, squad, password, send_mail):
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
    ok_mail = False
    if len(squad.squad_lectures.all()) > 0:
        send_date = (timezone.now().date() + timedelta(needed_day - today)).strftime('%d%m%y')+time
        if lecture.office:
            address = lecture.office.address
        else:
            address = squad.school.school_offices.first().address
        if send_mail:
            ok_mail = True
            try:
                if password:
                    send_hello_email(first_name, phone, mail, password, 'В '+lecture_time+' у Вас состоится пробный урок по адресу '+address)
                else:
                    timeaddress = 'В '+lecture_time+' у Вас состоится пробный урок по адресу '+address
                    text = "Здравствуйте "+first_name+ "! Вас зарегестрировали в группу<br><br>"+timeaddress+". Расписание можете посмотреть в личной странице"
                    send_email('Bilimtap регистрация в группу', text, [mail])
            except Exception as e:
                ok_mail = False
        if is_send:
            #send_sms(student.phone, 'Ждем Вас на пробном уроке в '+lecture_time+' '+address, send_date)
            pass
    return ok_mail

def add_student_to_squad(student, squad):
    squad.students.add(student)
    for subject in squad.subjects.all():
        ages = subject.age.all()
        student.crm_age_connect.add(*ages)
        categories = subject.category.all()
        student.crm_subject_connect.add(*categories)
        subject.students.add(student)
        student.salary += subject.cost
    student.save()
    school = squad.school
    for timep in school.time_periods.all():
        timep.people.add(student)
    for lecture in squad.squad_lectures.all():
        add_person_to_lecture(lecture, student)
        lecture.save()

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

# **************************************************************************************


def squad_schedule(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    squad = Squad.objects.get(id = id)
    school = squad.school
    is_in_school(profile, school)
    res = []
    for timep in school.time_periods.all():
        line = []
        for cell in timep.time_cell.all():
            lectures = []
            for lecture in cell.lectures.filter(squad = squad):
                if lecture.subject in squad.subjects.all():
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
                    lectures.append([lecture.id, lecture.subject.title, lecture.subject.id, cabinet, cabinet_id, office_cabs])
            line.append([cell.id, lectures])
        res.append([timep.start + '-' + timep.end, line])

    data = {
        'calendar':res
    }
    return JsonResponse(data)

def subject_list(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    squad = Squad.objects.get(id = id)
    school = squad.school
    is_in_school(profile, school)
    res = []
    res2 = []
    for subject in school.school_subjects.all():
        if not subject in squad.subjects.all():
            res.append([subject.id, [subject.title]])
        else:
            res2.append([subject.id, [subject.title]])
    data = {
        'courses_in_group':res2,
        'courses_not_in_group':res,
    }
    return JsonResponse(data)

def change_schedule(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    squad = Squad.objects.get(id = id)
    school = squad.school
    is_in_school(profile, school)
    school.new_schedule = True
    school.save()

    if request.GET.get('subject_id') and request.GET.get('cell_id') and request.GET.get('old_cell'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')) )
        subject_students = subject.students.all()
        cell = Cell.objects.get(id = int(request.GET.get('cell_id')))
        if request.GET.get('old_cell') == 'none':
            if len(Lecture.objects.filter(squad=squad,subject=subject,cell=cell)) == 0:
                lecture = Lecture.objects.create(
                    squad=squad,
                    subject=subject,
                    cell=cell, 
                    school=school,
                    day=cell.day,
                    office=squad.office,
                    category=subject.category,
                    age=subject.age.first())
                lecture.people.add(*subject_students)
                if squad.teacher:
                    lecture.people.add(squad.teacher)
        else:
            old_cell = Cell.objects.get(id = int(request.GET.get('old_cell')))
            lecture = Lecture.objects.get(squad=squad,subject=subject,cell=old_cell)
            if len(Lecture.objects.filter(squad=squad,subject=subject,cell=cell)) == 0:
                lecture.cell = cell
                lecture.day = cell.day
                lecture.save()
            else:
                lecture.delete()
        squad.save()

    data = {
    }
    return JsonResponse(data)

def add_subject(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('subject_id') and request.GET.get('squad_id'):
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')) )
        school = squad.school
        is_in_school(profile, school)
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')) )
        squad.subjects.add(subject)
        squad_students = squad.students.all()
        subject.students.add(*squad_students)
        if squad.teacher:
            subject.teachers.add(squad.teacher)
    data = {
    }
    return JsonResponse(data)

def delete_subject(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('subject_id') and request.GET.get('squad_id'):
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')) )
        school = squad.school
        is_in_school(profile, school)
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')) )
        squad.subjects.remove(subject)
        squad_students = subject.students.all()
        subject.students.remove(*squad_students)
        subject.teachers.remove(squad.teacher)
    data = {
    }
    return JsonResponse(data)
        
def delete_lesson(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('lecture_id'):
        squad = Squad.objects.get(id = id)
        school = squad.school
        is_in_school(profile, school)
        lecture = squad.squad_lectures.get(id=int(request.GET.get('lecture_id')))
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

def get_page_students(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    squad = Squad.objects.get(id = id)
    school = squad.school
    is_in_school(profile, school)
    if request.GET.get('need_page'):
        need_page = int(request.GET.get('need_page'))
        free_students = []
        i = 0
        qs = school.people.filter(is_student=True).exclude(squads=squad)
        lenqs = len(qs)
        number_in_page = 27
        for x in range((need_page-1)*number_in_page,(need_page)*number_in_page):
            if x >= lenqs:
                break
            student = qs[x]
            if student.image:
                image = student.image.url
            else:
                image = '/static/images/nophoto.png'
            free_students.append([student.id, student.first_name, image])
    data = {
        "all_students":free_students
    }
    return JsonResponse(data)

from django.contrib.postgres.search import TrigramSimilarity
def hint_students_group(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    squad = Squad.objects.get(id = id)
    school = squad.school
    is_in_school(profile, school)
    res = []
    if request.GET.get('text'):
        text = request.GET.get('text')
        if len(text) > 0:
            i = 0
            kef = 1
            if len(text) > 4:
                kef = 4            
            similarity=TrigramSimilarity('first_name', text)
            students = school.people.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
            for student in students:
                if i >= 4:
                    break
                if student.image:
                    image = student.image.url
                else:
                    image = '/static/images/nophoto.png'
                if student in squad.students.all():
                    is_in = True
                else:
                    is_in = False
                res.append([student.id, student.first_name, image, is_in])
                i += 1
    data = {
        "res":res
    }
    return JsonResponse(data)
