from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )
from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import dateutil.parser
from datetime import datetime, timedelta
from django.contrib.auth.models import User

from django.shortcuts import render, redirect

from .forms import *
from .models import *
from squads.models import *
from docs.models import *
from subjects.models import Day,Attendance,TimePeriod,SquadCell
from django.contrib.auth.forms import PasswordChangeForm

def change_profile(request):
    if not request.user.is_authenticated:
        raise Http404
    if request.user.is_authenticated:
        hisprofile = Profile.objects.get(user = request.user.id)

    form = ProfileForm(request.POST or None, request.FILES or None,instance=hisprofile)
    if form.is_valid():
        hisprofile = form.save(commit=False)
        hisprofile.save()

    if request.method == 'POST':
        print('de')
        password_form = PasswordChangeForm(request.user, request.POST)
        print(password_form)
        if password_form.is_valid():
            hisprofile.user = password_form.save()
            update_session_auth_hash(request, hisprofile.user)  # Important!
            login(request, hisprofile.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect(hisprofile.change_url())
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        password_form = PasswordChangeForm(request.user)

    context = {
        "profile": hisprofile, 
        'form':form,
        'password_form':password_form,
    }
    return render(request, "profile/change_profile.html", context)

def test_account(request):
    user = User.objects.get(id = 1)
    hisprofile = Profile.objects.get(user = user)
    if hisprofile.is_trener:
        hissubjects = hisprofile.teachers_subjects.all()
        hissquads = hisprofile.curators_squads.all()
    else:
        hissubjects = hisprofile.hissubjects.all()
        hissquads = hisprofile.squads.all()
    time_periods = TimePeriod.objects.all()
    form = ProfileForm(request.POST or None, request.FILES or None,instance=hisprofile)
    if form.is_valid():
        hisprofile = form.save(commit=False)
        hisprofile.save()
        return HttpResponseRedirect(hisprofile.get_absolute_url())

    homework_list = []
    found_classwork = False
    idet_urok = False
    classwork = []
    hislessonss = hislessons(hisprofile)
    context = {
        "profile":hisprofile,
        "hisprofile": hisprofile,
        "hisprofile_list":[hisprofile],
        'all_squads':Squad.objects.all(),
        'all_profiles':Profile.objects.all(),
        'hischarts':hischarts(hisprofile.squads.all()),
        'hisboards':hisboards(hisprofile),
        'days':Day.objects.all(),
        'hissquads':hissquads,
        'time_periods':time_periods,
        'classwork':hislessonss[2],
        'homeworks':hislessonss[0],
        'lesson_now':hislessonss[1],
    }
    return render(request, "profile.html", context)

def account_view(request, user = None):
    if not request.user.is_authenticated:
        raise Http404
    user = user.replace('_', ' ')
    user = User.objects.get(username = user)
    hisprofile = Profile.objects.get(user = user)
    if request.user.is_authenticated:
        yourprofile = Profile.objects.get(user = request.user.id)

    form = ProfileForm(request.POST or None, request.FILES or None,instance=hisprofile)
    if form.is_valid():
        hisprofile = form.save(commit=False)
        hisprofile.save()
        return HttpResponseRedirect(hisprofile.get_absolute_url())

    homework_list = []
    found_classwork = False
    idet_urok = False
    classwork = []

    hislessonss = hislessons(hisprofile)
    time_periods = TimePeriod.objects.all()
    if hisprofile.is_trener:
        hissubjects = hisprofile.teachers_subjects.all()
        hissquads = hisprofile.curators_squads.all()
    else:
        hissubjects = hisprofile.hissubjects.all()
        hissquads = hisprofile.squads.all()
    context = {
        "profile":yourprofile,
        "hisprofile": hisprofile,
        "hisprofile_list":[hisprofile],
        'all_squads':Squad.objects.all(),
        'all_profiles':Profile.objects.all(),
        'hischarts':hischarts(hisprofile.squads.all()),
        'hisboards':hisboards(hisprofile),
        'hissubjects':hissubjects,
        'days':Day.objects.all(),
        'hissquads':hissquads,
        'time_periods':time_periods,
        'classwork':hislessonss[2],
        'homeworks':hislessonss[0],
        'lesson_now':hislessonss[1],
    }
    return render(request, "profile.html", context)

def hislessons(hisprofile):
    res = []
    lesson_now = False
    classwork = []
    for subject in hisprofile.teachers_subjects.all():
        homeworks = []
        for squad in subject.squads.all():
            needed_timep = 'none'
            last_lecture = 'none'
            timenow_int = int(timezone.now().strftime('%H')) * 60 + int(timezone.now().strftime('%M'))
            for timep in TimePeriod.objects.all():
                tstart = timep.start.split(':')
                timep_start_int = int(tstart[0]) * 60 + int(tstart[1])
                tend = timep.end.split(':')
                timep_end_int =   int(tend[0]) * 60 + int(tend[1])
                if timenow_int >= timep_start_int and timenow_int <= timep_end_int:
                    needed_timep = timep

            sw = SquadWeek.objects.filter(squad=squad, actual=True)
            if len(sw) > 0:
                sw = sw[0]
                if needed_timep != 'none':
                    sc = SquadCell.objects.filter(squad=squad,date=timezone.now().date(),time_period = needed_timep)
                    if len(sc) > 0:
                        sc = sc[0]
                        if len(sc.subject_materials.filter(subject=subject)) > 0:
                            last_lecture = [squad, sc, sc.subject_materials.get(subject=subject)]
                            lesson_now = True
                            classwork = [[subject, [last_lecture]]]
                else:
                    for sc in sw.week_cells.all():
                        if sc.date > timezone.now().date():
                            if len(sc.subject_materials.filter(subject=subject)) > 0:
                                last_lecture = [squad, sc, sc.subject_materials.get(subject=subject)]
                
                if last_lecture == 'none' and lesson_now == False:
                    index = list(squad.weeks.all()).index(sw)
                    if index+1 < len(squad.weeks.all()):
                        found_in_this_week = False
                        for i in range(index+1, len(squad.weeks.all())):
                            if found_in_this_week:
                                break
                            sw = squad.weeks.all()[i]
                            for sc in sw.week_cells.all():
                                if sc.date > timezone.now().date():
                                    if len(sc.subject_materials.filter(subject=subject)) > 0:
                                        if len(sc.subject_materials.get(subject=subject).lessons.all()) > 0:
                                            last_lecture = [squad, sc, sc.subject_materials.get(subject=subject)]
                                            found_in_this_week = True
                                            break
                homeworks.append(last_lecture) 
        res.append([subject, homeworks])
    return res, lesson_now, classwork

def hischarts(hissquads):
    hischarts = []
    pprs_results = []
    # for sq in hissquads:
    #     for lesson in sq.lessons.all():
    #         pprs_results = []
    #         for ppr in lesson.papers.all():
    #             ppr_summary_result = 0
    #             for student in sq.followers.all():
    #                 resultt = 0
    #                 cnt = 0
    #                 for subtheme in ppr.subthemes.all():
    #                     if len(subtheme.task_list.all()) > 0:
    #                         ppr_summary_result += 100 * cnt/len(subtheme.task_list.all())
    #                     else:
    #                         ppr_summary_result = 0
    #             if len(sq.followers.all()) == 0:
    #                 result = 0
    #             else:
    #                 result = int( ppr_summary_result/len(sq.followers.all()) )
    #             pprs_results.append( [ppr, result] )

    #     hischarts.append([sq, pprs_results])
    return(hischarts)

def hisboards(hisprofile):
    hisboards = []
    for board in Board.objects.all():
        hiscolumns = []
        for column in board.columns.all():
            hiscards = []
            for card in column.cards.all():
                if hisprofile in card.user_list.all():
                    hiscards.append(card)
            if len(hiscards) > 0:
                hiscolumns.append([column, hiscards])
        if len(hiscolumns) > 0:
            hisboards.append([board, hiscolumns])
    return(hisboards)

def login_view(request):
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/")
    return render(request, "form.html", {"form":form, "title": title})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse

def att_present(request):
    profile = Profile.objects.get(user = request.user)
    if request.GET.get('id') and profile.is_trener:
        attendance = Attendance.objects.get(id = request.GET.get('id'))
        attendance.present = 'present'
        attendance.save()
    data = {
    }
    return JsonResponse(data)

def ChangeAttendance(request):
    if request.GET.get('id'):
        attendance = Attendance.objects.get(id = int(request.GET.get('id')))
        if request.GET.get('grade'):
            attendance.grade = int(request.GET.get('grade'))
        attendance.save()
    data = {
    }
    return JsonResponse(data)

def tell_about_corruption(request):
    profile = Profile.objects.get(user = request.user)
    ok = False
    if request.GET.get('text'):
        Corruption.objects.create(text=request.GET.get('text'),author_profile=profile, school=profile.school)
        ok = True
    data = {
        'ok':ok
    }
    return JsonResponse(data)

class ChangeTimeAPIToggle(APIView):    
    def get(self, request, format=None):
        data = {
            "like_num":0,
        }
        return Response(data)

class DeleteZaiavkaAPIToggle(APIView):    
    def get(self, request, id=None, format=None):
        zaiavka = Zaiavka.objects.get(id = id)
        zaiavka.delete()
        data = {
            "like_num":0,
        }
        return Response(data)
class DeleteFollowAPIToggle(APIView):    
    def get(self, request, id=None, format=None):
        follow = Follow.objects.get(id = id)
        follow.delete()
        data = {
            "like_num":0,
        }
        return Response(data)

def ChangePage(request):
    profile = Profile.objects.get(user = request.user.id)
    if request.GET.get('page'):
        page = request.GET.get('page')
        if page == 'cabinet':
            profile.page = '0' + profile.page[1:]
        if page == 'homework':
            profile.page = '2' + profile.page[1:]
        if page == 'profile_info':
            profile.page = '0profile_info'
        if page == 'profile_lesson':
            profile.page = '0profile_lesson'
        if page == 'profile_attendance':
            profile.page = '0profile_attendance'
        if page == 'profile_zaiavki':
            profile.page = '0profile_zaiavki'
        if page == 'profile_squads':
            profile.page = '0profile_squads'

        profile.save()
    data = {
        "like_num":0,
    }
    return JsonResponse(data)


def register_view(request):
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        password2 = form.cleaned_data.get('password2')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)

        profile = Profile.objects.get(user = new_user)
        profile.rating = 0

        for i in range(0, 28):
            profile.schedule.append('free')
        profile.save()
        if next:
            return redirect(next)
        return redirect("/")

    context = {
        "form": form,
        "title": title,
        "timetable": timetable,        
    }
    return render(request, "form.html", context)

def logout_view(request):
    logout(request)
    return redirect("/")