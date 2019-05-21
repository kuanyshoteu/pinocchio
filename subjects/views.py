from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import RedirectView

from .forms import SubjectForm,SubjectForm2
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
    if profile.is_student:
        profile.squads

    context = {
        "instance": instance,
        "profile":profile,
        'time_periods':time_periods,
        'days':days,
        'materials':instance.materials.prefetch_related('lessons'),
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
    if profile.crm_subject:
        subjects = profile.crm_subject.category_subjects.all()
    else:
        subjects = school.school_subjects.all()
    context = {
        "profile": profile,
        "subjects":subjects,
        "subject_categories":school.school_subject_categories.all(),
        "school":school,
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
    school = profile.schools.first()    
    if form.is_valid():
        instance = form.save(commit=False)
        instance.school = school
        instance.save()
        return HttpResponseRedirect(instance.get_update_url())

    context = {
        "form": form,
        "profile":profile,
        "all_teachers":all_teachers(school),
        "subject_categories":school.school_subject_categories.all(),        
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

    form2 = SubjectForm2(request.POST or None, request.FILES or None, instance=instance)
    if form2.is_valid():
        instance = form2.save(commit=False)
        if not instance.height_field:
            instance.height_field = 0
        if not instance.width_field:
            instance.width_field = 0
        for squad in instance.squads.all():
            update_squad_dates(instance, squad)
        instance.save()
        return HttpResponseRedirect(instance.get_update_url())

    school = profile.schools.first()
    time_periods = school.time_periods.all()
    days = Day.objects.all()
    cells = school.school_cells.all()
    if len(cells) < len(days) * len(time_periods):
        for day in days:
            for timep in time_periods:
                new_cell = Cell.objects.get_or_create(day = day, time_period = timep)

    context = {
        "instance": instance,
        "form":form,
        "form2":form2,
        'page':'subject_update',
        "profile":profile,
        'squads':Squad.objects.all(),
        "subject_categories":school.school_subject_categories.all(),        
        "subject_ages":school.school_subject_ages.all(),        
        'time_periods':time_periods,
        'days':days,
        "all_teachers":all_teachers(school),
        'is_trener':is_profi(profile, 'Teacher'),
        "is_manager":is_profi(profile, 'Manager'),
        "is_director":is_profi(profile, 'Director'),
    }
    return render(request, "subjects/subject_create.html", context)
from datetime import timedelta
def update_squad_dates(subject, squad):
    if not squad.id in subject.squad_ids:
        subject.squad_ids.append(squad.id)
        subject.start_dates.append(timezone.now().date())
    squad_index = subject.squad_ids.index(squad.id)
    lectures = squad.squad_lectures.filter(subject = subject)
    found = False
    start = int(squad.start_date.strftime('%w'))
    if start == 0:
        start = 7
    for lecture in lectures:
        if lecture.day.number >= start:
            subject.start_dates[squad_index] = squad.start_date + timedelta(lecture.day.number - start)
            found = True
            break
    if found == False and len(lectures) > 0:
        subject.start_dates[squad_index] = squad.start_date + timedelta(7 + lectures[0].day.number - start)
    
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
    school = profile.schools.first()
    subject = Subject.objects.get(id = id)
    res = []
    for timep in school.time_periods.all():
        line = []
        for cell in timep.time_cell.all():
            if cell.day.number != 7:
                lectures = []
                for lecture in cell.lectures.filter(subject = subject):
                    if lecture.squad in subject.squads.all():
                        cabinet=''
                        if lecture.cabinet:
                            cabinet = lecture.cabinet.title
                        lectures.append([lecture.id, lecture.squad.title, lecture.squad.id, cabinet])
                line.append([cell.id, lectures])
        res.append([timep.start + '-' + timep.end, line])

    data = {
        'calendar':res
    }
    return JsonResponse(data)

def squad_list(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    school = profile.schools.first()
    subject = Subject.objects.get(id = id)
    res = []
    res2 = []
    for squad in school.groups.all():
        if not squad in subject.squads.all():
            res.append([squad.id, [squad.title]])
        else:
            res2.append([squad.id, [squad.title]])
    data = {
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
        squad_students = squad.students.all()
        cell = Cell.objects.get(id = int(request.GET.get('cell_id')))
        if request.GET.get('old_cell') == 'none':
            if len(Lecture.objects.filter(subject=subject,squad=squad,cell=cell)) == 0:
                lecture = Lecture.objects.create(
                    subject=subject,
                    squad=squad,
                    cell=cell, 
                    day=cell.day,
                    office=subject.office,
                    category=subject.category,
                    age=subject.age)
                lecture.people.add(*squad_students)
                if squad.teacher:
                    lecture.people.add(squad.teacher)
        else:
            old_cell = Cell.objects.get(id = int(request.GET.get('old_cell')))
            lecture = Lecture.objects.get(subject=subject,squad=squad,cell=old_cell)
            if len(Lecture.objects.filter(subject=subject,squad=squad,cell=cell)) == 0:
                lecture.cell = cell
                lecture.day = cell.day
                lecture.save()
            else:
                lecture.delete()
        subject.save()

    data = {
    }
    return JsonResponse(data)

def add_squad(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('squad_id') and request.GET.get('subject_id'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')) )
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')) )
        subject.squads.add(squad)
        squad_students = squad.students.all()
        subject.students.add(*squad_students)
        subject.teachers.add(squad.teacher)
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
        squad_students = squad.students.all()
        subject.students.remove(*squad_students)
        subject.teachers.remove(squad.teacher)
    data = {
    }
    return JsonResponse(data)

def change_teacher(request):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('teacher_id') and request.GET.get('subject_id'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')) )
        teacher = Profile.objects.get(id = int(request.GET.get('teacher_id')) )
        subject.author = teacher
        subject.save()
    data = {
    }
    return JsonResponse(data)

def change_category(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('object_id'):
        subject = Subject.objects.select_related('category').get(id = id)
        students = subject.students.all()
        if subject.category:
            subject.category.students.remove(*students)
        if int(request.GET.get('object_id')) == -1:
            subject.category = None
        else:
            category = SubjectCategory.objects.get(id = int(request.GET.get('object_id')))
            subject.category = category
            category.students.add(*students)
        subject.save()
    data = {
    }
    return JsonResponse(data)
        
def change_age(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('object_id'):
        subject = Subject.objects.select_related('age').get(id = id)
        students = subject.students.all()
        if subject.age:
            subject.age.students.remove(*students)
        if int(request.GET.get('object_id')) == -1:
            subject.age = None
        else:
            age = SubjectAge.objects.get(id = int(request.GET.get('object_id')))
            subject.age = age
            age.students.add(*students)
        subject.save()
    data = {
    }
    return JsonResponse(data)
        
def delete_lesson(request, id=None):
    profile = get_profile(request)
    only_managers(profile)
    if request.GET.get('lecture_id'):
        subject = Subject.objects.get(id = id)
        lecture = subject.subject_lectures.get(id=int(request.GET.get('lecture_id')))
        lecture.delete()
    data = {
    }
    return JsonResponse(data)
        
