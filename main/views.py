from django.shortcuts import render, redirect
from accounts.models import *
from .models import *
from accounts.forms import *
from squads.models import Squad
from subjects.models import *

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from itertools import chain
from django.views.generic import ListView

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )
from django.contrib.auth.models import User
def loaderio(request):
    context = {
    }
    return render(request, "loaderio.txt", context)

def main_view(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
        return redirect(profile.get_absolute_url())    

    form = EmptyForm(request.POST or None)
    if form.is_valid():
        if request.POST.get('username') and request.POST.get('password'):
            for profile in Profile.objects.all():
                if profile.mail == request.POST.get('username') or profile.phone == request.POST.get('username'):
                    user = authenticate(username=str(profile.user.username), password=str(request.POST.get('password')))
                    if user:
                        login(request, user)
                        return HttpResponseRedirect(profile.get_absolute_url())

    context = {
        'main':True,
        'form':form,
    }
    return render(request, "main.html", context)

def hislessons(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    else:
        raise Http404

    res = []
    lesson_now = False
    classwork = []
    if profile.is_trener:
        hissubjects = profile.teachers_subjects.all()
    else:
        hissubjects = profile.hissubjects.all()
    for subject in hissubjects:
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

    context = {
        "profile":profile,
        'classwork':classwork,
        'homeworks':res,
        'lesson_now':lesson_now,
    }
    return render(request, "profile/classwork.html", context)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import JsonResponse

def login_view(request):
    if request.GET.get('username') and request.GET.get('password'):
        for profile in Profile.objects.all():
            if profile.mail == request.GET.get('username') or profile.phone == request.GET.get('username'):
                print(request.GET.get('password'),profile.user.username)
                user = authenticate(username=str(profile.user.username), password=str(request.GET.get('password')))
                login(request, user)
                break
    data = {
    }
    return JsonResponse(data)

def register_view(request):
    if request.GET.get('first_name') and request.GET.get('second_name') and request.GET.get('school') and request.GET.get('phone') and request.GET.get('mail') and request.GET.get('password1') and request.GET.get('password2'):
        if request.GET.get('password1') == request.GET.get('password2'):
            new_id = User.objects.order_by("id").last().id + 1
            user = User.objects.create(username='user' + str(new_id), password=request.GET.get('password1'))
            new_user = authenticate(username = user.username, password=request.GET.get('password1'))
            login(request, user)
            profile = Profile.objects.get(user = user)
            profile.first_name = request.GET.get('first_name')
            profile.second_name = request.GET.get('second_name')
            profile.school = request.GET.get('school')
            profile.phone = request.GET.get('phone')
            profile.mail = request.GET.get('mail')
            profile.save()
    data = {
    }
    return JsonResponse(data)

def ChangeSubject(request):
    if request.GET.get('id'):
        subject = Subject.objects.get(id = int(request.GET.get('id')))
        if request.GET.get('text'):
            subject.text = request.GET.get('text')
        if request.GET.get('title'):
            subject.title = request.GET.get('title')
        if request.GET.get('cost'):
            subject.cost = request.GET.get('cost')
        subject.save()
                    
    data = {
        "like_num":0,
    }
    return JsonResponse(data)

def SaveZaiavka(request):
    if request.GET.get('name'):
        if request.GET.get('phone'):
            zaiavka = Zaiavka.objects.create(name=request.GET.get('name'), phone=request.GET.get('phone'))
    data = {
    }
    return JsonResponse(data)


class CityAPIToggle(APIView):
    def get(self, request, format=None):
        #print("dedede")
        data = {
            "like_num":0,
        }
        return Response(data)

class FilialAPIToggle(APIView):
    def get(self, request, format=None):
        data = {
            "like_num":0,
        }
        return Response(data)

class SubjectAPIToggle(APIView):
    def get(self, request, format=None):
        #print("dedede")
        data = {
            "like_num":0,
        }
        return Response(data)

def contacts_view(request):
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    
    context = {
        "profile":profile,
    }
    return render(request, "contacts.html", context)


def trener_update(request, slug=None):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Trener, slug=slug)
    form = TrenerForm(request.POST or None, request.FILES or None, instance=instance)
    main_page = 'de'
    if len(MainPage.objects.all()) < 1:
        main_page = MainPage.objects.create()
    else:
        main_page = MainPage.objects.all()[0]
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(main_page.main_url())
    
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)

    context = {
        "title": instance.title,
        "instance": instance,
        "form":form,
        "user":request.user,
        "profile":profile,
    }
    return HttpResponseRedirect(main_page.main_url())



def trener_delete(request, slug=None):
    try:
        instance = Trener.objects.get(slug=slug)
    except:
        raise Http404

    if not request.user.is_staff and not request.user.is_superuser:
        reponse.status_code = 403 
        return HttpResponse("You do not have permission to do this.")

    main_page = 'de'
    if len(MainPage.objects.all()) < 1:
        main_page = MainPage.objects.create()
    else:
        main_page = MainPage.objects.all()[0]
    if request.method == "POST":
        instance.delete()
        return HttpResponseRedirect(main_page.main_url())
    context = {
        "object": instance
    }
    return render(request, "confirm_delete.html", context)
