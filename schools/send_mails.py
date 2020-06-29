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
    order = request.GET.get('order')
    text = request.GET.get('text')
    addresses = request.GET.get('addresses')
    ok = 'no'
    if text:
        head = request.GET.get('head')
        cards = school.crm_cards.all()
        if '8%'+'next_lesson_date_tag'+'%8' in text or '8%'+'next_lesson_time_tag'+'%8' in text or '8%'+'next_lesson_timeend_tag'+'%8' in text:
            need_next_lesson = True
        else:
            need_next_lesson = False
        today = timezone.now().date()
        nocard = []
        nosquad = []
        noschedule = []
        found_error = False
        mails = addresses.split(',')
        if order == 'check':
            for mail in mails:
                if '@' in mail:
                    check = check_tags(mail,text,school,today,need_next_lesson,cards)
                    if check[0] != 'ok':
                        found_error = True
                        if check[0] == 'nocard':
                            nocard.append(check[1])
                        elif check[0] == 'nosquad':
                            nosquad.append([check[1], mail])
                        elif check[0] == 'noschedule':
                            noschedule.append([check[1], check[2]])
            if found_error:
                data = {
                    'ok':'found_error',
                    'nocard':nocard,
                    'nosquad':nosquad,
                    'noschedule':noschedule,
                }
                return JsonResponse(data)
        for mail in mails:
            if '@' in mail:
                text = prepare_tags(mail,text,school,today,need_next_lesson,cards)
                if text != False:
                    try:
                        send_email_client(head, text, [mail])
                    except Exception as e:
                        raise
        ok = 'yes'
    data = {
        "ok": ok,
    }
    return JsonResponse(data)

def check_tags(mail, text, school, today, need_next_lesson, cards):
    card = cards.filter(mail=mail)
    if len(card) > 0:
        card = card[0]
    else:
        return ['nocard', mail]
    if need_next_lesson:
        student = card.card_user
        if len(card.bill_data.all()) == 0:
            return ['nosquad', card.name]
        squad = card.bill_data.all().order_by('start_date').first().squad
        if len(squad.squad_lectures.all()) == 0:
            return ['noschedule', card.name, squad.title]
    return ['ok']

def prepare_tags(mail, text, school, today, need_next_lesson, cards):
    card = cards.filter(mail=mail)
    name = ''
    next_lesson_date = ''
    next_lesson_time = ''
    next_lesson_timeend = ''
    next_payment_date = ''
    if len(card) > 0:
        card = card[0]
        name = card.name
        text = text.replace('8%'+'student_name_tag'+'%8', card.name)
        if need_next_lesson:
            student = card.card_user
            if len(card.bill_data.all()) == 0:
                return False
            bill_data = card.bill_data.all().order_by('start_date').first()
            squad = bill_data.squad
            if len(squad.squad_lectures.all()) == 0:
                return False
            today_num = int(today.strftime('%w'))
            today_day = Day.objects.get(number=today_num)
            pn_day = Day.objects.get(number=1)
            next_lecture = squad.squad_lectures.filter(day__gte=today_day)
            if len(next_lecture) == 0:
                next_lecture = squad.squad_lectures.filter(day__gte=pn_day)
            next_lecture = next_lecture.first()
            diff = next_lecture.day.number - today_num
            if diff < 0:
                diff += 7
            next_lesson_date = (today + timedelta(diff)).strftime('%d %B')
            next_lesson_time = next_lecture.cell.time_period.start
            next_lesson_timeend = next_lecture.cell.time_period.end
            next_payment_date = bill_data.pay_date.strftime("%d %B %Y")
    text = text.replace('8%'+'student_name_tag'+'%8', name)
    text = text.replace('8%'+'next_lesson_date_tag'+'%8', next_lesson_date)
    text = text.replace('8%'+'next_lesson_time_tag'+'%8', next_lesson_time)
    text = text.replace('8%'+'next_lesson_timeend_tag'+'%8', next_lesson_timeend)
    text = text.replace('8%'+'next_payment_tag'+'%8', next_payment_date)
    return text

def get_mail_students_list(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    res = []
    all_students_len = 0
    crnt_students_len = 0
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
        school = is_moderator_school(request, profile)
        squad = profile.filter_data.squad_mail
        squads = school.groups.filter(shown=True).prefetch_related('students')
        all_students_len = len(school.people.filter(is_student=True, squads__in=squads).exclude(card=None).exclude(squads=None).distinct())
        if squad != None:
            squads = school.groups.filter(id = squad.id)
        else:
            if profile.filter_data.office_mail:
                squads = school.groups.filter(shown=True,office=profile.filter_data.office).prefetch_related('students')
        if profile.filter_data.subject_category_mail or profile.filter_data.subject_mail:
            if profile.filter_data.subject_category_mail:
                subjects = school.school_subjects.filter(category=profile.filter_data.subject_category_mail)
            else:
                subjects = school.school_subjects.all()                
            if profile.filter_data.subject_mail:
                subjects = subjects.filter(id=profile.filter_data.subject_mail.id)
            squads = squads.filter(subjects__in=subjects)
        students = school.people.filter(is_student=True, squads__in=squads).exclude(card=None).exclude(squads=None).distinct()
        crnt_students_len = len(students)
        if crnt_students_len <= (page-1)*16:
            return JsonResponse({
                "ended":True,
                "crnt_students_len":crnt_students_len,
                "all_students_len":all_students_len,
                })
        p = Paginator(students, 16)
        page1 = p.page(page)
        res = []
        today = timezone.now().date()
        bill_day_diff = school.bill_day_diff
        for student in page1.object_list:
            res.append([
                student.id,
                student.first_name,
                student.mail,
                student.get_absolute_url(),
                ])
        print(len(res))
    data = {
        "res":res,
        "ended":False,
        "all_students_len":all_students_len,
        "crnt_students_len":crnt_students_len,
    }
    return JsonResponse(data)

def change_mail_option(request):
    profile = Profile.objects.get(user = request.user.id)
    if request.GET.get('object_id') and request.GET.get('option'):
        filter_data = profile.filter_data
        if request.GET.get('option') == 'subject_category':
            if int(request.GET.get('object_id')) == -1:
                filter_data.subject_category_mail = None
            else:
                category = SubjectCategory.objects.get(id = int(request.GET.get('object_id')))
                filter_data.subject_category_mail = category
        if request.GET.get('option') == 'office':
            if int(request.GET.get('object_id')) == -1:
                filter_data.office_mail = None
            else:
                office = Office.objects.get(id = int(request.GET.get('object_id')))
                filter_data.office_mail = office
        if request.GET.get('option') == 'group':
            if int(request.GET.get('object_id')) != -1:
                school = is_moderator_school(request, profile)
                squad = school.groups.get(id = int(request.GET.get('object_id')))
                filter_data.squad_mail = squad
            else:
                filter_data.squad_mail = None                
        if request.GET.get('option') == 'subject':
            if int(request.GET.get('object_id')) != -1:
                subject = Subject.objects.get(id = int(request.GET.get('object_id')))
                filter_data.subject_mail = subject
            else:
                filter_data.subject_mail = None                
        filter_data.save()
    data = {
    }
    return JsonResponse(data)

def save_mail_template(request):
    profile = Profile.objects.get(user = request.user.id)
    only_managers(profile)
    title = request.GET.get('title')
    text = request.GET.get('text')
    tid = -1
    if title and text:
        school = is_moderator_school(request, profile)
        if len(school.mail_templates.filter(title=title)) == 0 and len(school.mail_templates.filter(text=text)) == 0:
            temp = school.mail_templates.create(
                title=title,
                text=text,
                )
            temp.save()
            tid = temp.id
    data = {
        "tid":tid,
    }
    return JsonResponse(data)
