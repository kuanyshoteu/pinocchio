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
from datetime import timedelta
from django.contrib.auth.models import User

from django.shortcuts import render, redirect

from .forms import *
from .models import *
from squads.models import *
from todolist.models import *
from subjects.models import *
from django.contrib.auth.forms import PasswordChangeForm
from schools.models import School
from constants import *
from subjects.templatetags.ttags import get_date, check_date, create_atts, create_atts_student

def account_view(request, user = None):
    profile = get_profile(request)
    user = user.replace('_', ' ')
    user = User.objects.get(username = user)
    hisprofile = Profile.objects.get(user = user)
    if hisprofile.first_name == 'name':
        hisprofile.first_name = user.first_name + ' ' + user.last_name
        hisprofile.save()
    miss_lesson = MissLesson.objects.filter(profile = profile)
    if len(miss_lesson) > 0:
        miss_lesson = miss_lesson[0]
        miss_lesson_form = MissLessonForm(request.POST or None, request.FILES or None, instance=miss_lesson)
    else:
        miss_lesson_form = MissLessonForm(request.POST or None, request.FILES or None)
    if miss_lesson_form.is_valid():
        miss_lesson = miss_lesson_form.save()
        return redirect(profile.get_absolute_url())

    if is_profi(hisprofile, 'Teacher'):
        hissubjects = hisprofile.teacher_subjects.all()
        hissquads = hisprofile.hissquads.all()
        hiscourses = hisprofile.hiscourses.all()
    else:
        hissubjects = hisprofile.hissubjects.all()
        hissquads = hisprofile.squads.all()
        hiscourses = hisprofile.courses.all()
    hiscacheatt = CacheAttendance.objects.get_or_create(profile = profile)[0]
    if hiscacheatt.subject == None and len(hissubjects) > 0:
        hiscacheatt.subject = hissubjects[0]
        hiscacheatt.save()
    if hiscacheatt.squad == None and len(hissquads) > 0:
        hiscacheatt.squad = hissquads[0]
        hiscacheatt.save()
    if not profile.skill:
        skill = Skill.objects.create()
        profile.skill = skill
        profile.save()
    else:
        skill = profile.skill
    if profile == hisprofile and skill.confirmed == False:
        if timezone.now() - skill.confirmation_time > timedelta(1):
            skill.confirmation_code = random_secrete_confirm()
            skill.confirmation_time = timezone.now()
            skill.save()
            url = request.build_absolute_uri().replace(request.get_full_path(), '') + '/confirm/?confirm='+profile.skill.confirmation_code
            text = "Здравствуйте "+profile.first_name+ "!<br><br> Вы зарегестрировались на сайте Pinocchio.kz, для подтверждения вашего Email пожалуйста пройдите по ссылке: "
            html_content = text + "<br><a href='"+url+"'>подтвердить</a><br><br>С уважением, команда Pinocchio.kz"
            send_email("Подтверждение", html_content, [profile.mail])
        context = {
            "profile": profile,
        }
        return render(request, "confirm.html", context)
    school_money = 0
    is_director = is_profi(profile, 'Director')
    if is_director:
        school_money = profile.schools.first().money
    context = {
        "profile":profile,
        "hisprofile": hisprofile,
        'hisboards':hisboards(hisprofile),
        'days':Day.objects.all(),
        'time_periods':hisprofile.histime_periods.all(),
        'hissubjects':hissubjects,
        'hissquads':hissquads,
        'hiscourses':hiscourses,
        'att_subject':hiscacheatt.subject,
        'att_squad':hiscacheatt.squad,
        'today':int(timezone.now().date().strftime('%w')),
        'miss_lesson_form':miss_lesson_form,
        'is_this_trener':is_profi(hisprofile, 'Teacher'),
        "is_this_manager":is_profi(hisprofile, 'Manager'),
        "is_this_director":is_profi(hisprofile, 'Director'),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_director,
        'hint':skill.hint_numbers[0],
        "school_money":school_money,
    }
    return render(request, "profile.html", context)

def hisboards(hisprofile):
    hisboards = []
    if is_profi(hisprofile, 'Student') == False:
        for school in hisprofile.schools.all():
            for board in school.school_boards.all():
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
        password_form = PasswordChangeForm(request.user, request.POST)
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
        'is_trener':is_profi(hisprofile, 'Teacher'),
        "is_manager":is_profi(hisprofile, 'Manager'),
        "is_director":is_profi(hisprofile, 'Director'),
        'hint':hisprofile.skill.hint_numbers[1],
    }
    return render(request, "profile/change_profile.html", context)

def confirm_email(request):
    if request.GET.get('confirm'):
        profile = Profile.objects.get(user = request.user)
        skill = profile.skill
        if skill.confirmation_code == request.GET.get('confirm'):
            skill.confirmed = True
            print('yoyoyo')
            skill.save()
    return redirect(profile.get_absolute_url())

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse

def subject_attendance(request):
    if request.GET.get('subject_id'):
        profile = Profile.objects.get(user = request.user)
        cache_att = CacheAttendance.objects.get_or_create(profile=profile)[0]
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')))
        school = subject.school
        is_in_school(profile, school)
        cache_att.subject = subject
        if not cache_att.squad in subject.squads.all():
            if is_profi(profile, "Teacher"):
                cache_att.squad = subject.squads.first()
            else:
                for hissquad in profile.squads.all():
                    if hissquad in subject.squads.all():
                        cache_att.squad = hissquad
                        break
        cache_att.save()
    data = {
    }
    return JsonResponse(data)
def squad_attendance(request):
    if request.GET.get('squad_id'):
        profile = Profile.objects.get(user = request.user)
        cache_att = CacheAttendance.objects.get(profile=profile)
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')))
        school = squad.school
        is_in_school(profile, school)
        cache_att.squad = squad
        cache_att.save()
    data = {
    }
    return JsonResponse(data)

def more_attendance(request):
    profile = Profile.objects.get(user = request.user)
    if request.GET.get('subject_id') and request.GET.get('squad_id') and request.GET.get('direction') and request.GET.get('sm_id'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')))
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')))
        school = subject.school
        is_in_school(profile, school)
        current_sm = int(request.GET.get('sm_id'))
        columns = []
        last_set = False
        first_set = False
        stopleft = False
        stopright = False
        if request.GET.get('direction') == 'left':
            queryset = subject.materials.filter(id__lt = current_sm).order_by('-id')
            if len(queryset) <= 4:
                first_set = True
                if len(queryset) == 0:
                    stopleft = True
            for sm in queryset:
                if len(columns) == 4:
                    break
                if len(sm.sm_atts.filter(squad = squad)) < len(squad.students.all()):
                    create_atts(squad, sm, subject)
                get_date_results = get_date(sm, squad)
                if get_date_results == '_':
                    section = ['_', sm.id, '_']
                else:
                    section = [get_date_results[0].strftime('%d %B %Y'), sm.id, get_date_results[1]]
                for att in sm.sm_atts.filter(squad = squad):
                    section.append([att.id, att.present, att.grade])
                columns.append(section)
        else:
            queryset = subject.materials.filter(id__gt = current_sm)
            if len(queryset) <= 4:
                last_set = True
                if len(queryset) == 0:
                    stopright = True                
            for sm in queryset:
                if len(columns) == 4:
                    break
                section = [get_date(sm, squad)[0].strftime('%d %B %Y'), sm.id]
                columns.append(section)
        data = {
            'first_set':first_set,
            'last_set':last_set,
            'columns':columns,
            'stopleft':stopleft,
            'stopright':stopright,
        }
        return JsonResponse(data)

def more_attendance_student(request):
    profile = get_profile(request)
    if request.GET.get('subject_id') and request.GET.get('squad_id') and request.GET.get('direction') and request.GET.get('sm_id'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')))
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')))
        school = subject.school
        is_in_school(profile, school)
        current_sm = int(request.GET.get('sm_id'))
        columns = []
        last_set = False
        first_set = False
        if request.GET.get('direction') == 'left':
            queryset = subject.materials.filter(id__lt = current_sm).order_by('-id')
            if len(queryset) <= 4:
                first_set = True
            for sm in queryset:
                if len(columns) == 4:
                    break
                if len(sm.sm_atts.filter(student = profile)) < 1:
                    create_atts_student(sm, profile)
                section = [get_date(sm, squad)[0], sm.id, 'past']
                att = sm.sm_atts.get(student = profile)
                section.append([att.id, att.present, att.grade])
                columns.append(section)
        else:
            queryset = subject.materials.filter(id__gt = current_sm)
            if len(queryset) <= 4:
                last_set = True
            for sm in queryset:
                if len(columns) == 4:
                    break
                section = [get_date(sm, squad)[0], sm.id]
                columns.append(section)
        data = {
            'first_set':first_set,
            'last_set':last_set,
            'columns':columns,
        }
        return JsonResponse(data)

def miss_lecture(request):
    profile = Profile.objects.get(user = request.user)
    if request.GET.get('date'):
        miss_lesson = MissLesson.objects.filter(profile = profile)
        if len(miss_lesson) > 0:
            miss_lesson = miss_lesson[0]
        else:
            print('new miss')
            miss_lesson = MissLesson.objects.create(profile=profile)
        date = datetime.datetime.strptime(request.GET.get('date'), "%Y-%m-%d").date()
        if date in miss_lesson.dates:
            action = 'remove'
            miss_lesson.dates.remove(date)
        else:
            action = 'add'
            miss_lesson.dates.append(date)
        miss_lesson.save()

    data = {
        'action':action
    }
    return JsonResponse(data)

def att_present(request):
    profile = Profile.objects.get(user = request.user)
    if request.GET.get('id') and is_profi(profile, 'Teacher'):
        attendance = Attendance.objects.get(id = request.GET.get('id'))
        school = attendance.school
        is_in_school(profile, school)        
        attendance.present = 'present'
        if len(CRMCard.objects.filter(card_user=attendance.student)) > 0:
            if attendance.student.card.column.id == 2:
                attendance.student.card.column = CRMColumn.objects.get(id=3)
                attendance.student.card.save()
        else:
            CRMCard.objects.create(
                card_user=attendance.student,
                column=CRMColumn.objects.get(id=1),
                name=attendance.student.first_name,
                phone=attendance.student.phone,
                mail=attendance.student.mail,
                saved=True
            )   
        material = attendance.subject_materials
        if not profile in material.done_by.all():
            material.done_by.add(profile)
            profile.money += profile.salary
            school = attendance.subject.school
            school.money -= profile.salary
            school.save()
            for student in attendance.squad.students.all():
                was_minus = False
                if student.money < student.salary:
                    was_minus = True
                student.money -= attendance.subject.cost
                student.save()
                if student.money < student.salary and was_minus == False and student.card.was_called == True:
                    skill = student.card.author_profile.skill
                    skill.need_actions += 1
                    skill.save()
        attendance.save()
        profile.save()
    data = {
    }
    return JsonResponse(data)

def ChangeAttendance(request):
    profile = Profile.objects.get(user = request.user)
    if request.GET.get('id'):
        attendance = Attendance.objects.get(id = int(request.GET.get('id')))
        school = attendance.school
        is_in_school(profile, school)        
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

def another_hint(request):
    profile = Profile.objects.get(user = request.user)
    hint_type = int(request.GET.get('hint_type'))
    if request.GET.get('dir') == 'next':
        profile.skill.hint_numbers[hint_type] += 1
    elif request.GET.get('dir') == 'prev':
        profile.skill.hint_numbers[hint_type] -= 1
    else:
        profile.skill.hint_numbers[hint_type] = 100
    profile.skill.save()
    data = {
    }
    return JsonResponse(data)

def update_hints(request):
    profile = Profile.objects.get(user = request.user)
    if profile.is_student:
        profile.skill.hint_numbers = [0,0,0,0,0,0,0]        
    if is_profi(profile, 'Manager'):
        profile.skill.hint_numbers = [20,20,20,20,20,20,20]        
    if is_profi(profile, 'Teacher'):
        profile.skill.hint_numbers = [40,40,40,40,40,40,40]
    if is_profi(profile, 'Director'):
        profile.skill.hint_numbers = [60,60,60,60,60,60,60]

    profile.skill.save()
    data = {
    }
    return JsonResponse(data)

def logout_view(request):
    logout(request)
    return redirect("/")

def test_account(request):
    user = User.objects.get(id = 1)
    hisprofile = Profile.objects.get(user = user)
    if is_profi(hisprofile, 'Teacher'):
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

def make_payment(request):
    manager = Profile.objects.get(user = request.user)
    only_managers(manager)
    amount = int(request.GET.get('amount'))
    if amount > 0 and request.GET.get('id'):
        profile = Profile.objects.get(id = int(request.GET.get('id')))
        school = manager.schools.first()
        is_in_school(profile, school)        
        profile.money += amount
        profile.payment_history.create(
            manager = manager,
            amount = amount,
        )
        school.money += amount
        school.save()
        if profile.money > profile.salary:
            if profile.card:
                card = profile.card            
            else:
                card = CRMCard.objects.create(
                    author_profile=manager,
                    card_user = profile,
                    school = school,
                    column = CRMColumn.objects.get(id = 5),
                    name = profile.first_name,
                    phone = profile.phone,
                    mail = profile.mail,
                    saved = True,
                    was_called = True
                )[0]
            card.was_called = True
        profile.save()
    data = {
    }
    return JsonResponse(data)
