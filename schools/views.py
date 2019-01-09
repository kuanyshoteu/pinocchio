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
import pandas as pd
import os

def school_detail(request, slug=None):
    instance = get_object_or_404(School, slug=slug)
    profile = 'admin'
    is_auth = False
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
        is_auth = True

    time_periods = TimePeriod.objects.all()
    context = {
        "instance": instance,
        "school_url":instance.get_absolute_url(),
        "profile":profile,
        'time_periods':time_periods,
        "all_teachers":Profile.objects.filter(is_trener = True),
        "all_students":Profile.objects.filter(is_trener = False),
    }
    return render(request, "schools/school_detail.html", context)

def school_list(request):
    if not request.user.is_authenticated:
        raise Http404

    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"
        
    profile = 'admin'

    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    
    context = {
        "profile": profile,
        "schools":School.objects.all(),
    }
    return render(request, "schools/school_list.html", context)

def school_create(request):
    if not request.user.is_authenticated:
        raise Http404

    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    if not profile.is_trener:
        raise Http404
        
    form = SchoolForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_update_url())   
    
    context = {
        "form": form,
        "profile":profile,
    }
    return render(request, "schools/school_create.html", context)

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
        
    profile = 'admin'
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


def change_curator(request):
    if request.GET.get('teacher_id') and request.GET.get('subject_id'):
        school = School.objects.get(id = int(request.GET.get('subject_id')) )
        curator = Profile.objects.get(id = int(request.GET.get('teacher_id')) )
        for oldteacher in school.curator.all():
            school.curator.remove(oldteacher)
        school.curator.add(curator)
    data = {
    }
    return JsonResponse(data)
