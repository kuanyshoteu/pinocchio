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

from .forms import SquadForm
from .table_change_form import TableChangeForm
from .models import *
from schools.models import School
from subjects.models import *
from papers.models import *
from library.models import Folder
from accounts.models import Profile, MainPage
from accounts.forms import *
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.contrib.auth.models import User
import pandas as pd
import os

def squad_detail(request, slug=None):
    school = School.objects.all()[0]
    for p in Profile.objects.all():
        p.school = school
        p.save()

    # ff = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # file = str(ff) + "/abc.xlsx"
    # data = pd.read_excel(file,header=None) #reading file
    # a = data.values.tolist()
    # for row in a:
    #     new_id = User.objects.using('akuir').order_by("id").last().id + 1
    #     user = User.objects.create(username='user' + str(new_id), password=str(row[1]))
    #     profile = Profile.objects.get(user = user)
    #     profile.first_name = row[0]
    #     profile.phone = str(row[2])
    #     profile.save()

    instance = get_object_or_404(Squad, slug=slug)
    profile = 'admin'
    is_auth = False
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
        is_auth = True

    in_squad = 'no'
    if profile in instance.students.all():
        in_squad = 'yes'

    time_periods = TimePeriod.objects.all()
    days = Day.objects.all()
    cells = Cell.objects.all()
    if len(cells) < len(days) * len(time_periods):
        for day in days:
            for timep in time_periods:
                new_cell = Cell.objects.get_or_create(day = day, time_period = timep)

    update_actual_week(instance)
    context = {
        "instance": instance,
        "squad_url":instance.get_absolute_url(),
        "profile":profile,
        'time_periods':time_periods,
    }
    return render(request, "squads/squad_detail.html", context)

def update_actual_week(instance):
    next_week_actual = False
    for week in instance.weeks.all():
        if len(week.week_cells.all()) > 0:
            if week.week_cells.all()[len(week.week_cells.all())-1].date>=timezone.now().date() and timezone.now().date()>=week.week_cells.all()[0].date:
                if timezone.now().date() > week.week_cells.all()[len(week.week_cells.all())-1].date:
                    next_week_actual = True
                else:
                    week.actual = True
                    week.save()
            else:
                if next_week_actual:
                    week.actual = True
                    next_week_actual = False
                else:
                    week.actual = False
                    week.save()

def squad_list(request):
    if not request.user.is_authenticated:
        raise Http404

    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"
        
    profile = 'admin'

    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)

    main_page = 'de'
    if len(MainPage.objects.all()) < 1:
        main_page = MainPage.objects.create()
    else:
        main_page = MainPage.objects.all()[0]
    
    context = {
        "staff" : staff,
        "profile": profile,
        "user":request.user,
        "squads":Squad.objects.all(),
        'main_page':main_page,
        "squad_categories":SquadCategory.objects.all(),
    }
    return render(request, "squads/squad_list.html", context)

def squad_videos(request, slug=None):
    instance = get_object_or_404(Squad, slug=slug)
    context = {
        "instance": instance,
    }
    return render(request, "squads/squad_videos.html", context)

def squad_lessons(request, slug=None):
    instance = get_object_or_404(Squad, slug=slug)
    main_page = 'de'
    if len(MainPage.objects.all()) < 1:
        main_page = MainPage.objects.create()
    else:
        main_page = MainPage.objects.all()[0]
    context = {
        "instance": instance,
        "main_page":main_page,
    }
    return render(request, "squads/squad_lessons.html", context)

def squad_create(request):
    if not request.user.is_authenticated:
        raise Http404

    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    if not profile.is_trener:
        raise Http404
        
    form = SquadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.start_date = timezone.now().date()
        instance.end_date = timezone.now().date()
        instance.save()
        return HttpResponseRedirect(instance.get_update_url())   
    
    context = {
        "form": form,
        "profile":profile,
        "all_teachers":Profile.objects.filter(is_trener = True),
    }
    return render(request, "squads/squad_create.html", context)

def squad_update(request, slug=None):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Squad, slug=slug)
    form = SquadForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if not instance.height_field:
            instance.height_field = 0
        if not instance.width_field:
            instance.width_field = 0

        for subject in instance.subjects.all():
            for student in instance.students.all():
                subject.students.remove(student)
        for student in Profile.objects.filter(is_trener = False):
            data_string = request.POST.get('student' + str(student.id))
            if data_string == 'on':
                instance.students.add(student)
            else:
                instance.students.remove(student)
        for subject in instance.subjects.all():
            for student in instance.students.all():
                subject.students.add(student)
        for subject in instance.subjects.all():
            for sm in subject.materials.all():
                for student in instance.students.all():    
                    sc = sm.material_cells.filter(squad=instance)
                    if len(sc)>0:
                        att = Attendance.objects.get_or_create(subject_materials=sm,student=student,subject=subject,squad_cell=sc[0])   
                        att[0].squad = instance
                        att[0].save()

        instance.save()
        return HttpResponseRedirect(instance.get_update_url())
        
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)

    context = {
        "instance": instance,
        "form":form,
        "user":request.user,
        "profile":profile,
        "all_teachers":Profile.objects.filter(is_trener = True),
        "all_students":Profile.objects.filter(is_trener = False),
    }
    return render(request, "squads/squad_create.html", context)


def squad_delete(request, slug=None):
    if not request.user.is_authenticated:
        raise Http404
    try:
        instance = Squad.objects.get(slug=slug)
    except:
        raise Http404

    if not request.user.is_staff and not request.user.is_superuser:
        reponse.status_code = 403
        return HttpResponse("You do not have permission to do this.")
        
    if request.method == "POST":
        instance.delete()
        messages.success(request, "Successfully deleted")
        return redirect("squads:list")
    context = {
        "object": instance
    }
    return render(request, "confirm_delete.html", context)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse

def add_paper(request):
    if request.GET.get('group_id'):
        squad = Squad.objects.get(id = int(request.GET.get('group_id')) )
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
    if request.GET.get('id'):
        squad = Squad.objects.get(id = int(request.GET.get('id')) )
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
    if request.GET.get('instance_id'):
        squad = Squad.objects.get(id = int(request.GET.get('instance_id')) )
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
    if request.GET.get('teacher_id') and request.GET.get('subject_id'):
        squad = Squad.objects.get(id = int(request.GET.get('subject_id')) )
        curator = Profile.objects.get(id = int(request.GET.get('teacher_id')) )
        for oldteacher in squad.curator.all():
            squad.curator.remove(oldteacher)
        squad.curator.add(curator)
    data = {
    }
    return JsonResponse(data)
