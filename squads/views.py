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
    time_periods = profile.histime_periods.all()
    days = Day.objects.all()
    context = {
        "instance": instance,
        "squad_url":instance.get_absolute_url(),
        "profile":profile,
        'time_periods':time_periods,
        'days':days
    }
    return render(request, "squads/squad_detail.html", context)

def squad_list(request):
    profile = get_profile(request)
    context = {
        "profile": profile,
        "squads":Squad.objects.all(),
    }
    return render(request, "squads/squad_list.html", context)

def squad_videos(request, slug=None):
    instance = get_object_or_404(Squad, slug=slug)
    profile = get_profile(request)
    context = {
        "profile": profile,
        "instance": instance,
    }
    return render(request, "squads/squad_videos.html", context)

def squad_lessons(request, slug=None):
    instance = get_object_or_404(Squad, slug=slug)
    profile = get_profile(request)
    context = {
        "profile": profile,
        "instance": instance,
    }
    return render(request, "squads/squad_lessons.html", context)

def squad_create(request):
    profile = get_profile(request)
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
        "all_teachers":Profile.objects.filter(),
    }
    return render(request, "squads/squad_create.html", context)

def squad_update(request, slug=None):
    profile = get_profile(request)
    if not is_profi(profile, 'Manager'):
        raise Http404
    instance = get_object_or_404(Squad, slug=slug)
    school = profile.schools.first()
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
        for student in school.people.filter(is_student=True):
            data_string = request.POST.get('student' + str(student.id))
            if data_string == 'on':
                instance.students.add(student)
            else:
                instance.students.remove(student)
        for subject in instance.subjects.all():
            for student in instance.students.all():
                subject.students.add(student)

        instance.save()
        return HttpResponseRedirect(instance.get_update_url())        
    context = {
        "instance": instance,
        "form":form,
        "profile":profile,
        "all_teachers":Profile.objects.filter(),
        "all_students":Profile.objects.filter(),
    }
    return render(request, "squads/squad_create.html", context)


def squad_delete(request, slug=None):
    profile = get_profile(request)
    instance = Squad.objects.get(slug=slug)

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
