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
from todolist.models import *
from subjects.models import *
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
  
    context = {
        "profile":hisprofile,
        "hisprofile": hisprofile,
        "hisprofile_list":[hisprofile],
        'all_squads':Squad.objects.all(),
        'all_profiles':Profile.objects.all(),
        'hisboards':hisboards(hisprofile),
        'hissubjects':hissubjects,
        'days':Day.objects.all(),
        'hissquads':hissquads,
        'time_periods':time_periods,
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

    time_periods = TimePeriod.objects.all()
    if hisprofile.is_trener:
        hissubjects = hisprofile.teachers_subjects.all()
        hissquads = hisprofile.curators_squads.all()
    else:
        hissubjects = hisprofile.hissubjects.all()
        hissquads = hisprofile.squads.all()

    first_squad = ''
    first_subject = ''
    if len(hissquads) > 0:
        first_squad = hissquads[0].id
        first_subject = hissubjects[0].id,

    context = {
        "profile":yourprofile,
        "hisprofile": hisprofile,
        "hisprofile_list":[hisprofile],
        'hisboards':hisboards(hisprofile),
        'days':Day.objects.all(),
        'hissubjects':hissubjects,
        'hissquads':hissquads,
        'first_squad':first_squad,
        'first_subject':first_subject,
        'time_periods':time_periods,
        #'hisschedule':hisschedule(hissquads, hissubjects),
    }
    return render(request, "profile.html", context)

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
        password = form.cleaned_data.get("password")
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

def update_schedule(request):
    hisprofile = Profile.objects.get(user = request.user)
    if hisprofile.is_trener:
        hissubjects = hisprofile.teachers_subjects.all()
        hissquads = hisprofile.curators_squads.all()
    else:
        hissubjects = hisprofile.hissubjects.all()
        hissquads = hisprofile.squads.all()

    for timep in TimePeriod.objects.all():
        for day in Day.objects.all():
            if day.number != 7:
                cell = hisprofile.hisschedule.get_or_create(x=day.number,y=timep.num)[0]
                cell.subjects = []
                cell.squads = []
                cell.colors = []
                cell.teachers = []
                cell.cabinets = []
                cell.indexes = []
                cell.save()

    for subject in hissubjects:
        print(subject.title)
        for lecture in subject.subject_lectures.all():
            print(lecture.id)
            if lecture.squad in hissquads and subject.teacher.first():
                cell = hisprofile.hisschedule.get(x = lecture.cell.day.number,y=lecture.cell.time_period.num)
                cell.subjects.append(subject.title)
                cell.squads.append(lecture.squad.id)
                cell.colors.append(subject.color_back)
                cell.teachers.append(subject.teacher.first().first_name)
                cell.cabinets.append(subject.cabinet)
                cell.indexes.append(len(cell.subjects) - 1)
                cell.save()
    data = {
    }
    return JsonResponse(data)

def hisattendance(request):
    if request.GET.get('subject_id') and request.GET.get('class_id'):
        subject_id = int(request.GET.get('subject_id'))
        squad_id = int(request.GET.get('class_id'))
        subject = Subject.objects.get(id = subject_id)
        squad = Squad.objects.get(id = squad_id)

        squads = []
        for sq in subject.squads.all():
            squads.append(sq.title)

        students = []
        for student in squad.students.all():
            students.append(student.first_name)
            
        columns = []
        for sm in subject.materials.order_by('-id'):
            if len(columns) == 4:
                break
            if len(sm.material_cells.filter(squad=squad)) > 0:
                squad_cell = sm.material_cells.filter(squad=squad)[0]
                grades = [sm.id, squad_cell.date.strftime('%d %B %Y'), squad_cell.time_period.start + '-' + squad_cell.time_period.end]
                for attendance in squad_cell.attendances.filter(subject=subject, squad=squad):
                    if attendance.squad_cell.date + timedelta(2) >= timezone.now().date() and attendance.squad_cell.date < timezone.now().date():
                        grades.append(attendance.id)
                    if attendance.grade > 0:
                        grades.append(attendance.grade)
                    else:
                        grades.append('')
                columns.append(grades)
        data = {
            'classes':squads,
            'students':students,
            'columns':columns,
        }
        return JsonResponse(data)

def more_attendance(): 
    if request.GET.get('subject_id') and request.GET.get('class_id') and request.GET.get('direction') and request.GET.get('sm_id'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')))
        squad = Squad.objects.get(id = int(request.GET.get('class_id')))
        current_sm = int(request.GET.get('sm_id'))
        columns = []
        if request.GET.get('direction') == 'left':
            queryset = subject.materials.filter(id__lt = current_sm)
        else:
            queryset = subject.materials.filter(id__gt = current_sm)
        for sm in queryset:
            if len(columns) == 4:
                break
            if len(sm.material_cells.filter(squad=squad)) > 0:
                squad_cell = sm.material_cells.filter(squad=squad)[0]
                grades = [squad_cell.date.strftime('%d %B %Y'), squad_cell.time_period.start + '-' + squad_cell.time_period.end]
                for attendance in squad_cell.attendances.filter(subject=subject, squad=squad):
                    if attendance.squad_cell.date + timedelta(2) >= timezone.now().date() and attendance.squad_cell.date < timezone.now().date():
                        grades.append(attendance.id)
                    if attendance.grade > 0:
                        grades.append(attendance.grade)
                    else:
                        grades.append('')
                columns.append(grades)
        data = {
            'classes':squads,
            'students':students,
            'columns':columns,
        }
        return JsonResponse(data)

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

def logout_view(request):
    logout(request)
    return redirect("/")