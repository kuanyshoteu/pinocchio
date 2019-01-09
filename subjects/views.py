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
from accounts.models import Profile, MainPage
from accounts.forms import *
from squads.views import update_actual_week
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.contrib.auth.models import User

def subject_detail(request, slug=None):
    instance = get_object_or_404(Subject, slug=slug)
   
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)

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
        'folders':Folder.objects.all(),
        'lessons':Lesson.objects.all(),
        'time_periods':time_periods,
        'days':days,
        'videos':get_videos(instance)[0],
        'youtubes':get_videos(instance)[1],
    }
    return render(request, "subjects/subject_detail.html", context)

def subject_list(request):
    if not request.user.is_authenticated:
        raise Http404
        
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    
    context = {
        "profile": profile,
        "subjects":Subject.objects.all(),
        "subject_categories":SubjectCategory.objects.all(),
    }
    return render(request, "subjects/subject_list.html", context)

def subject_videos(request, slug=None):
    instance = get_object_or_404(Subject, slug=slug)
    context = {
        "instance": instance,
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
    main_page = 'de'
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    if len(MainPage.objects.all()) < 1:
        main_page = MainPage.objects.create()
    else:
        main_page = MainPage.objects.all()[0]
    context = {
        "user":request.user,
        "profile":profile,
        "instance": instance,
        "main_page":main_page,
    }
    return render(request, "subjects/subject_lessons.html", context)

def subject_create(request):
    if not request.user.is_authenticated:
        raise Http404

    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    if not profile.is_trener:
        raise Http404
        
    form = SubjectForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_update_url())

    context = {
        "form": form,
        "profile":profile,
        "all_teachers":Profile.objects.filter(is_trener = True),
    }
    return render(request, "subjects/subject_create.html", context)

def subject_update(request, slug=None):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Subject, slug=slug)
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
        
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)

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
    }
    return render(request, "subjects/subject_create.html", context)

def all_teachers():
    return Profile.objects.filter(is_trener = True)

def subject_delete(request, slug=None):
    if not request.user.is_authenticated:
        raise Http404
    try:
        instance = Subject.objects.get(slug=slug)
    except:
        raise Http404

    if not request.user.is_staff and not request.user.is_superuser:
        reponse.status_code = 403
        return HttpResponse("You do not have permission to do this.")
        
    if request.method == "POST":
        instance.delete()
        messages.success(request, "Successfully deleted")
        return redirect("subjects:list")
    context = {
        "object": instance
    }
    return render(request, "confirm_delete.html", context)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse

class ChangeTimeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, format=None):
        data = {
            "like_num":0,
        }
        return Response(data)

class SubjectRegAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Subject, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        profile = Profile.objects.get(user = user)
        reg = False
        if user.is_authenticated:
            if profile in obj.followers.all():
                reg = False
                obj.followers.remove(profile)
            else:
                reg = True
                obj.followers.add(profile)
            profile.save()    
            new_follow = Follow.objects.create(
                    author_profile=profile,
                    group=obj,
                )
            new_follow.save()
        fol_num = int(obj.followers.count())
        obj.followers_number = obj.followers.count()
        obj.save()
        data = {
            "reg": reg,
            "fol_num":fol_num,
        }
        return Response(data)


def add_paper(request):
    if request.GET.get('day_id') and request.GET.get('paper_id'):
        lesson = Lesson.objects.get(id = int(request.GET.get('paper_id')))
        subject_materials = SubjectMaterials.objects.get(id=int(request.GET.get('day_id')))
        subject_materials.lessons.add(lesson)
    data = {
        'href':lesson.get_absolute_url()
    }
    return JsonResponse(data)

def subject_schedule(request, id=None):
    subject = Subject.objects.get(id = id)
    res = []
    for timep in TimePeriod.objects.all():
        line = []
        for cell in timep.time_cell.all():
            if cell.day.number != 7:
                lectures = []
                for lecture in cell.lectures.filter(subject = subject):
                    if lecture.squad in subject.squads.all():
                        print(timep.start, cell.id,lecture.squad.title)
                        lectures.append(lecture.squad.title)
                line.append([cell.id, lectures])
        res.append([timep.start + '-' + timep.end, line])

    data = {
        'calendar':res
    }
    return JsonResponse(data)

def squad_list(request, id=None):
    subject = Subject.objects.get(id = id)
    res = []
    res2 = []
    for squad in Squad.objects.all():
        if not squad in subject.squads.all():
            res.append([squad.id, [squad.title]])
        else:
            res2.append([squad.id, [squad.title]])
    data = {
        'trener':subject.teacher.all()[0].first_name,
        'groups_in_subject':res2,
        'groups_not_in_subject':res,
    }
    return JsonResponse(data)

def change_schedule(request, id=None):
    subject = Subject.objects.get(id = id)
    if request.GET.get('squad_id') and request.GET.get('cell_id') and request.GET.get('old_cell'):
        squad = Squad.objects.get(id = int(request.GET.get('squad_id')) )
        if request.GET.get('cell_id') != 'trash':
            cell = Cell.objects.get(id = int(request.GET.get('cell_id')))
            if request.GET.get('old_cell') == 'none':
                lecture = Lecture.objects.get_or_create(subject=subject,squad=squad,cell=cell)
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
    for squad in subject.squads.all():
        cnt = number_of_weeks * len(Lecture.objects.filter(subject=subject,squad=squad))
        extra = 0
        finish = int(subject.end_date.strftime('%w'))
        if finish == 0:
            finish = 7
        start = int(subject.start_date.strftime('%w'))
        if start == 0:
            start = 7 
        for i in range(start, finish + 1):
            cnt_cell = Cell.objects.filter(day=Day.objects.get(id=int(i)))
            for cell in cnt_cell:
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

    for squad in subject.squads.all():
        if squad.start_date > subject.start_date:
            squad.start_date = subject.start_date
            squad.save()
            update_squad_weeks(squad)
        if squad.end_date < subject.end_date:
            squad.end_date = subject.end_date
            squad.save()
            update_squad_weeks(squad)
        if len(squad.weeks.filter(actual = True)) == 0:
            update_actual_week(squad)
        
    sc_dict = {}
    sm_dict = {}
    for squad in subject.squads.all():
        cells = []
        for lecture in Lecture.objects.filter(squad=squad,subject=subject):
            if not lecture.cell in cells:
                cells.append(lecture.cell)
        old_sc = SquadCell.objects.filter(squad=squad)[0]
        sm_dict[squad.id] = old_sc
        for sc in SquadCell.objects.filter(squad=squad):
            for m in sc.subject_materials.filter(subject=subject):
                sc.subject_materials.remove(m)
            if sc.cell in cells and sc.date >= subject.start_date and sc.date <= subject.end_date:
                sc_dict[old_sc.id] = sc.id
                sc_dict[sc.id] = -1
                old_sc = sc
    
    for sm in subject.materials.all():
        stud_num = 0
        for squad in subject.squads.all():
            if sm_dict[squad.id] != 'ended':
                sc = sm_dict[squad.id]
                if len(Lecture.objects.filter(cell = sc.cell,subject=subject,squad=squad)) > 0:
                    if sc.date >= subject.start_date and sc.date <= subject.end_date:
                        sc.subject_materials.add(sm)
                if sc_dict[sc.id] > 0:
                    next_sc = SquadCell.objects.filter(id=sc_dict[sc.id])
                    sm_dict[squad.id] = next_sc[0]
                else:
                    sm_dict[squad.id] = 'ended'

            stud_num += len(squad.students.all())
    for sm in subject.materials.all():
        for squad in subject.squads.all():
            for student in squad.students.all():
                sc = sm.material_cells.filter(squad=squad)
                if len(sc)>0:
                    att = Attendance.objects.get_or_create(student=student,subject=subject,squad_cell=sc[0])   
                    att[0].squad = squad
                    att[0].subject_materials = sm
                    att[0].save()

def update_squad_weeks(instance):
    if int((instance.end_date - instance.start_date).days) > 0:
        new_weeks = True
        number_of_weeks = int((instance.end_date - instance.start_date).days/7) + 1
        if len(instance.weeks.all()) > number_of_weeks:
            for i in range(number_of_weeks, len(instance.weeks.all())):
                instance.weeks.all()[i].delete()
        if len(instance.weeks.all()) < number_of_weeks:
            new_weeks = True
            for i in range(len(instance.weeks.all()), number_of_weeks):
                SquadWeek.objects.create(squad=instance)

        for squad_week in instance.weeks.all():
            if len(squad_week.week_cells.all()) > len(TimePeriod.objects.all())*7:  
                squad_week.week_cells.all().delete()

        if new_weeks or len(instance.cells.all()) < len(instance.weeks.all()) * len(TimePeriod.objects.all())*7:
            date = instance.start_date - timedelta(1)
            week = instance.weeks.all()[0]
            before_start = int(instance.start_date.strftime('%w'))
            for i in range(1, before_start + 1):
                for timep in TimePeriod.objects.all():
                    sc = SquadCell.objects.get_or_create(squad=instance,date=date,time_period=timep)[0]
                    sc.week = week
                    sc.save()
                date = instance.start_date - timedelta(i)
            date = instance.start_date
            for i in range(1, (instance.end_date - instance.start_date).days + 2):
                week_num = int((date - instance.start_date + timedelta(before_start)).days/7)
                if week_num == len(instance.weeks.all()):
                    break
                week = instance.weeks.all()[week_num]
                for timep in TimePeriod.objects.all():
                    number = int(date.strftime('%w'))
                    if number == 0:
                        number = 7
                    sc = SquadCell.objects.get_or_create(squad=instance,date=date,time_period=timep)[0]
                    sc.cell = Cell.objects.get(time_period = timep,day = Day.objects.get(number=number))
                    sc.week = week
                    sc.save()
                date = instance.start_date + timedelta(i)

def add_squad(request):
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
    if request.GET.get('date') and request.GET.get('subject_id'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')) )
        subject.start_date = datetime.datetime.strptime(request.GET.get('date'), "%Y-%m-%d").date()
        subject.save()
    data = {
    }
    return JsonResponse(data)


def change_end(request):
    if request.GET.get('date') and request.GET.get('subject_id'):
        subject = Subject.objects.get(id = int(request.GET.get('subject_id')) )
        subject.end_date = datetime.datetime.strptime(request.GET.get('date'), "%Y-%m-%d").date()
        subject.save()
    data = {
    }
    return JsonResponse(data)
    