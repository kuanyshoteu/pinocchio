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
import datetime

from .forms import SubjectForm
from .models import *
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
from constants import *

def subject_detail(request, slug=None):
    instance = get_object_or_404(Subject, slug=slug)   
    profile = get_profile(request)
    time_periods = TimePeriod.objects.all()
    days = Day.objects.all()
    cells = Cell.objects.all()
    if len(cells) < len(days) * len(time_periods):
        for day in days:
            for timep in time_periods:
                new_cell = Cell.objects.get_or_create(day = day, time_period = timep)

    context = {
        "instance": instance,
        "profile":profile,
        'time_periods':time_periods,
        'days':days,
        "teacher":is_profi(profile, 'Teacher'),
        "lessons":profile.lesson_author.all(),
        "folders":profile.folders.all(), 
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),       
    }
    return render(request, "subjects/subject_detail.html", context)

def subject_list(request):
    profile = get_profile(request)
    only_staff(profile)
    school = profile.schools.first()
    context = {
        "profile": profile,
        "subjects":school.school_subjects.all(),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
    }
    return render(request, "subjects/subject_list.html", context)

def subject_videos(request, slug=None):
    instance = get_object_or_404(Subject, slug=slug)
    context = {
        "instance": instance,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
    }
    return render(request, "subjects/subject_videos.html", context)

def get_videos(instance):
    found = False
    youtubes = []
    videos = []
    cnt = 0
    for sm in instance.materials.all():
        if found:
            break
        for lesson in sm.lessons.all():
            if found:
                break
            for paper in lesson.papers.all():
                if found:
                    break
                for subtheme in paper.subthemes.all():
                    if cnt >= 2:
                        found = True
                        break
                    if subtheme.video:
                        videos.append(subtheme.video)
                        cnt += 1
                    if subtheme.youtube_video_link:
                        youtubes.append(subtheme.youtube_video_link)
                        cnt += 1

    return videos, youtubes
def subject_lessons(request, slug=None):
    instance = get_object_or_404(Subject, slug=slug)
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    context = {
        "user":request.user,
        "profile":profile,
        "instance": instance,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
    }
    return render(request, "subjects/subject_lessons.html", context)

def subject_create(request):
    profile = get_profile(request)
    only_managers(profile)
    form = SubjectForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_update_url())

    context = {
        "form": form,
        "profile":profile,
        "all_teachers":all_teachers(),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
    }
    return render(request, "subjects/subject_create.html", context)

def subject_update(request, slug=None):
    instance = get_object_or_404(Subject, slug=slug)
    profile = get_profile(request)
    only_managers(profile)
    form = SubjectForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if not instance.height_field:
            instance.height_field = 0
        if not instance.width_field:
            instance.width_field = 0
        instance.save()
        subject = Subject.objects.get(slug=slug)
        calc_subject_lessons(subject)
        return HttpResponseRedirect(instance.get_update_url())

    time_periods = TimePeriod.objects.all()
    days = Day.objects.all()
    cells = Cell.objects.all()
    if len(cells) < len(days) * len(time_periods):
        for day in days:
            for timep in time_periods:
                new_cell = Cell.objects.get_or_create(day = day, time_period = timep)

    context = {
        "instance": instance,
        "form":form,
        'page':'subject_update',
        "profile":profile,
        'squads':Squad.objects.all(),
        'time_periods':time_periods,
        'days':days,
        "all_teachers":all_teachers(),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
    }
    return render(request, "subjects/subject_create.html", context)

def all_teachers():
    return Profile.objects.filter()

def subject_delete(request, slug=None):
    instance = Subject.objects.get(slug=slug)
    profile = get_profile(request)
    only_managers(profile)
    if request.method == "POST":
        instance.delete()
        messages.success(request, "Successfully deleted")
        return redirect("subjects:list")
    context = {
        "object": instance,
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
    }
    return render(request, "confirm_delete.html", context)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse

def add_paper(request):
    profile = get_profile(request)
    only_teachers(profile)
    if request.GET.get('day_id') and request.GET.get('paper_id'):
        lesson = Lesson.objects.get(id = int(request.GET.get('paper_id')))
        subject_materials = SubjectMaterials.objects.get(id=int(request.GET.get('day_id')))
        subject_materials.lessons.add(lesson)
    data = {
        'href':lesson.get_absolute_url()
    }
    return JsonResponse(data)
    
def remove_lesson(request):
    profile = get_profile(request)
    only_teachers(profile)
    if request.GET.get('material_id') and request.GET.get('lesson_id'):
        material = SubjectMaterials.objects.get(id=int(request.GET.get('material_id')))
        lesson = Lesson.objects.get(id=int(request.GET.get('lesson_id')))
        material.lessons.remove(lesson)
        print('ok')
    data = {
    }
    return JsonResponse(data)

def subject_schedule(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    subject = Subject.objects.get(id = id)
    res = []
    for timep in TimePeriod.objects.all():
        line = []
        for cell in timep.time_cell.all():
            if cell.day.number != 7:
                lectures = []
                for lecture in cell.lectures.filter(subject = subject):
                    if lecture.squad in subject.squads.all():
                        lectures.append(lecture.squad.title)
                line.append([cell.id, lectures])
        res.append([timep.start + '-' + timep.end, line])

    data = {
        'calendar':res
    }
    return JsonResponse(data)

def squad_list(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    subject = Subject.objects.get(id = id)
    res = []
    res2 = []
    for squad in Squad.objects.all():
        if not squad in subject.squads.all():
            res.append([squad.id, [squad.title]])
        else:
            res2.append([squad.id, [squad.title]])
    if len(subject.teacher.all()) > 0:
        trener = subject.teacher.first().first_name
    else:
        trener = 'none'
    data = {
        'trener': trener,
        'groups_in_subject':res2,
        'groups_not_in_subject':res,
    }
    return JsonResponse(data)

def change_schedule(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    subject = Subject.objects.get(id = id)
    school = subject.school
    school.new_schedule = True
    school.save()

    if request.GET.get('squad_id') and request.GET.get('cell_id') and request.GET.get('old_cell'):
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')) )
        if request.GET.get('cell_id') != 'trash':
            cell = Cell.objects.get(id = int(request.GET.get('cell_id')))
            if request.GET.get('old_cell') == 'none':
                lecture = Lecture.objects.get_or_create(subject=subject,squad=squad,cell=cell, day=cell.day)[0]
                squad_students = squad.students.all()
                lecture.people.add(*squad_students)
                subject_teacher = subject.teacher.all()
                lecture.people.add(*squad_students)
                lecture.people.add(*subject_teacher)
                print(lecture.id)
            else:
                old_cell = Cell.objects.get(id = int(request.GET.get('old_cell')))
                lecture = Lecture.objects.get(subject=subject,squad=squad,cell=old_cell)
                if len(Lecture.objects.filter(subject=subject,squad=squad,cell=cell)) == 0:
                    lecture.cell = cell
                    lecture.save()
                else:
                    lecture.delete()
        else:
            if request.GET.get('old_cell') != 'none':
                old_cell = Cell.objects.get(id = int(request.GET.get('old_cell')))
                lecture = Lecture.objects.get(subject=subject,squad=squad,cell=old_cell)
                lecture.delete()
        subject.save()

    data = {
    }
    return JsonResponse(data)

def calc_subject_lessons(subject):
    res = 0
    number_of_weeks = int((subject.end_date - subject.start_date).days/7)
    finish = int(subject.end_date.strftime('%w'))
    start = int(subject.start_date.strftime('%w'))
    if start == 0:
        start = 7
    if start > finish or finish == 0:
        finish += 7 
    for squad in subject.squads.all():
        if not squad.id in subject.squad_ids:
            subject.squad_ids.append(squad.id)
            subject.start_dates.append(timezone.now().date())
        squad_index = subject.squad_ids.index(squad.id)
        lectures = squad.squad_lectures.filter(subject = subject)
        found = False
        for lecture in lectures:
            if lecture.day.number >= start:
                subject.start_dates[squad_index] = subject.start_date + timedelta(lecture.day.number - start)
                found = True
                break
        if found == False and len(lectures) > 0:
            subject.start_dates[squad_index] = subject.start_date + timedelta(7 + lectures[0].day.number - start)

        cnt = number_of_weeks * len(lectures)
        extra = 0
        for i in range(start, finish + 1): # Days of week of last not full week
            i = i % 7
            if i == 0:
                i = 7
            cnt_cell = Cell.objects.filter(day=Day.objects.get(number=int(i)))
            for cell in cnt_cell: # Check if there are lectures in this days
                if len(Lecture.objects.filter(subject=subject, squad=squad, cell=cell)) > 0:
                    extra += 1
        cnt += extra
        if res < cnt:
            res = cnt
    subject.number_of_lectures = res
    subject.save()

    if len(subject.materials.all()) < subject.number_of_lectures:
        for i in range(len(subject.materials.all())+1, res+1):
            SubjectMaterials.objects.create(subject=subject, number=i)
    if len(subject.materials.all()) > subject.number_of_lectures:
        for i in range(subject.number_of_lectures, len(subject.materials.all())):
            if i >= len(subject.materials.all()):
                break
            subject.materials.all()[i].delete()

def add_squad(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('squad_id') and request.GET.get('subject_id'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')) )
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')) )
        subject.squads.add(squad)
        for student in squad.students.all():
            subject.students.add(student)
    data = {
    }
    return JsonResponse(data)

def delete_squad(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('squad_id') and request.GET.get('subject_id'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')) )
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')) )
        subject.squads.remove(squad)
        for student in squad.students.all():
            subject.students.remove(student)
    data = {
    }
    return JsonResponse(data)

def change_teacher(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('teacher_id') and request.GET.get('subject_id'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')) )
        teacher = Profile.objects.get(id = int(request.GET.get('teacher_id')) )
        for oldteacher in subject.teacher.all():
            subject.teacher.remove(oldteacher)
        subject.teacher.add(teacher)
    data = {
    }
    return JsonResponse(data)

def change_start(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('date') and request.GET.get('subject_id'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')) )
        subject.start_date = datetime.datetime.strptime(request.GET.get('date'), "%Y-%m-%d").date()
        subject.save()
    data = {
    }
    return JsonResponse(data)

def change_end(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('date') and request.GET.get('subject_id'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')) )
        subject.end_date = datetime.datetime.strptime(request.GET.get('date'), "%Y-%m-%d").date()
        subject.save()
    data = {
    }
    return JsonResponse(data)
    