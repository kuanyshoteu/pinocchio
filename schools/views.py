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

def school_rating(request):
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    
    context = {
        "profile":profile,
        "instance": profile.school,
        "squads":Squad.objects.all(),
        "subjects":Subject.objects.all(),
        "all_students":Profile.objects.filter(is_trener = False),
    }
    return render(request, "school/school_rating.html", context)

def school_info(request):
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    context = {
        "profile":profile,
        "instance": profile.school,
        "squads":Squad.objects.all(),
        "subjects":Subject.objects.all(),    
    }
    return render(request, "school/info.html", context)

def school_teachers(request):
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    context = {
        "profile":profile,
        "instance": profile.school,
        "all_teachers":Profile.objects.filter(is_trener = True),    
    }
    return render(request, "school/all_teachers.html", context)

def school_crm(request):
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    context = {
        "profile":profile,
        "instance": profile.school,
        "all_students":Profile.objects.filter(is_trener = False),
        "students":"students",
    }
    return render(request, "school/all_students.html", context)

def school_requests(request):
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    context = {
        "profile":profile,
        "instance": profile.school,
        "all_students":Zaiavka.objects.all(),
        "requests":"requests",
    }
    return render(request, "school/all_students.html", context)

def school_recalls(request):
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    context = {
        "profile":profile,
        "instance": profile.school,
        "all_students":Profile.objects.filter(is_trener = False),
        "recalls":"recalls"
    }
    return render(request, "school/all_students.html", context)

def school_courses(request):
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    context = {
        "profile":profile,
        "instance": profile.school,
        "courses":"courses",
    }
    return render(request, "school/all_courses.html", context)

def school_list(request):
    if not request.user.is_authenticated:
        raise Http404

    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"
        
    profile = ''

    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    
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
        
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)

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

    data = {
        'password':password
    }
    return JsonResponse(data)
