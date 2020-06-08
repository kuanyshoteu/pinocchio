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
from squads.models import Squad,PaymentHistory,SquadHistory,DiscountSchool
from subjects.templatetags.ttags import get_date, get_pay_date,constant_school_lectures
from squads.views import remove_student_from_squad, add_student_to_squad, prepare_mail
from accounts.models import Profile,CRMCardHistory
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.contrib.auth.models import User
import os
from constants import *
from .social_media import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse
import json
import urllib
from django.contrib.postgres.search import TrigramSimilarity
from dateutil.relativedelta import relativedelta

def send_mails(request):
    profile = Profile.objects.get(user = request.user.id)
    school = is_moderator_school(request, profile)
    only_managers(profile)
    text = request.GET.get('text')
    addresses = request.GET.get('addresses')
    ok = False
    print(text, addresses)
    if text:
        head = request.GET.get('head')
        for mail in addresses.split(','):
            if '@' in mail:
                try:
                    send_email(head, text, [mail])
                except Exception as e:
                    raise
        ok = True
    data = {
        "ok": ok,
    }
    return JsonResponse(data)

def get_mail_students_list(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    res = []
    if request.GET.get('page'):
        print('eee')
        page = int(request.GET.get('page'))
        school = is_moderator_school(request, profile)
        squad = profile.filter_data.squad
        if squad != None:
            squads = [squad]
        else:
            if profile.filter_data.office:
                squads = school.groups.filter(shown=True,office=profile.filter_data.office).prefetch_related('students')
            else:
                squads = school.groups.filter(shown=True).prefetch_related('students')
        if profile.filter_data.subject_category:
            subjects = school.school_subjects.filter(category=profile.filter_data.subject_category)
            squads = squads.filter(subjects__in=subjects)
        students = school.people.filter(is_student=True, squads__in=squads).exclude(card=None).exclude(squads=None).distinct()
        if len(students) <= (page-1)*16:
            return JsonResponse({"ended":True})
        p = Paginator(students, 16)
        page1 = p.page(page)
        res = []
        for student in page1.object_list:
            res.append([
                student.first_name,
                student.mail,
                ])
    data = {
        "res":res,
    }
    return JsonResponse(data)
