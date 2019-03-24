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
        "subjects":school.school_subjects.all(),
        "all_students":school.people.filter(),
    }
    return render(request, "school/school_rating.html", context)

def school_info(request):
    profile = get_profile(request)
    school = profile.schools.first()
    context = {
        "profile":profile,
        "instance": profile.schools.first(),
        "squads":school.groups.all(),
        "subjects":school.school_subjects.all(),
    }
    return render(request, "school/info.html", context)

def school_teachers(request):
    profile = get_profile(request)
    school = profile.schools.first()
    context = {
        "profile":profile,
        "instance": school,
        "all_teachers":school.people.filter(),    
    }
    return render(request, "school/all_teachers.html", context)

def school_crm(request):
    profile = get_profile(request)
    school = profile.schools.first()
    time_periods = school.time_periods.all()

    context = {
        "profile":profile,
        "instance": profile.schools.first(),
        "subject_categories":school.school_subject_categories.all(),
        "ages":school.school_subject_ages.all(),
        "offices":school.school_offices.all(),
        'days':Day.objects.all(),
        'time_periods':time_periods,
        "registration":"registration",
    }
    return render(request, "school/register_students.html", context)

def school_students(request):
    profile = get_profile(request)
    school = profile.schools.first()    
    context = {
        "profile":profile,
        "instance": profile.schools.first(),
        "all_students":school.people.filter(),
        "students":"students",
    }
    return render(request, "school/all_students.html", context)

def school_requests(request):
    profile = get_profile(request)
    school = profile.schools.first()
    context = {
        "profile":profile,
        "instance": profile.schools.first(),
        "all_students":school.zaiavkas.all(),
        "requests":"requests",
    }
    return render(request, "school/all_students.html", context)

def school_recalls(request):
    profile = get_profile(request)
    school = profile.schools.first()
    context = {
        "profile":profile,
        "instance": school,
        "all_students":school.people.filter(),
        "recalls":"recalls"
    }
    return render(request, "school/all_students.html", context)

def school_courses(request):
    profile = get_profile(request)
    context = {
        "profile":profile,
        "instance": profile.schools.first(),
        "courses":"courses",
    }
    return render(request, "school/all_courses.html", context)

def school_list(request):
    if not request.user.is_authenticated:
        raise Http404        
    profile = get_profile(request)
    context = {
        "profile": profile,
        "schools":School.objects.all(),
    }
    return render(request, "schools/school_list.html", context)

def school_update(request, slug=None):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
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
    }
    return render(request, "schools/school_create.html", context)


def school_delete(request, slug=None):
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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse
import string
import random

def register_to_school(request):
    manager_profile = Profile.objects.get(user = request.user.id)
    school = manager_profile.schools.first()
    if request.GET.get('name') and request.GET.get('phone') and request.GET.get('mail') and request.GET.get('status'):
        new_id = User.objects.order_by("id").last().id + 1
        symbols = string.ascii_letters + string.digits
        password = ''
        for i in range(0, 9):
            password += random.choice(symbols)
        user = User.objects.create(username='user' + str(new_id))
        user.set_password(password)
        user.save()
        profile = Profile.objects.get(user = user)
        profile.first_name = request.GET.get('name')
        profile.phone = request.GET.get('phone')
        profile.mail = request.GET.get('mail')
        profile.save()
        profile.schools.add(school)
        squad_id = int(request.GET.get('squad_id'))
        if squad_id > 0:
            squad = Squad.objects.get(id=squad_id)
            squad.students.add(profile)
            for subject in squad.subjects.all():
                subject.students.add(profile)
    data = {
        'password':password
    }
    return JsonResponse(data)

def crm_option(request):
    profile = Profile.objects.get(user = request.user.id)
    if request.GET.get('object_id') and request.GET.get('option'):
        print(request.GET.get('object_id') , request.GET.get('option'))
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
        profile.save()
    data = {
    }
    return JsonResponse(data)
