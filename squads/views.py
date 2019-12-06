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
from subjects.views import update_squad_dates,change_lecture_options,get_subject_students
from papers.models import *
from library.models import Folder
from accounts.models import Profile, CRMCardHistory
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
        'height':28*15*int(60/school.schedule_interval)+25,
        'constant_times':get_times(school.schedule_interval),
        'interval':school.schedule_interval,   
        'page':'squads',
    }
    return render(request, "squads/squad_detail.html", context)

def squad_list(request):
    profile = get_profile(request)
    only_staff(profile)
    if is_profi(profile, 'Teacher'):
        hissquads = profile.hissquads.filter(shown=True)
    else:
        hissquads = profile.squads.filter(shown=True)
    school = is_moderator_school(request, profile)
    context = {
        "profile": profile,
        "squads":school.groups.filter(shown=True),
        "hisschools":profile.schools.all(),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_crnt":school,        
        "school_money":school.money,
        "filter_office":profile.skill.crm_office2,
        'page':'squads',    
    }
    return render(request, "squads/squad_list.html", context)

def squad_trash(request):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    two_weeks_ago = timezone.now() - timedelta(14)
    delete_list = school.groups.filter(shown=False, deleted_time__lt=two_weeks_ago)
    if len(delete_list) > 0:
        delete_list.delete()
    context = {
        "profile": profile,
        "squads":school.groups.filter(shown=False),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_crnt":school,        
        "school_money":school.money,
        "trash":True,
        'page':'squads',
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
        instance.school = school
        if len(school.school_offices.all()) > 0:
            instance.office = school.school_offices.first()
        instance.save()
        instance.squad_histories.create(action_author=profile,edit='Создал группу '+instance.title)
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
        'page':'squads',
    }
    return render(request, "squads/squad_create.html", context)

def squad_update(request, slug=None):
    profile = get_profile(request)
    only_managers(profile)
    instance = get_object_or_404(Squad, slug=slug)
    school = instance.school
    is_in_school(profile, school)
    form = SquadForm(request.POST or None, request.FILES or None, instance=instance)
    change_time = False
    change_img = False
    change_title = False
    change_content = False
    if form.is_valid():
        old_start_date = instance.start_date
        old_title = instance.title
        old_content = instance.content
        instance = form.save(commit=False)
        start = request.POST.get('start')
        end = request.POST.get('end')
        if start == '':
            start = timezone.now().strftime("%Y-%m-%d")
        if end == '':
            end = timezone.now().strftime("%Y-%m-%d")
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        if old_title != instance.title:
            change_title = True
        if old_content != instance.content:
            change_content = True
        if instance.start_date != start_date:
            change_time = True
            instance.start_date = start_date
        instance.save()
    if request.POST:
        if len(request.FILES) > 0:
            change_img = True
            if 'squad_banner' in request.FILES:
                file = request.FILES['squad_banner']
                instance.image_banner = file
            if 'squad_icon' in request.FILES:
                file = request.FILES['squad_icon']
                instance.image_icon = file
        if request.POST.get('color_back'):
            instance.color_back = request.POST.get('color_back')
        instance.save()
        text = 'Внес изменения в группу '+instance.title
        if change_title:
            text += '<br> Название '+old_title+' -> ' + instance.title 
        if change_content:
            text += '<br> Описание '+old_content+' -> ' + instance.content
        if change_time:
            text += '<br> Дата начала '+str(old_start_date)+' -> '+str(start_date)
        if change_img:
            text += '<br> Картинка'
        instance.squad_histories.create(action_author=profile,edit=text)        
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
        'constant_times':get_times(school.schedule_interval),
        'interval':school.schedule_interval,
        'days':get_days(),
        'other_subjects':school.school_subjects.all(),
        'height':28*15*int(60/school.schedule_interval)+25,
        'page':'squads',
    }
    return render(request, "squads/squad_create.html", context)

def squad_delete(request, slug=None):
    profile = get_profile(request)
    only_managers(profile)
    only_main_managers(profile)    
    instance = Squad.objects.get(slug=slug)
    school = instance.school
    is_in_school(profile, school)
        
    if request.method == "POST":
        text = 'Удалил группу '+instance.title
        instance.squad_histories.create(action_author=profile,edit=text)
        instance.shown = False
        instance.deleted_time = timezone.now()
        instance.save()
        return redirect("squads:list")
    context = {
        "object": instance,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
        "is_moderator":is_profi(profile, 'Moderator'),
        "school_crnt":school,        
        "school_money":profile.schools.first().money,
        'page':'squads',
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
        if oldteacher:
            text = 'Изменен учитель группы '+squad.title+' '+oldteacher.first_name+' -> '+teacher.first_name
        else:
            text = 'Установлен учитель '+teacher.first_name+' в группу '+squad.title
        squad.squad_histories.create(action_author=profile,edit=text)

    data = {
    }
    return JsonResponse(data)

def add_student(request):
    profile = get_profile(request)
    only_managers(profile)
    add = False
    problems = 'ok'
    if request.GET.get('student_id') and request.GET.get('squad_id'):
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')) )
        school = squad.school
        is_in_school(profile, school)        
        student = Profile.objects.get(id = int(request.GET.get('student_id')) )
        add = True
        if student in squad.students.all():
            add = False
            # text = 'Убран ученик '+student.first_name+' в группу '+squad.title
            # squad.squad_histories.create(action_author=profile,edit=text)
            remove_student_from_squad(student, squad, profile)
        else:
            # text = 'Добавлен ученик '+student.first_name+' в группу '+squad.title
            # squad.squad_histories.create(action_author=profile,edit=text)
            problems = add_student_to_squad(student, squad, profile)
    data = {
        'add':add,
        'problems':problems
    }
    return JsonResponse(data)

def remove_student_from_squad(student, squad, manager_profile):
    squad.students.remove(student)
    school = squad.school
    other_squads = student.squads.all().exclude(id=squad.id)
    other_subjects = Subject.objects.filter(squads__in=other_squads)
    card = student.card.get_or_create(school=school)[0]
    for subject in squad.subjects.all():
        cats = subject.category.all()
        cats = cats.exclude(category_subjects__in=other_subjects)

        # Subject filter and subject hashtag in crm removing
        student.crm_subject_connect.remove(*cats)
        for cat in cats:
            hs = school.hashtags.filter(title = cat.title.replace(' ', '_'))
            if len(hs) > 0:
                card.hashtags.remove(hs[0])
    student.save()
#    squad.squad_attendances.filter(student=student).delete()
    hist = CRMCardHistory.objects.create(
        action_author = manager_profile,
        card = card,
        edit = '*** Убрали из ' + squad.title + ' ***',
        )

def add_student_to_squad(student, squad, manager_profile):
    subjects = squad.subjects.all()
    other_sqs = Squad.objects.filter(subjects__in=subjects).exclude(id=squad.id)
    other_sts = Profile.objects.filter(squads__in=other_sqs)
    school = squad.school
    card = student.card.get_or_create(school=school)[0]
    squad.students.add(student)
    for subject in squad.subjects.all():
        categories = subject.category.all()
        student.crm_subject_connect.add(*categories)
        for cat in categories:
            hs = school.hashtags.get_or_create(title = cat.title.replace(' ', '_'))
            card.hashtags.add(hs[0])
    nm = squad.need_money.get_or_create(card=card)[0]
    nm.start_date = timezone.now().date()
    nm.finance_closed.create(
        start=timezone.now().date(),
        money=0,
        )
    school = squad.school
    hist = CRMCardHistory.objects.create(
        action_author = manager_profile,
        card = card,
        edit = '*** Регистрация в ' + squad.title + ' ***',
        )    
    if student in other_sts:
        return student.first_name
    return 'ok'

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
            if len(squad.school.school_offices.all())> 0:
                address = squad.school.school_offices.first().address
            else:
                address = ''
        if send_mail and '@' in mail:
            ok_mail = True
            try:
                if password:
                    send_str = 'В '+lecture_time+' у Вас состоится пробный урок'
                    if address != '':
                        send_str += ' по адресу '+address
                    send_hello_email(first_name, phone, mail, password, send_str)
                else:
                    timeaddress = 'В '+lecture_time+' у Вас состоится пробный урок'
                    if address != '':
                        timeaddress += ' по адресу '+address
                    text = "Здравствуйте "+first_name+ "! Вас зарегестрировали в группу<br><br>"+timeaddress+". Расписание можете посмотреть в личной странице"
                    send_email('Bilimtap регистрация в группу', text, [mail])
            except Exception as e:
                ok_mail = False
        if is_send:
            school = squad.school
            if school.version != 'free' and school.sms_amount > 0:
                send_sms(phone, 'Ждем Вас на пробном уроке в '+lecture_time+' '+address, send_date)
                school.sms_amount -= 1
                school.save()
            pass
    return ok_mail

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
            change_lecture_options(squad.students.all(), squad, 'office', None, old_office)
        else:
            office = Office.objects.get(id = int(request.GET.get('object_id')))
            squad.office = office
            change_lecture_options(squad.students.all(), squad, 'office', office, old_office)
        
        old_office_title = ', убран '
        new_office_title = ', добавлен '
        if old_office:
            old_office_title += old_office.title
        if squad.office:
            new_office_title += squad.office.title
        text = 'В группе '+squad.title+' изменен офис'+old_office_title+new_office_title
        squad.squad_histories.create(action_author=profile,edit=text)
        squad.save()
    data = {
    }
    return JsonResponse(data)

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
        subject_students = get_subject_students(subject.squads.prefetch_related('students'))
        cell = Cell.objects.get(id = int(request.GET.get('cell_id')))
        if request.GET.get('old_cell') == 'none':
            if len(Lecture.objects.filter(squad=squad,subject=subject,cell=cell)) == 0:
                ages = subject.age.all()
                categories = subject.category.all()
                lecture = Lecture.objects.create(
                    squad=squad,
                    subject=subject,
                    cell=cell, 
                    school=school,
                    day=cell.day,
                    office=squad.office,
                )
                lecture.age.add(*ages)
                lecture.category.add(*categories)
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
        
        add_subject_work(school, squad, subject)
    data = {
    }
    return JsonResponse(data)

def add_subject_work(school, squad, subject):
    squad.subjects.add(subject)
    cost = subject.cost
    cards = school.crm_cards.all()
    if subject.cost_period == 'month':
        squad.bill -= cost
    elif subject.cost_period == 'lesson':
        squad.lesson_bill -= cost
    squad.save()
def delete_subject(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('subject_id') and request.GET.get('squad_id'):
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')) )
        school = squad.school
        is_in_school(profile, school)
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')) )
        squad.subjects.remove(subject)
        subject.subject_lectures.filter(squad=squad).delete()
        cost = subject.cost
        if subject.cost_period == 'month':
            squad.bill -= cost
        elif subject.cost_period == 'lesson':
            squad.lesson_bill -= cost
        squad.save()
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
        school = lecture.squad.school
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

def const_create_lectures(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    squad = Squad.objects.get(id = id)
    school = squad.school
    is_in_school(profile, school)
    if request.GET.get('start') and request.GET.get('end') and request.GET.get('subject_id'):
        subject = school.school_subjects.get(id=int(request.GET.get('subject_id')))
        add_subject_work(school, squad, subject)
        teacher = squad.teacher
        category = subject.category.all()
        age = subject.age.all()
        level = subject.level.all()        
        tp = school.time_periods.get_or_create(
            start = request.GET.get('start'),
            end = request.GET.get('end')
            )[0]
        students = squad.students.all()
        for i in range(1, 8):
            if request.GET.get('day'+str(i)) == 'true':
                day = Day.objects.get(id=int(i))
                cell = day.day_cell.filter(time_period=tp)
                if len(cell) > 0:
                    cell = cell[0]
                else:
                    cell = day.day_cell.create(time_period=tp,school=school)
                lecture = squad.squad_lectures.create(
                    cell=cell,
                    day=day,
                    subject=subject,
                    office = squad.office,
                    )
                lecture.save()
                lecture.category.add(*category)
                lecture.age.add(*age)
                lecture.level.add(*level)
    data = {
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

def update_cards_money(request):
    if request.GET.get('secret') == 'NJf5wefewfm58keijnw':
        schools = School.objects.filter(version='standart').prefetch_related('groups__need_money')
        today = int(timezone.now().date().strftime('%d'))
        for school in schools:
            forward = today + school.pay_day_diff
            for squad in school.groups.filter(start_day=forward):
                stard_day = squad.start_date.strftime('%d')
                for nm in squad.need_money.all():
                    nm.money -= nm.bill
                    nm.save()
                    card = nm.card
                    if nm.money < nm.bill:
                        card.colour = 'red'
                    elif nm.money < 2*nm.bill:
                        card.colour = 'orange'
                    card.save()
        return JsonResponse({"id":today})

def get_student_discounts(request):
    profile = get_profile(request)
    only_managers(profile)
    res = []
    name = ''
    if request.GET.get('squad_id') and request.GET.get('student_id'):
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')))
        school = squad.school
        is_in_school(profile, school)
        student = Profile.objects.get(id = int(request.GET.get('student_id')))
        name = student.first_name
        card = student.card.get_or_create(school=school)[0]
        hisnm = card.need_money.get(squad=squad)
        discs = school.discounts.filter(nms=hisnm)
        for dis in discs:
            res.append(dis.id)
    return JsonResponse({"res":res, "name":name,})

def set_student_discounts(request):
    profile = get_profile(request)
    only_managers(profile)
    add = False
    if request.GET.get('id') and request.GET.get('squad_id') and request.GET.get('student_id'):
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')))
        school = squad.school
        is_in_school(profile, school)
        student = Profile.objects.get(id = int(request.GET.get('student_id')))
        card = student.card.get_or_create(school=school)[0]
        hisnm = card.need_money.get(squad=squad)
        
        this_disc = school.discounts.get(id=int(request.GET.get('id')))
        if this_disc in hisnm.discount_school.all():
            hisnm.discount_school.remove(this_disc)
        else:
            hisnm.discount_school.add(this_disc)
            add = True
    return JsonResponse({"add":add})

def move_money(request):
    profile = get_profile(request)
    school = profile.schools.first()
    only_managers(profile)
    ok = False
    if request.GET.get('id') and request.GET.get('from') and request.GET.get('to') and request.GET.get('amount'):
        student = Profile.objects.get(id = int(request.GET.get('id')))
        card = student.card.get_or_create(school=school)[0]
        need_money_from = card.need_money.get(id=int(request.GET.get('from')))
        need_money_to = card.need_money.get(id=int(request.GET.get('to')))
        squad1 = need_money_from.squad
        squad2 = need_money_to.squad
        school1 = squad1.school
        school2 = squad2.school
        if school1 != school and school2 != school:
            return Http404

        amount = int(request.GET.get('amount'))
        if amount <= need_money_from.money:
            need_money_from.money -= amount
            need_money_to.money += amount
            need_money_from.save()
            need_money_to.save()
            ok = True
        else:
            ok = 'NotEnouph'

    data = {
        "ok":ok,
        "from":need_money_from.money,
        "to":need_money_to.money
    }
    return JsonResponse(data)

from django.contrib.postgres.search import TrigramSimilarity

def searching_groups(request):
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
        squads = school.groups.annotate(similarity=similarity,).filter(similarity__gt=0.05*kef).order_by('-similarity')
        i = 0
        for squad in squads:
            image_url = ''
            if squad.image_icon:
                image_url = squad.image_icon.url
            res.append([squad.title, squad.get_absolute_url(), image_url])
            i+=1
            if i == 4:
                break

    data = {
        "res":res,
    }
    return JsonResponse(data)

def choose_color(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    school = is_moderator_school(request, profile)
    if request.GET.get('id'):
        squad = Squad.objects.get(id = id)
        if squad.school != school:
            return Http404
        squad.color_back = request.GET.get('id')
        squad.save()
    data = {
    }
    return JsonResponse(data)

def make_alive(request):
    profile = get_profile(request)
    only_directors(profile)
    school = is_moderator_school(request, profile)
    if request.GET.get('id'):
        squad = Squad.objects.get(id = int(request.GET.get('id')))
        squad.shown = True
        squad.save()
    data = {
    }
    return JsonResponse(data)

def delete_payment(request):
    ok = False
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('id'):
        school = is_moderator_school(request, profile)
        payment = school.payment_history.filter(id=int(request.GET.get('id')))
        if len(payment) > 0:
            do = False
            payment = payment[0]
            if profile == payment.action_author:
                do = True
            else:
                director = Profession.objects.get(title = 'Director')
                if director in profile.profession.all():
                    do = True
            if do:
                student = payment.user
                card = student.card.get(school=school)
                squad = payment.squad
                payment.canceled = True
                payment.save()
                add_money(student, school, squad, card, -1*payment.amount, profile)

    data = {
        "ok":True
    }
    return JsonResponse(data)